from datetime import datetime, timedelta
from urllib.parse import quote

from flask import Blueprint, jsonify, request # type: ignore
from flask_jwt_extended import get_jwt_identity # type: ignore

from models import db, User, Complaint, Department, ActivityLog, Feedback, Assignment, Announcement, now_ist
from api_auth_utils import log_activity, role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

HIGH_WORKLOAD_THRESHOLD = 50
VALID_DEPT_STATUSES = {'Active', 'Inactive', 'Under Maintenance'}


def _pct_change(curr, prev):
    """Percent change from prev -> curr. None if there's no meaningful baseline."""
    if prev == 0:
        return None if curr == 0 else 100.0
    return round(((curr - prev) / prev) * 100, 1)


# ─────────────────────────────────────────────────────────────────────────
# Admin dashboard
# ─────────────────────────────────────────────────────────────────────────
@admin_bp.route('/dashboard', methods=['GET'])
@role_required('Admin')
def dashboard():
    now = now_ist()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_start - timedelta(days=1)
    this_month_start = today_start.replace(day=1)
    last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)

    # ── Top stats ────────────────────────────────────────────────────
    def count_role(role, status=None):
        q = User.query.filter_by(role=role)
        if status:
            q = q.filter_by(status=status)
        return q.count()

    total_citizens = count_role('Citizen')
    total_officers = count_role('Officer', 'active')
    total_workers = count_role('Worker', 'active')
    total_complaints = Complaint.query.count()
    resolved_today = Complaint.query.filter(
        Complaint.status == 'Resolved', Complaint.updated_at >= today_start
    ).count()
    resolved_yesterday = Complaint.query.filter(
        Complaint.status == 'Resolved',
        Complaint.updated_at >= yesterday_start,
        Complaint.updated_at < today_start
    ).count()

    def month_count(model_query_fn):
        this_m = model_query_fn(this_month_start, now)
        last_m = model_query_fn(last_month_start, this_month_start)
        return _pct_change(this_m, last_m)

    citizens_trend = month_count(lambda a, b: User.query.filter(
        User.role == 'Citizen', User.created_at >= a, User.created_at < b).count())
    officers_trend = month_count(lambda a, b: User.query.filter(
        User.role == 'Officer', User.created_at >= a, User.created_at < b).count())
    workers_trend = month_count(lambda a, b: User.query.filter(
        User.role == 'Worker', User.created_at >= a, User.created_at < b).count())
    complaints_trend = month_count(lambda a, b: Complaint.query.filter(
        Complaint.created_at >= a, Complaint.created_at < b).count())
    resolved_trend = _pct_change(resolved_today, resolved_yesterday)

    top_stats = {
        "total_citizens":  {"value": total_citizens, "trend_pct": citizens_trend},
        "total_officers":  {"value": total_officers, "trend_pct": officers_trend},
        "total_workers":   {"value": total_workers, "trend_pct": workers_trend},
        "total_complaints": {"value": total_complaints, "trend_pct": complaints_trend},
        "resolved_today":  {"value": resolved_today, "trend_pct": resolved_trend},
    }

    # ── Department performance ──────────────────────────────────────
    dept_rows = (
        db.session.query(Complaint.department, db.func.count(Complaint.id))
        .group_by(Complaint.department)
        .all()
    )
    department_performance = []
    for dept_name, total in dept_rows:
        pending = Complaint.query.filter_by(department=dept_name, status='Pending').count()
        resolved_or_closed = Complaint.query.filter(
            Complaint.department == dept_name,
            Complaint.status.in_(['Resolved', 'Closed'])
        ).all()
        if resolved_or_closed:
            timed = [c for c in resolved_or_closed if c.updated_at]
            avg_hours = max(0, (sum((c.updated_at - c.created_at).total_seconds() for c in timed)
                         / max(1, len(timed)) / 3600)) if timed else 0
            avg_time_label = f"{int(avg_hours // 24)}d {int(avg_hours % 24)}h" if avg_hours >= 24 else f"{round(avg_hours, 1)}h"
        else:
            avg_time_label = "N/A"
        score = round((len(resolved_or_closed) / total) * 100) if total else 0
        department_performance.append({
            "name": dept_name, "total": total, "pending": pending,
            "avg_time": avg_time_label, "score": score
        })
    department_performance.sort(key=lambda d: d['total'], reverse=True)

    # ── Real system alerts (no fake infra metrics) ──────────────────
    alerts = []

    seven_days_ago = now - timedelta(days=7)
    inactive_staff = (
        User.query.filter(
            User.role.in_(['Officer', 'Worker']),
            User.status == 'active',
            ~User.id.in_(
                db.session.query(ActivityLog.user_id).filter(
                    ActivityLog.activity_type == 'login',
                    ActivityLog.created_at >= seven_days_ago
                )
            )
        ).all()
    )
    if inactive_staff:
        names = ", ".join(u.name for u in inactive_staff[:3])
        more = f" and {len(inactive_staff) - 3} more" if len(inactive_staff) > 3 else ""
        alerts.append({
            "type": "inactive_staff", "severity": "info",
            "title": f"{len(inactive_staff)} Officer/Worker Account(s) Inactive",
            "message": f"{names}{more} haven't logged in for 7+ days."
        })

    last_24h = now - timedelta(hours=24)
    emergency_spike = Complaint.query.filter(
        Complaint.priority == 'Emergency', Complaint.created_at >= last_24h
    ).count()
    if emergency_spike >= 3:
        alerts.append({
            "type": "emergency_spike", "severity": "critical",
            "title": "Emergency Complaint Spike",
            "message": f"{emergency_spike} Emergency-priority complaints submitted in the last 24 hours."
        })

    high_workload = [d for d in department_performance if d['pending'] >= 50]
    for d in high_workload:
        alerts.append({
            "type": "high_workload", "severity": "warning",
            "title": f"High Pending Backlog: {d['name']}",
            "message": f"{d['pending']} complaints pending in {d['name']}."
        })

    # ── Pending Officer/Worker approvals ─────────────────────────────
    pending_users = (
        User.query.filter(User.role.in_(['Officer', 'Worker']), User.status == 'pending')
        .order_by(User.created_at.asc())
        .limit(10)
        .all()
    )
    pending_approvals = [
        {
            "id": u.id, "name": u.name, "email": u.email, "role": u.role,
            "department": u.member_department.department_name if u.member_department else None,
            "requested_at": u.created_at.isoformat() if u.created_at else None
        }
        for u in pending_users
    ]

    # ── Recent platform-wide activity ────────────────────────────────
    recent_logs = (
        db.session.query(ActivityLog, User)
        .join(User, ActivityLog.user_id == User.id)
        .order_by(ActivityLog.created_at.desc())
        .limit(8)
        .all()
    )
    platform_activity = [
        {
            "id": log.id,
            "action": log.activity_type.replace('_', ' ').title(),
            "description": f"{user.name} ({user.role}): {log.description}",
            "created_at": log.created_at.isoformat() if log.created_at else None
        }
        for log, user in recent_logs
    ]

    # ── Growth chart: new Citizens vs new Workers, last 6 months ─────
    month_keys = []
    y, m = now.year, now.month
    for _ in range(6):
        month_keys.append((y, m))
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    month_keys.reverse()

    def bucket_users(role):
        counts = {k: 0 for k in month_keys}
        rows = User.query.filter_by(role=role).with_entities(User.created_at).all()
        for (created_at,) in rows:
            if created_at:
                key = (created_at.year, created_at.month)
                if key in counts:
                    counts[key] += 1
        return [counts[k] for k in month_keys]

    growth_chart = {
        "labels": [datetime(y, m, 1).strftime('%b') for (y, m) in month_keys],
        "new_citizens": bucket_users('Citizen'),
        "new_workers": bucket_users('Worker'),
    }

    # ── Category breakdown (platform-wide) ───────────────────────────
    category_rows = (
        db.session.query(Complaint.category, db.func.count(Complaint.id))
        .group_by(Complaint.category)
        .all()
    )

    return jsonify(
        success=True,
        top_stats=top_stats,
        department_performance=department_performance,
        alerts=alerts,
        pending_approvals=pending_approvals,
        pending_approvals_count=User.query.filter(
            User.role.in_(['Officer', 'Worker']), User.status == 'pending'
        ).count(),
        platform_activity=platform_activity,
        growth_chart=growth_chart,
        category_breakdown={cat: count for cat, count in category_rows},
    ), 200


# ─────────────────────────────────────────────────────────────────────────
# Approve / reject a pending Officer or Worker registration.
# ─────────────────────────────────────────────────────────────────────────
@admin_bp.route('/users/<int:user_id>/approve', methods=['PATCH'])
@role_required('Admin')
def approve_user(user_id):
    user = User.query.get(user_id)
    if not user or user.role not in ('Officer', 'Worker'):
        return jsonify(message="User not found."), 404
    if user.status != 'pending':
        return jsonify(message="This account is not pending approval."), 400

    user.status = 'active'
    log_activity(
        int(get_jwt_identity()), 'officer_approved',
        f'Approved {user.role.lower()} account for {user.name}.'
    )
    db.session.commit()
    return jsonify(success=True, message=f'{user.name} approved.'), 200


@admin_bp.route('/users/<int:user_id>/reject', methods=['PATCH'])
@role_required('Admin')
def reject_user(user_id):
    user = User.query.get(user_id)
    if not user or user.role not in ('Officer', 'Worker'):
        return jsonify(message="User not found."), 404
    if user.status != 'pending':
        return jsonify(message="This account is not pending approval."), 400

    user.status = 'rejected'
    log_activity(
        int(get_jwt_identity()), 'officer_rejected',
        f'Rejected {user.role.lower()} account for {user.name}.'
    )
    db.session.commit()
    return jsonify(success=True, message=f'{user.name} rejected.'), 200


# ─────────────────────────────────────────────────────────────────────────
# Department Management
# ─────────────────────────────────────────────────────────────────────────
def _avg_time_label(rows):
    """rows: Complaint objects with both created_at and updated_at set.
    Returns (label, numeric_hours_or_None)."""
    timed = [c for c in rows if c.updated_at]
    if not timed:
        return "N/A", None
    avg_hours = sum((c.updated_at - c.created_at).total_seconds() for c in timed) / len(timed) / 3600
    label = f"{int(avg_hours // 24)}d {int(avg_hours % 24)}h" if avg_hours >= 24 else f"{round(avg_hours, 1)}h"
    return label, avg_hours


def _avatar_url(user):
    if not user:
        return "https://ui-avatars.com/api/?name=NA&background=random"
    return user.profile_photo or f"https://ui-avatars.com/api/?name={quote(user.name)}&background=random"


def _serialize_department(dept):
    head = dept.head_officer
    officers_count = sum(1 for u in dept.members if u.role == 'Officer' and u.status == 'active')
    workers_count  = sum(1 for u in dept.members if u.role == 'Worker' and u.status == 'active')

    pending = Complaint.query.filter_by(department=dept.department_name, status='Pending').count()
    total   = Complaint.query.filter_by(department=dept.department_name).count()
    resolved_or_closed = Complaint.query.filter(
        Complaint.department == dept.department_name,
        Complaint.status.in_(['Resolved', 'Closed'])
    ).all()
    resolved_count = len(resolved_or_closed)
    avg_time_label, _ = _avg_time_label(resolved_or_closed)
    score = round((resolved_count / total) * 100) if total else 0

    display_status = dept.status
    if dept.status == 'Active' and pending >= HIGH_WORKLOAD_THRESHOLD:
        display_status = 'High Workload'

    return {
        "id":          dept.id,
        "code":        dept.code,
        "name":        dept.department_name,
        "description": dept.description,
        "head":        head.name if head else "Unassigned",
        "headEmail":   head.email if head else "N/A",
        "headPhone":   head.phone if head else "N/A",
        "headAvatar":  _avatar_url(head),
        "officers":    officers_count,
        "workers":     workers_count,
        "pending":     pending,
        "resolved":    resolved_count,
        "avgTime":     avg_time_label,
        "score":       score,
        "status":      display_status,     # display-only, may read "High Workload"
        "rawStatus":   dept.status,         # actual stored value: Active | Inactive | Under Maintenance
        "created":     dept.created_at.strftime('%b %d, %Y') if dept.created_at else None
    }


@admin_bp.route('/departments', methods=['GET'])
@role_required('Admin')
def list_departments():
    departments = Department.query.order_by(Department.department_name.asc()).all()
    serialized = [_serialize_department(d) for d in departments]

    total_departments = len(serialized)
    active_departments = sum(1 for d in serialized if d['rawStatus'] == 'Active')
    depts_without_officers = sum(1 for d in serialized if d['officers'] == 0)
    active_complaints = sum(d['pending'] for d in serialized)
    total_officers = User.query.filter_by(role='Officer', status='active').count()

    platform_resolved = Complaint.query.filter(
        Complaint.status.in_(['Resolved', 'Closed']),
        Complaint.updated_at.isnot(None)
    ).all()
    avg_resolution_label, _ = _avg_time_label(platform_resolved)

    top_stats = {
        "total_departments":           total_departments,
        "active_departments":          active_departments,
        "departments_without_officers": depts_without_officers,
        "active_complaints":           active_complaints,
        "total_officers":              total_officers,
        "avg_resolution":              avg_resolution_label,
    }

    # ── Quick insights ────────────────────────────────────────────────
    quick_insights = []
    with_volume = [d for d in serialized if (d['pending'] + d['resolved']) > 0]
    if with_volume:
        most_active = max(with_volume, key=lambda d: d['pending'] + d['resolved'])
        quick_insights.append({
            "label": "Most Active", "department": most_active['name'],
            "value": f"{most_active['pending'] + most_active['resolved']} Cmp"
        })

    # Fastest resolution — recompute numeric hours per department with data
    fastest = None
    for dept in departments:
        rows = Complaint.query.filter(
            Complaint.department == dept.department_name,
            Complaint.status.in_(['Resolved', 'Closed']),
            Complaint.updated_at.isnot(None)
        ).all()
        _, hours = _avg_time_label(rows)
        if hours is not None and (fastest is None or hours < fastest[1]):
            fastest = (dept.department_name, hours)
    if fastest:
        h = fastest[1]
        label = f"{int(h // 24)}d {int(h % 24)}h" if h >= 24 else f"{round(h, 1)}h"
        quick_insights.append({"label": "Fastest Resolution", "department": fastest[0], "value": label})

    # Highest average feedback rating, by department
    rating_rows = (
        db.session.query(Complaint.department, db.func.avg(Feedback.rating))
        .join(Feedback, Feedback.complaint_id == Complaint.id)
        .group_by(Complaint.department)
        .all()
    )
    rated = [(name, float(avg)) for name, avg in rating_rows if avg is not None]
    if rated:
        best = max(rated, key=lambda r: r[1])
        quick_insights.append({"label": "Highest Rating", "department": best[0], "value": f"{round(best[1], 1)}/5"})

    if with_volume:
        busiest = max(with_volume, key=lambda d: d['pending'])
        if busiest['pending'] > 0:
            quick_insights.append({
                "label": "High Workload Alert", "department": busiest['name'],
                "value": f"{busiest['pending']} Pnd"
            })

    # ── Recent department-related activity ──────────────────────────
    recent_logs = (
        db.session.query(ActivityLog, User)
        .join(User, ActivityLog.user_id == User.id)
        .filter(ActivityLog.activity_type.in_(['department_created', 'department_updated', 'department_deleted']))
        .order_by(ActivityLog.created_at.desc())
        .limit(10)
        .all()
    )
    recent_activities = [
        {
            "id": log.id,
            "action": log.activity_type.replace('_', ' ').title(),
            "description": log.description,
            "date": log.created_at.strftime('%b %d, %Y %I:%M %p') if log.created_at else None,
            "admin": user.name
        }
        for log, user in recent_logs
    ]

    return jsonify(
        success=True,
        departments=serialized,
        top_stats=top_stats,
        quick_insights=quick_insights,
        recent_activities=recent_activities
    ), 200


@admin_bp.route('/departments', methods=['POST'])
@role_required('Admin')
def create_department():
    data = request.get_json()
    if not data:
        return jsonify(message="Request body must be JSON."), 400

    name        = data.get('name', '').strip()
    code        = data.get('code', '').strip().upper()
    description = data.get('description', '').strip()
    status      = data.get('status', 'Active').strip()

    if not name:
        return jsonify(message="Department name is required."), 400
    if not code:
        return jsonify(message="Department code is required."), 400
    if status not in VALID_DEPT_STATUSES:
        return jsonify(message=f"Invalid status. Choose from: {', '.join(VALID_DEPT_STATUSES)}."), 400
    if Department.query.filter_by(department_name=name).first():
        return jsonify(message="A department with this name already exists."), 409
    if Department.query.filter_by(code=code).first():
        return jsonify(message="A department with this code already exists."), 409

    dept = Department(
        department_name=name, code=code,
        description=description or None, status=status
    )
    db.session.add(dept)
    db.session.flush()

    log_activity(int(get_jwt_identity()), 'department_created', f'Created department "{name}" ({code}).')
    db.session.commit()

    return jsonify(success=True, message="Department created.", department=_serialize_department(dept)), 201


@admin_bp.route('/departments/<int:dept_id>', methods=['PUT'])
@role_required('Admin')
def update_department(dept_id):
    dept = Department.query.get(dept_id)
    if not dept:
        return jsonify(message="Department not found."), 404

    data = request.get_json()
    if not data:
        return jsonify(message="Request body must be JSON."), 400

    name        = data.get('name', dept.department_name).strip()
    code        = data.get('code', dept.code or '').strip().upper()
    description = data.get('description', dept.description or '').strip()
    status      = data.get('status', dept.status).strip()

    if not name:
        return jsonify(message="Department name is required."), 400
    if status not in VALID_DEPT_STATUSES:
        return jsonify(message=f"Invalid status. Choose from: {', '.join(VALID_DEPT_STATUSES)}."), 400
    if name != dept.department_name and Department.query.filter_by(department_name=name).first():
        return jsonify(message="A department with this name already exists."), 409
    if code and code != dept.code and Department.query.filter_by(code=code).first():
        return jsonify(message="A department with this code already exists."), 409

    dept.department_name = name
    dept.code = code or None
    dept.description = description or None
    dept.status = status

    log_activity(int(get_jwt_identity()), 'department_updated', f'Updated department "{name}".')
    db.session.commit()

    return jsonify(success=True, message="Department updated.", department=_serialize_department(dept)), 200


@admin_bp.route('/departments/<int:dept_id>', methods=['DELETE'])
@role_required('Admin')
def delete_department(dept_id):
    dept = Department.query.get(dept_id)
    if not dept:
        return jsonify(message="Department not found."), 404

    has_members = len(dept.members) > 0
    has_active_complaints = Complaint.query.filter(
        Complaint.department == dept.department_name,
        ~Complaint.status.in_(['Resolved', 'Closed'])
    ).first() is not None

    if has_members or has_active_complaints:
        return jsonify(
            message="Departments with active complaints or assigned officers cannot be deleted."
        ), 400

    name = dept.department_name
    db.session.delete(dept)
    log_activity(int(get_jwt_identity()), 'department_deleted', f'Deleted department "{name}".')
    db.session.commit()

    return jsonify(success=True, message="Department deleted."), 200


@admin_bp.route('/departments/<int:dept_id>/assign-head', methods=['PATCH'])
@role_required('Admin')
def assign_department_head(dept_id):
    dept = Department.query.get(dept_id)
    if not dept:
        return jsonify(message="Department not found."), 404

    data = request.get_json()
    if not data:
        return jsonify(message="Request body must be JSON."), 400

    officer_id = data.get('officerId')
    if not officer_id:
        return jsonify(message="officerId is required."), 400

    officer = User.query.get(int(officer_id))
    if not officer or officer.role != 'Officer':
        return jsonify(message="Officer not found."), 404
    if officer.status != 'active':
        return jsonify(message="Only active officers can be assigned as department head."), 400

    dept.user_id = officer.id
    if officer.department_id != dept.id:
        officer.department_id = dept.id

    log_activity(
        int(get_jwt_identity()), 'department_updated',
        f'Assigned {officer.name} as head of "{dept.department_name}".'
    )
    db.session.commit()

    return jsonify(success=True, message="Department head assigned.", department=_serialize_department(dept)), 200


@admin_bp.route('/departments/eligible-heads', methods=['GET'])
@role_required('Admin')
def eligible_department_heads():
    """Active officers, for the 'Assign Head' dropdown."""
    officers = User.query.filter_by(role='Officer', status='active').order_by(User.name.asc()).all()
    return jsonify(
        success=True,
        officers=[
            {
                "id": o.id,
                "name": o.name,
                "currentDepartment": o.member_department.department_name if o.member_department else None
            }
            for o in officers
        ]
    ), 200


# ─────────────────────────────────────────────────────────────────────────
# Officer Management
# ─────────────────────────────────────────────────────────────────────────
def _experience_label(created_at):
    """Tenure since account creation — there's no separate 'years of prior
    experience' field, so this reflects time on this platform, not career
    history."""
    if not created_at:
        return "N/A"
    days = (now_ist() - created_at).days
    years, remainder_days = divmod(days, 365)
    months = remainder_days // 30
    if years and months:
        return f"{years} Yr {months} Mo"
    if years:
        return f"{years} Yr{'s' if years != 1 else ''}"
    if months:
        return f"{months} Mo{'s' if months != 1 else ''}"
    return f"{days} Day{'s' if days != 1 else ''}"


def _officer_complaint_stats(officer_id):
    """Returns (resolved_count, pending_count, avg_time_label, citizen_rating)
    for complaints assigned to one officer."""
    assigned = Complaint.query.filter_by(assigned_officer=officer_id).all()
    resolved_rows = [c for c in assigned if c.status in ('Resolved', 'Closed')]
    pending_count = sum(1 for c in assigned if c.status not in ('Resolved', 'Closed'))
    avg_time_label, _ = _avg_time_label(resolved_rows)

    rating_avg = (
        db.session.query(db.func.avg(Feedback.rating))
        .join(Complaint, Feedback.complaint_id == Complaint.id)
        .filter(Complaint.assigned_officer == officer_id)
        .scalar()
    )
    citizen_rating = round(float(rating_avg), 1) if rating_avg is not None else None

    return len(resolved_rows), pending_count, avg_time_label, citizen_rating


def _serialize_officer(u):
    resolved, pending, avg_time_label, citizen_rating = _officer_complaint_stats(u.id)
    total = resolved + pending
    score = round((resolved / total) * 100) if total else 0

    return {
        "id":           u.id,
        "empId":        f"OFC-{u.id:04d}",
        "name":         u.name,
        "designation":  u.designation,
        "department":   u.member_department.department_name if u.member_department else None,
        "departmentId": u.department_id,
        "email":        u.email,
        "phone":        u.phone,
        "joined":       u.created_at.strftime('%b %Y') if u.created_at else None,
        "experience":   _experience_label(u.created_at),
        "resolved":     resolved,
        "pending":      pending,
        "avgTime":      avg_time_label,
        "score":        score,
        "citizenRating": citizen_rating,
        "status":       u.status.capitalize(),   # Active | Suspended | Pending
        "avatar":       _avatar_url(u),
    }


@admin_bp.route('/officers', methods=['GET'])
@role_required('Admin')
def list_officers():
    """Matches OfficerManagement.vue: top stats, quick insights, the
    filterable officer table, pending registrations, and recent
    officer-related activity, all in one call."""
    all_officers = User.query.filter_by(role='Officer').filter(User.status != 'rejected').all()
    full = [_serialize_officer(u) for u in all_officers]   # unfiltered, used for stats/insights

    # ── apply filters/search/sort for the table itself ─────────────────
    result = full

    search = request.args.get('search', '').strip().lower()
    if search:
        result = [
            o for o in result
            if search in o['name'].lower() or search in o['empId'].lower() or search in o['email'].lower()
        ]

    status = request.args.get('status', 'All')
    if status != 'All':
        result = [o for o in result if o['status'] == status]

    department = request.args.get('department', 'All')
    if department != 'All':
        result = [o for o in result if o['department'] == department]

    performance = request.args.get('performance', 'All')
    if performance != 'All':
        def in_bucket(score):
            if performance == 'Excellent': return score >= 90
            if performance == 'Good': return 80 <= score < 90
            if performance == 'Average': return 60 <= score < 80
            return score < 60
        result = [o for o in result if in_bucket(o['score'])]

    sort = request.args.get('sort', 'Name')
    if sort == 'Complaints':
        result = sorted(result, key=lambda o: o['resolved'] + o['pending'], reverse=True)
    elif sort == 'Score':
        result = sorted(result, key=lambda o: o['score'], reverse=True)
    else:
        result = sorted(result, key=lambda o: o['name'].lower())

    # ── top stats (platform-wide, ignores the filters above) ───────────
    ratings = [o['citizenRating'] for o in full if o['citizenRating'] is not None]
    top_stats = {
        "total_officers":    len(full),
        "active_officers":   sum(1 for o in full if o['status'] == 'Active'),
        "pending_approvals": sum(1 for o in full if o['status'] == 'Pending'),
        "suspended":         sum(1 for o in full if o['status'] == 'Suspended'),
        "departments":       Department.query.count(),
        "avg_rating":        round(sum(ratings) / len(ratings), 1) if ratings else None,
    }

    # ── quick insights ──────────────────────────────────────────────────
    quick_insights = []
    scored = [o for o in full if (o['resolved'] + o['pending']) > 0]
    if scored:
        top_performer = max(scored, key=lambda o: o['score'])
        quick_insights.append({
            "label": "Top Performer",
            "value": f"{top_performer['name']} ({top_performer['department'] or 'Unassigned'})"
        })

    dept_activity = (
        db.session.query(Complaint.department, db.func.count(Complaint.id))
        .group_by(Complaint.department)
        .all()
    )
    if dept_activity:
        most_active = max(dept_activity, key=lambda d: d[1])
        quick_insights.append({"label": "Most Active Dept", "value": most_active[0]})

    if scored:
        highest_workload = max(scored, key=lambda o: o['pending'])
        if highest_workload['pending'] > 0:
            quick_insights.append({
                "label": "Highest Workload",
                "value": f"{highest_workload['name']} ({highest_workload['pending']} Cmp)"
            })

    # ── pending Officer registrations ───────────────────────────────────
    pending_users = (
        User.query.filter_by(role='Officer', status='pending')
        .order_by(User.created_at.asc())
        .all()
    )
    pending_registrations = [
        {
            "id":            u.id,
            "name":          u.name,
            "requestedDept": u.member_department.department_name if u.member_department else None,
            "date":          u.created_at.strftime('%b %d, %Y') if u.created_at else None,
        }
        for u in pending_users
    ]

    # ── recent officer-related admin activity ───────────────────────────
    officer_activity_types = [
        'officer_approved', 'officer_rejected', 'officer_suspended',
        'officer_reactivated', 'officer_updated', 'officer_transferred'
    ]
    recent_logs = (
        db.session.query(ActivityLog, User)
        .join(User, ActivityLog.user_id == User.id)
        .filter(ActivityLog.activity_type.in_(officer_activity_types))
        .order_by(ActivityLog.created_at.desc())
        .limit(10)
        .all()
    )
    recent_activities = [
        {
            "id":          log.id,
            "action":      log.activity_type.replace('_', ' ').title(),
            "description": log.description,
            "created_at":  log.created_at.isoformat() if log.created_at else None,
            "admin":       actor.name,
        }
        for log, actor in recent_logs
    ]

    return jsonify(
        success=True,
        top_stats=top_stats,
        quick_insights=quick_insights,
        officers=result,
        pending_registrations=pending_registrations,
        recent_activities=recent_activities,
        departments=[
            d.department_name for d in Department.query.order_by(Department.department_name.asc()).all()
        ],
    ), 200


@admin_bp.route('/officers/<int:officer_id>/suspend', methods=['PATCH'])
@role_required('Admin')
def suspend_officer(officer_id):
    officer = User.query.get(officer_id)
    if not officer or officer.role != 'Officer':
        return jsonify(message="Officer not found."), 404
    if officer.status != 'active':
        return jsonify(message="Only active officers can be suspended."), 400

    data = request.get_json(silent=True) or {}
    reason = data.get('reason', '').strip()

    officer.status = 'suspended'
    log_activity(
        int(get_jwt_identity()), 'officer_suspended',
        f'Suspended officer {officer.name}.' + (f' Reason: {reason}' if reason else '')
    )
    db.session.commit()

    return jsonify(success=True, message=f'{officer.name} suspended.', officer=_serialize_officer(officer)), 200


@admin_bp.route('/officers/<int:officer_id>/reactivate', methods=['PATCH'])
@role_required('Admin')
def reactivate_officer(officer_id):
    officer = User.query.get(officer_id)
    if not officer or officer.role != 'Officer':
        return jsonify(message="Officer not found."), 404
    if officer.status != 'suspended':
        return jsonify(message="Only suspended officers can be reactivated."), 400

    officer.status = 'active'
    log_activity(
        int(get_jwt_identity()), 'officer_reactivated',
        f'Reactivated officer {officer.name}.'
    )
    db.session.commit()

    return jsonify(success=True, message=f'{officer.name} reactivated.', officer=_serialize_officer(officer)), 200


@admin_bp.route('/officers/<int:officer_id>/transfer', methods=['PATCH'])
@role_required('Admin')
def transfer_officer(officer_id):
    officer = User.query.get(officer_id)
    if not officer or officer.role != 'Officer':
        return jsonify(message="Officer not found."), 404
    if officer.status not in ('active', 'suspended'):
        return jsonify(message="Only active or suspended officers can be transferred."), 400

    data = request.get_json()
    if not data:
        return jsonify(message="Request body must be JSON."), 400

    new_dept_id = data.get('departmentId')
    if not new_dept_id:
        return jsonify(message="departmentId is required."), 400

    new_dept = Department.query.get(int(new_dept_id))
    if not new_dept:
        return jsonify(message="Department not found."), 404
    if new_dept.id == officer.department_id:
        return jsonify(message="Officer is already assigned to this department."), 400

    old_dept = officer.member_department
    old_name = old_dept.department_name if old_dept else 'Unassigned'

    if old_dept and old_dept.user_id == officer.id:
        old_dept.user_id = None

    officer.department_id = new_dept.id

    log_activity(
        int(get_jwt_identity()), 'officer_transferred',
        f'Transferred {officer.name} from {old_name} to {new_dept.department_name}.'
    )
    db.session.commit()

    return jsonify(
        success=True,
        message=f'{officer.name} transferred to {new_dept.department_name}.',
        officer=_serialize_officer(officer)
    ), 200


# ─────────────────────────────────────────────────────────────────────────
# Single-officer detail — powers OfficerDetails.vue
# ─────────────────────────────────────────────────────────────────────────
@admin_bp.route('/officers/<int:officer_id>', methods=['GET'])
@role_required('Admin')
def officer_details(officer_id):
    officer = User.query.get(officer_id)
    if not officer or officer.role != 'Officer':
        return jsonify(message="Officer not found."), 404

    resolved, pending, avg_time_label, citizen_rating = _officer_complaint_stats(officer.id)
    total = resolved + pending
    score = round((resolved / total) * 100) if total else 0

    assigned_complaints = Complaint.query.filter_by(assigned_officer=officer.id).all()

    # Department rank — this officer's score vs every other officer in the same department.
    dept_rank = None
    if officer.department_id:
        dept_officers = User.query.filter_by(role='Officer', department_id=officer.department_id).all()
        scored = []
        for o in dept_officers:
            r, p, _, _ = _officer_complaint_stats(o.id)
            t = r + p
            scored.append((o.id, round((r / t) * 100) if t else 0))
        scored.sort(key=lambda x: x[1], reverse=True)
        for i, (oid, _) in enumerate(scored, start=1):
            if oid == officer.id:
                dept_rank = i
                break

    # Complaint status breakdown, for the doughnut chart.
    status_breakdown = {}
    for c in assigned_complaints:
        status_breakdown[c.status] = status_breakdown.get(c.status, 0) + 1

    # Monthly trend — last 6 months, complaints managed + resolution rate.
    monthly_trend = []
    today = now_ist().date()
    for i in range(5, -1, -1):
        y, m = today.year, today.month
        m -= i
        while m <= 0:
            m += 12
            y -= 1
        month_start_d = datetime(y, m, 1)
        next_m, next_y = (m + 1, y) if m < 12 else (1, y + 1)
        month_end_d = datetime(next_y, next_m, 1)

        month_complaints = [c for c in assigned_complaints
                             if c.created_at and month_start_d <= c.created_at < month_end_d]
        month_resolved = [c for c in month_complaints if c.status in ('Resolved', 'Closed')]
        rate = round((len(month_resolved) / len(month_complaints)) * 100) if month_complaints else 0
        monthly_trend.append({
            "month": month_start_d.strftime('%b'),
            "managed": len(month_complaints),
            "resolution_rate": rate,
        })

    # Worker summary — workers in this officer's department, and how many of
    # this officer's assignments they've completed.
    worker_summary = {"total": 0, "active": 0, "pending": 0, "completed": 0}
    if officer.department_id:
        dept_workers = User.query.filter_by(role='Worker', department_id=officer.department_id).all()
        worker_summary["total"] = len(dept_workers)
        worker_summary["active"] = sum(1 for w in dept_workers if w.status == 'active')
        worker_summary["pending"] = sum(1 for w in dept_workers if w.status == 'pending')
        worker_summary["completed"] = (
            db.session.query(Assignment)
            .join(Complaint, Assignment.complaint_id == Complaint.id)
            .filter(Assignment.assigned_by == officer.id, Complaint.status.in_(['Resolved', 'Closed']))
            .count()
        )

    # Quick insights — best month by volume, fastest resolution.
    quick_insights = {"best_month": None, "fastest_resolution": None}
    if monthly_trend:
        best = max(monthly_trend, key=lambda m: m["managed"])
        if best["managed"] > 0:
            quick_insights["best_month"] = best["month"]
    resolved_rows = [c for c in assigned_complaints if c.status in ('Resolved', 'Closed') and c.updated_at]
    if resolved_rows:
        fastest = min(resolved_rows, key=lambda c: c.updated_at - c.created_at)
        delta = fastest.updated_at - fastest.created_at
        hours = delta.total_seconds() / 3600
        if hours < 24:
            quick_insights["fastest_resolution"] = f"{int(hours)}h {int((hours % 1) * 60)}m ({fastest.category})"
        else:
            quick_insights["fastest_resolution"] = f"{int(hours // 24)}d {int(hours % 24)}h ({fastest.category})"

    # Recent complaints (latest 6), with the assigned worker's name if any.
    recent = sorted(assigned_complaints, key=lambda c: c.created_at, reverse=True)[:6]
    recent_complaints = []
    for c in recent:
        assignment = Assignment.query.filter_by(complaint_id=c.id).order_by(Assignment.assigned_at.desc()).first()
        worker = User.query.get(assignment.worker_id) if assignment else None
        recent_complaints.append({
            "id": f"CMP-{c.id:05d}",
            "category": c.category,
            "priority": c.priority,
            "status": c.status,
            "worker": worker.name if worker else None,
        })

    # Feedback on this officer's complaints.
    fb_rows = (
        Feedback.query.join(Complaint, Feedback.complaint_id == Complaint.id)
        .filter(Complaint.assigned_officer == officer.id)
        .order_by(Feedback.submitted_at.desc())
        .all()
    )
    avg_rating = round(sum(f.rating for f in fb_rows) / len(fb_rows), 1) if fb_rows else None
    recent_feedback = []
    for f in fb_rows[:4]:
        complaint = Complaint.query.get(f.complaint_id)
        citizen = User.query.get(complaint.created_by) if complaint else None
        recent_feedback.append({
            "name": "Anonymous" if f.is_anonymous else (citizen.name if citizen else "Citizen"),
            "date": f.submitted_at.strftime('%b %d, %Y') if f.submitted_at else None,
            "comment": f.comments,
        })

    # Last login — most recent 'login' ActivityLog row for this user.
    last_login_row = (
        ActivityLog.query.filter_by(user_id=officer.id, activity_type='login')
        .order_by(ActivityLog.created_at.desc())
        .first()
    )
    last_login = None
    if last_login_row:
        last_login = {
            "at": last_login_row.created_at.strftime('%b %d, %Y - %I:%M %p'),
            "ip": last_login_row.ip_address,
        }

    # Administrative history — officer lifecycle events that name this officer.
    admin_rows = (
        ActivityLog.query.filter(
            ActivityLog.activity_type.in_([
                'officer_approved', 'officer_rejected', 'officer_suspended',
                'officer_reactivated', 'officer_updated', 'officer_transferred',
            ]),
            ActivityLog.description.contains(officer.name),
        )
        .order_by(ActivityLog.created_at.desc())
        .limit(10)
        .all()
    )
    admin_activities = []
    for a in admin_rows:
        admin_user = User.query.get(a.user_id)
        admin_activities.append({
            "id": a.id,
            "action": a.activity_type.replace('_', ' ').title(),
            "description": a.description,
            "date": a.created_at.strftime('%b %d, %Y - %I:%M %p'),
            "admin": admin_user.name if admin_user else 'System',
        })

    dept = officer.member_department
    dept_head = None
    if dept and dept.user_id:
        head_user = User.query.get(dept.user_id)
        dept_head = head_user.name if head_user else None

    return jsonify(
        officer={
            "id":           officer.id,
            "empId":        f"OFC-{officer.id:04d}",
            "name":         officer.name,
            "designation":  officer.designation,
            "department":   dept.department_name if dept else None,
            "departmentId": officer.department_id,
            "email":        officer.email,
            "phone":        officer.phone,
            "gender":       officer.gender,
            "address":      officer.address,
            "city":         officer.city,
            "state":        officer.state,
            "pincode":      officer.pincode,
            "joined":       officer.created_at.strftime('%b %d, %Y') if officer.created_at else None,
            "experience":   _experience_label(officer.created_at),
            "status":       officer.status.capitalize(),
            "avatar":       _avatar_url(officer),
        },
        top_stats={
            "total_managed": total,
            "resolved":      resolved,
            "pending":       pending,
            "avg_time":      avg_time_label,
            "satisfaction":  citizen_rating,
            "dept_rank":     dept_rank,
        },
        department={
            "name":   dept.department_name if dept else None,
            "code":   dept.code if dept else None,
            "status": dept.status if dept else None,
            "head":   dept_head,
            "since":  dept.created_at.strftime('%b %Y') if dept and dept.created_at else None,
        },
        complaint_status_breakdown=status_breakdown,
        monthly_trend=monthly_trend,
        performance={
            "resolution_rate": score,
            "citizen_satisfaction_pct": round(citizen_rating * 20) if citizen_rating is not None else None,
        },
        worker_summary=worker_summary,
        quick_insights=quick_insights,
        recent_complaints=recent_complaints,
        feedback={
            "avg_rating": avg_rating,
            "total_reviews": len(fb_rows),
            "recent": recent_feedback,
        },
        last_login=last_login,
        admin_activities=admin_activities,
    ), 200


# ─────────────────────────────────────────────────────────────────────────
# System-wide notification feed for admins — powers Notifications.vue
# ─────────────────────────────────────────────────────────────────────────
NOTIFICATION_CATEGORIES = {
    'officer_approved':     'approvals',
    'officer_rejected':     'approvals',
    'officer_suspended':    'suspensions',
    'officer_reactivated':  'suspensions',
    'department_created':   'departments',
    'department_updated':   'departments',
    'department_deleted':   'departments',
}
OPEN_COMPLAINT_STATUSES = ('Pending', 'Under Review', 'Assigned', 'In Progress')


@admin_bp.route('/notifications', methods=['GET'])
@role_required('Admin')
def admin_notifications():
    limit = min(int(request.args.get('limit', 50)), 200)

    rows = (
        ActivityLog.query
        .filter(ActivityLog.activity_type.in_(NOTIFICATION_CATEGORIES.keys()))
        .order_by(ActivityLog.created_at.desc())
        .limit(200)
        .all()
    )
    notifications = []
    for a in rows:
        admin_user = User.query.get(a.user_id)
        notifications.append({
            "id":          f"activity-{a.id}",
            "category":    NOTIFICATION_CATEGORIES[a.activity_type],
            "title":       a.activity_type.replace('_', ' ').title(),
            "message":     a.description,
            "admin":       admin_user.name if admin_user else 'System',
            "created_at":  a.created_at.isoformat(),
        })

    escalated = (
        Complaint.query
        .filter(Complaint.is_escalated.is_(True), Complaint.status.in_(OPEN_COMPLAINT_STATUSES))
        .order_by(Complaint.created_at.desc())
        .limit(200)
        .all()
    )
    for c in escalated:
        notifications.append({
            "id":            f"escalation-{c.id}",
            "category":      "escalations",
            "title":         f"Escalated: {c.category}",
            "message":       f"{c.title} — {c.priority} priority, currently {c.status}.",
            "admin":         None,
            "complaint_id":  f"CMP-{c.id:05d}",
            "created_at":    c.created_at.isoformat(),
        })

    notifications.sort(key=lambda n: n["created_at"], reverse=True)
    notifications = notifications[:limit]

    summary = {
        "total":       len(notifications),
        "approvals":   sum(1 for n in notifications if n["category"] == "approvals"),
        "suspensions": sum(1 for n in notifications if n["category"] == "suspensions"),
        "departments": sum(1 for n in notifications if n["category"] == "departments"),
        "escalations": sum(1 for n in notifications if n["category"] == "escalations"),
    }

    return jsonify(success=True, summary=summary, notifications=notifications), 200


# ─────────────────────────────────────────────────────────────────────────
# Activity Logs — powers ActivityLogs.vue
# ─────────────────────────────────────────────────────────────────────────
ACTIVITY_MODULE = {
    'register': 'Authentication', 'login': 'Authentication', 'logout': 'Authentication',
    'password_changed': 'Authentication', 'password_reset_requested': 'Authentication',
    'password_reset_completed': 'Authentication',
    'profile_updated': 'Profile', 'profile_photo_updated': 'Profile', 'profile_photo_removed': 'Profile',
    'complaint_submitted': 'Complaint', 'feedback_submitted': 'Complaint',
    'officer_approved': 'Officer', 'officer_rejected': 'Officer', 'officer_suspended': 'Officer',
    'officer_reactivated': 'Officer', 'officer_updated': 'Officer', 'officer_transferred': 'Officer',
    'department_created': 'Department', 'department_updated': 'Department', 'department_deleted': 'Department',
}
ACTIVITY_STATUS = {
    'officer_rejected': 'Critical', 'officer_suspended': 'Critical',
    'department_deleted': 'Warning',
}
DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


@admin_bp.route('/activity-logs', methods=['GET'])
@role_required('Admin')
def activity_logs():
    limit = min(int(request.args.get('limit', 500)), 1000)
    now = now_ist()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    rows = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(limit).all()
    user_ids = {r.user_id for r in rows if r.user_id}
    users = {u.id: u for u in User.query.filter(User.id.in_(user_ids)).all()} if user_ids else {}
    dept_ids = {u.department_id for u in users.values() if u.department_id}
    depts = {d.id: d for d in Department.query.filter(Department.id.in_(dept_ids)).all()} if dept_ids else {}

    logs = []
    role_counts = {'Admin': 0, 'Officer': 0, 'Worker': 0, 'Citizen': 0}
    module_counts = {}
    action_counts = {}
    today_count = 0
    heatmap = [[0] * 24 for _ in range(7)]
    user_activity_counts = {}

    for r in rows:
        u = users.get(r.user_id)
        role = u.role if u else 'Citizen'
        dept_name = depts[u.department_id].department_name if (u and u.department_id in depts) else ''
        module = ACTIVITY_MODULE.get(r.activity_type, 'Other')
        status = ACTIVITY_STATUS.get(r.activity_type, 'Success')

        logs.append({
            "id":          f"LOG-{r.id:06d}",
            "date":        r.created_at.strftime('%b %d, %Y'),
            "time":        r.created_at.strftime('%H:%M:%S'),
            "created_at":  r.created_at.isoformat(),
            "user":        u.name if u else 'Unknown',
            "role":        role,
            "department":  dept_name,
            "action":      r.activity_type.replace('_', ' ').title(),
            "desc":        r.description,
            "module":      module,
            "status":      status,
            "ip":          r.ip_address or 'N/A',
        })

        if role in role_counts:
            role_counts[role] += 1
        module_counts[module] = module_counts.get(module, 0) + 1
        action_counts[r.activity_type] = action_counts.get(r.activity_type, 0) + 1
        if r.created_at >= today_start:
            today_count += 1
        heatmap[r.created_at.weekday()][r.created_at.hour] += 1
        if u:
            user_activity_counts.setdefault(u.id, {"name": u.name, "role": role, "count": 0})
            user_activity_counts[u.id]["count"] += 1

    top_stats = {
        "total_events":    len(logs),
        "today":           today_count,
        "admin_actions":   role_counts['Admin'],
        "officer_actions": role_counts['Officer'],
        "worker_actions":  role_counts['Worker'],
        "citizen_actions": role_counts['Citizen'],
        "security_events": action_counts.get('officer_suspended', 0) + action_counts.get('officer_rejected', 0),
        "system_events":   module_counts.get('Department', 0),
    }

    most_frequent = sorted(
        [{"label": k.replace('_', ' ').title(), "count": v} for k, v in action_counts.items()],
        key=lambda x: x["count"], reverse=True
    )[:6]

    # Log-statistics card: most active module, peak login hour, busiest day, avg/day
    most_active_module = max(module_counts, key=module_counts.get) if module_counts else 'N/A'
    login_hours = [r.created_at.hour for r in rows if r.activity_type == 'login']
    if login_hours:
        from collections import Counter
        peak_hour = Counter(login_hours).most_common(1)[0][0]
        peak_login = f"{peak_hour:02d}:00 - {(peak_hour + 1) % 24:02d}:00"
    else:
        peak_login = 'N/A'
    day_totals = [sum(heatmap[d]) for d in range(7)]
    busiest_day_idx = day_totals.index(max(day_totals)) if any(day_totals) else None
    busiest_day = f"{DAY_NAMES[busiest_day_idx]} ({day_totals[busiest_day_idx]})" if busiest_day_idx is not None else 'N/A'
    span_days = max((now.date() - rows[-1].created_at.date()).days, 1) if rows else 1
    avg_daily = round(len(logs) / span_days, 1)

    log_stats = {
        "most_active_module": most_active_module,
        "peak_login_hour":    peak_login,
        "busiest_day":        busiest_day,
        "avg_daily_events":   avg_daily,
    }

    security_events = [
        {"event": "Password Resets",      "severity": "Medium", "count": action_counts.get('password_reset_completed', 0)},
        {"event": "Account Suspensions",  "severity": "High",   "count": action_counts.get('officer_suspended', 0)},
        {"event": "Account Rejections",   "severity": "Medium", "count": action_counts.get('officer_rejected', 0)},
    ]

    critical_rows = [l for l in logs if l["status"] == "Critical"][:6]
    critical_events = [{
        "id": l["id"], "action": l["action"], "time": l["date"] + ' ' + l["time"],
        "desc": l["desc"], "user": l["user"],
        "color": "border-red-500",
    } for l in critical_rows]

    active_users = sorted(user_activity_counts.values(), key=lambda x: x["count"], reverse=True)[:6]

    return jsonify(
        success=True,
        top_stats=top_stats,
        log_stats=log_stats,
        most_frequent_activities=most_frequent,
        role_distribution=role_counts,
        heatmap=heatmap,
        security_events=security_events,
        critical_events=critical_events,
        active_users=active_users,
        logs=logs,
    ), 200


# ─────────────────────────────────────────────────────────────────────────
# Announcements — powers Announcements.vue
# ─────────────────────────────────────────────────────────────────────────
VALID_ANN_STATUS    = {'Draft', 'Scheduled', 'Published', 'Archived'}
VALID_ANN_CATEGORY  = {'Maintenance', 'Policy', 'Alert', 'Holiday', 'General'}
VALID_ANN_PRIORITY  = {'Emergency', 'Critical', 'Important', 'Normal'}
VALID_ANN_AUDIENCE  = {'All Users', 'Citizens', 'Officers', 'Workers'}


def _serialize_announcement(a, author_name):
    return {
        "id":         f"ANN-{a.id:04d}",
        "rawId":      a.id,
        "title":      a.title,
        "summary":    a.summary,
        "content":    a.content,
        "category":   a.category,
        "priority":   a.priority,
        "audience":   a.audience,
        "status":     a.status,
        "isPinned":   a.is_pinned,
        "views":      a.views,
        "publishDate": a.publish_at.strftime('%b %d, %Y') if a.publish_at else '-',
        "expiryDate":  a.expiry_at.strftime('%b %d, %Y') if a.expiry_at else '-',
        "author":     author_name,
        "createdAt":  a.created_at.isoformat(),
    }


@admin_bp.route('/announcements', methods=['GET'])
@role_required('Admin')
def list_announcements():
    rows = Announcement.query.order_by(Announcement.created_at.desc()).all()
    author_ids = {a.author_id for a in rows}
    authors = {u.id: u.name for u in User.query.filter(User.id.in_(author_ids)).all()} if author_ids else {}

    announcements = [_serialize_announcement(a, authors.get(a.author_id, 'Unknown')) for a in rows]

    top_stats = {
        "total":     len(rows),
        "published": sum(1 for a in rows if a.status == 'Published'),
        "scheduled": sum(1 for a in rows if a.status == 'Scheduled'),
        "drafts":    sum(1 for a in rows if a.status == 'Draft'),
        "archived":  sum(1 for a in rows if a.status == 'Archived'),
        "total_views": sum(a.views for a in rows),
    }

    published_rows = [a for a in rows if a.status == 'Published']
    most_viewed = max(rows, key=lambda a: a.views, default=None)
    audience_counts = {}
    for a in rows:
        audience_counts[a.audience] = audience_counts.get(a.audience, 0) + 1
    top_audience = max(audience_counts, key=audience_counts.get) if audience_counts else None
    category_counts = {}
    for a in rows:
        category_counts[a.category] = category_counts.get(a.category, 0) + 1
    top_category = max(category_counts, key=category_counts.get) if category_counts else None
    latest_published = max(published_rows, key=lambda a: a.publish_at or a.created_at, default=None)

    quick_insights = [
        {"label": "Most Viewed", "value": f"{most_viewed.title} ({most_viewed.views})" if most_viewed else 'N/A'},
        {"label": "Most Active Audience", "value": f"{top_audience} ({audience_counts[top_audience]})" if top_audience else 'N/A'},
        {"label": "Top Category", "value": top_category or 'N/A'},
        {"label": "Latest Published", "value": latest_published.title if latest_published else 'N/A'},
    ]

    pinned = [
        {"id": f"ANN-{a.id:04d}", "title": a.title, "audience": a.audience, "views": a.views}
        for a in rows if a.is_pinned
    ]

    priority_dist = {p: sum(1 for a in rows if a.priority == p) for p in VALID_ANN_PRIORITY}
    category_dist = {c: category_counts.get(c, 0) for c in VALID_ANN_CATEGORY}
    audience_dist = {aud: audience_counts.get(aud, 0) for aud in VALID_ANN_AUDIENCE}

    # Created-per-month, last 6 months (real — there's no view-tracking yet to chart instead)
    monthly_created = []
    today = now_ist().date()
    for i in range(5, -1, -1):
        y, m = today.year, today.month
        m -= i
        while m <= 0:
            m += 12; y -= 1
        month_start = datetime(y, m, 1)
        next_m, next_y = (m + 1, y) if m < 12 else (1, y + 1)
        month_end = datetime(next_y, next_m, 1)
        count = sum(1 for a in rows if a.created_at and month_start <= a.created_at < month_end)
        monthly_created.append({"month": month_start.strftime('%b'), "count": count})

    ann_activity_types = [
        'announcement_created', 'announcement_updated', 'announcement_published',
        'announcement_scheduled', 'announcement_archived', 'announcement_deleted',
    ]
    activity_rows = (
        ActivityLog.query.filter(ActivityLog.activity_type.in_(ann_activity_types))
        .order_by(ActivityLog.created_at.desc()).limit(10).all()
    )
    recent_activity = []
    for act in activity_rows:
        admin_user = User.query.get(act.user_id)
        recent_activity.append({
            "id": act.id,
            "action": act.activity_type.replace('announcement_', 'Announcement ').replace('_', ' ').title(),
            "desc": act.description,
            "time": act.created_at.strftime('%b %d, %Y - %I:%M %p'),
            "admin": admin_user.name if admin_user else 'System',
        })

    return jsonify(
        success=True,
        top_stats=top_stats,
        quick_insights=quick_insights,
        pinned=pinned,
        priority_distribution=priority_dist,
        category_distribution=category_dist,
        audience_distribution=audience_dist,
        monthly_created=monthly_created,
        recent_activity=recent_activity,
        announcements=announcements,
    ), 200


@admin_bp.route('/announcements', methods=['POST'])
@role_required('Admin')
def create_announcement():
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    content = (data.get('content') or '').strip()
    summary = (data.get('summary') or '').strip() or None
    category = data.get('category', 'General')
    priority = data.get('priority', 'Normal')
    audience = data.get('audience', 'All Users')
    action = data.get('action', 'draft')  # 'draft' | 'publish'
    publish_at_raw = data.get('publishAt')
    expiry_at_raw = data.get('expiryAt')

    if len(title) < 3:
        return jsonify(message="Title must be at least 3 characters."), 400
    if len(content) < 10:
        return jsonify(message="Content must be at least 10 characters."), 400
    if category not in VALID_ANN_CATEGORY:
        return jsonify(message=f"Invalid category. Choose from: {', '.join(sorted(VALID_ANN_CATEGORY))}."), 400
    if priority not in VALID_ANN_PRIORITY:
        return jsonify(message=f"Invalid priority. Choose from: {', '.join(sorted(VALID_ANN_PRIORITY))}."), 400
    if audience not in VALID_ANN_AUDIENCE:
        return jsonify(message=f"Invalid audience. Choose from: {', '.join(sorted(VALID_ANN_AUDIENCE))}."), 400

    publish_at = None
    expiry_at = None
    try:
        if publish_at_raw:
            publish_at = datetime.fromisoformat(publish_at_raw)
        if expiry_at_raw:
            expiry_at = datetime.fromisoformat(expiry_at_raw)
    except ValueError:
        return jsonify(message="Invalid date format."), 400

    if action == 'publish':
        if publish_at and publish_at > now_ist():
            status = 'Scheduled'
        else:
            status = 'Published'
            publish_at = now_ist()
    else:
        status = 'Draft'

    admin_id = int(get_jwt_identity())
    ann = Announcement(
        title=title, summary=summary, content=content, category=category,
        priority=priority, audience=audience, status=status,
        publish_at=publish_at, expiry_at=expiry_at, author_id=admin_id,
    )
    db.session.add(ann)
    db.session.flush()

    activity_type = 'announcement_scheduled' if status == 'Scheduled' else \
        ('announcement_published' if status == 'Published' else 'announcement_created')
    log_activity(admin_id, activity_type, f'{"Scheduled" if status == "Scheduled" else status} announcement "{title}".')
    db.session.commit()

    author = User.query.get(admin_id)
    return jsonify(success=True, announcement=_serialize_announcement(ann, author.name)), 201


@admin_bp.route('/announcements/<int:ann_id>', methods=['PUT'])
@role_required('Admin')
def update_announcement(ann_id):
    ann = Announcement.query.get(ann_id)
    if not ann:
        return jsonify(message="Announcement not found."), 404

    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    content = (data.get('content') or '').strip()

    if len(title) < 3:
        return jsonify(message="Title must be at least 3 characters."), 400
    if len(content) < 10:
        return jsonify(message="Content must be at least 10 characters."), 400

    category = data.get('category', ann.category)
    priority = data.get('priority', ann.priority)
    audience = data.get('audience', ann.audience)
    if category not in VALID_ANN_CATEGORY:
        return jsonify(message=f"Invalid category. Choose from: {', '.join(sorted(VALID_ANN_CATEGORY))}."), 400
    if priority not in VALID_ANN_PRIORITY:
        return jsonify(message=f"Invalid priority. Choose from: {', '.join(sorted(VALID_ANN_PRIORITY))}."), 400
    if audience not in VALID_ANN_AUDIENCE:
        return jsonify(message=f"Invalid audience. Choose from: {', '.join(sorted(VALID_ANN_AUDIENCE))}."), 400

    ann.title = title
    ann.content = content
    ann.summary = (data.get('summary') or '').strip() or None
    ann.category = category
    ann.priority = priority
    ann.audience = audience
    try:
        ann.expiry_at = datetime.fromisoformat(data['expiryAt']) if data.get('expiryAt') else None
    except ValueError:
        return jsonify(message="Invalid expiry date format."), 400

    admin_id = int(get_jwt_identity())
    log_activity(admin_id, 'announcement_updated', f'Updated announcement "{title}".')
    db.session.commit()

    author = User.query.get(ann.author_id)
    return jsonify(success=True, announcement=_serialize_announcement(ann, author.name if author else 'Unknown')), 200


@admin_bp.route('/announcements/<int:ann_id>', methods=['DELETE'])
@role_required('Admin')
def delete_announcement(ann_id):
    ann = Announcement.query.get(ann_id)
    if not ann:
        return jsonify(message="Announcement not found."), 404

    title = ann.title
    admin_id = int(get_jwt_identity())
    log_activity(admin_id, 'announcement_deleted', f'Deleted announcement "{title}".')
    db.session.delete(ann)
    db.session.commit()
    return jsonify(success=True, message=f'"{title}" deleted.'), 200


@admin_bp.route('/announcements/<int:ann_id>/publish', methods=['PATCH'])
@role_required('Admin')
def publish_announcement(ann_id):
    ann = Announcement.query.get(ann_id)
    if not ann:
        return jsonify(message="Announcement not found."), 404
    if ann.status == 'Published':
        return jsonify(message="Already published."), 400

    ann.status = 'Published'
    ann.publish_at = now_ist()

    admin_id = int(get_jwt_identity())
    log_activity(admin_id, 'announcement_published', f'Published announcement "{ann.title}".')
    db.session.commit()

    author = User.query.get(ann.author_id)
    return jsonify(success=True, announcement=_serialize_announcement(ann, author.name if author else 'Unknown')), 200


@admin_bp.route('/announcements/<int:ann_id>/archive', methods=['PATCH'])
@role_required('Admin')
def archive_announcement(ann_id):
    ann = Announcement.query.get(ann_id)
    if not ann:
        return jsonify(message="Announcement not found."), 404
    if ann.status == 'Archived':
        return jsonify(message="Already archived."), 400

    ann.status = 'Archived'

    admin_id = int(get_jwt_identity())
    log_activity(admin_id, 'announcement_archived', f'Archived announcement "{ann.title}".')
    db.session.commit()

    author = User.query.get(ann.author_id)
    return jsonify(success=True, announcement=_serialize_announcement(ann, author.name if author else 'Unknown')), 200


@admin_bp.route('/announcements/<int:ann_id>/pin', methods=['PATCH'])
@role_required('Admin')
def toggle_pin_announcement(ann_id):
    ann = Announcement.query.get(ann_id)
    if not ann:
        return jsonify(message="Announcement not found."), 404

    ann.is_pinned = not ann.is_pinned
    db.session.commit()

    author = User.query.get(ann.author_id)
    return jsonify(success=True, announcement=_serialize_announcement(ann, author.name if author else 'Unknown')), 200
