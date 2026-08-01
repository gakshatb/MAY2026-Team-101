from datetime import datetime, timedelta
from urllib.parse import quote

from flask import Blueprint, jsonify, request # type: ignore
from flask_jwt_extended import get_jwt_identity # type: ignore

from models import db, User, Complaint, Department, ActivityLog, Feedback, now_ist
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
