from datetime import datetime, timedelta

from flask import Blueprint, jsonify # type: ignore
from flask_jwt_extended import get_jwt_identity # type: ignore

from models import db, User, Complaint, Department, ActivityLog, now_ist
from api_auth_utils import log_activity, role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


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