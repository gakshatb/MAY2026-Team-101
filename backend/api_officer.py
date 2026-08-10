from datetime import timedelta

from flask import Blueprint, jsonify, request  # type: ignore
from flask_jwt_extended import get_jwt_identity  # type: ignore

from models import (
    db, User, Complaint, Department, Assignment, Notification, StatusLog,
    Feedback, ActivityLog, now_ist
)
from api_auth_utils import log_activity, role_required

# Reuses the same image-upload helper citizens use for complaint photos —
# same validation, same Uploads folder, no need to duplicate it here.
from api_citizen import _save_uploaded_image

officer_bp = Blueprint('officer', __name__, url_prefix='/api/officer')

VALID_PRIORITIES = {'Low', 'Medium', 'High', 'Emergency'}

# Statuses an officer is allowed to set directly via /status. 'Resolved' is set
# by the worker on task completion; 'Closed' is admin-only (see api_admin.py).
OFFICER_SETTABLE_STATUSES = {'Assigned', 'In Progress'}

# Placeholder SLA window used only for the "days remaining" widget on
# ComplaintDetails.vue until per-category SLAs are modelled.
DEFAULT_SLA_DAYS = 7


def _current_officer():
    """Loads the logged-in officer's User row. Assumes @role_required('Officer') ran first."""
    return User.query.get(int(get_jwt_identity()))


def _serialize_officer_complaint(c):
    worker = None
    assignment = Assignment.query.filter_by(complaint_id=c.id).order_by(Assignment.assigned_at.desc()).first()
    if assignment:
        worker = User.query.get(assignment.worker_id)

    return {
        "id":         f"CMP-{c.id:05d}",
        "rawId":      c.id,
        "title":      c.title,
        "citizen":    c.citizen.name if c.citizen else 'Unknown',
        "citizenId":  c.created_by,
        "category":   c.category,
        "area":       c.area or c.city or '-',
        "priority":   c.priority,
        "status":     c.status,
        "worker":     worker.name if worker else None,
        "workerId":   worker.id if worker else None,
        "date":       c.created_at.strftime('%b %d, %Y'),
        "isEscalated": c.is_escalated,
    }


def _serialize_complaint_detail(c):
    base = _serialize_officer_complaint(c)
    citizen = c.citizen
    images = [img.image_url for img in c.images]
    history = [
        {
            "action": f"Status changed to {log.new_status}" if log.old_status else f"Complaint {log.new_status.lower()}",
            "date": log.changed_at.strftime('%b %d, %Y'),
            "time": log.changed_at.strftime('%H:%M'),
            "detail": log.remark,
        }
        for log in sorted(c.status_logs, key=lambda l: l.changed_at, reverse=True)
    ]
    related = (
        Complaint.query
        .filter(Complaint.area == c.area, Complaint.id != c.id, Complaint.area.isnot(None))
        .order_by(Complaint.created_at.desc())
        .limit(5)
        .all()
    ) if c.area else []

    target_date = c.created_at + timedelta(days=DEFAULT_SLA_DAYS)
    days_remaining = max(0, (target_date - now_ist()).days)
    complaint_age = (now_ist() - c.created_at).days

    resolution = None
    if c.status in ('Resolved', 'Closed'):
        resolved_log = next((l for l in c.status_logs if l.new_status == c.status), None)
        resolved_at = resolved_log.changed_at if resolved_log else c.updated_at
        if resolved_at:
            hours = round((resolved_at - c.created_at).total_seconds() / 3600, 1)
            resolution = {
                "date": resolved_at.strftime('%b %d, %Y'),
                "timeTaken": f"{hours}h",
                "notes": resolved_log.remark if resolved_log else None,
            }

    base.update({
        "description": c.description,
        "images": images,
        "location": {
            "address": ', '.join(filter(None, [c.street, c.landmark])) or c.location,
            "ward": c.ward or '-',
            "area": c.area or '-',
            "city": c.city or '-',
        },
        "submittedDate": c.created_at.strftime('%b %d, %Y'),
        "targetDate": target_date.strftime('%b %d, %Y'),
        "daysRemaining": days_remaining,
        "complaintAge": complaint_age,
        "citizenDetails": {
            "id": citizen.id if citizen else None,
            "name": citizen.name if citizen else 'Unknown',
            "phone": citizen.phone if citizen else None,
            "email": citizen.email if citizen else None,
            "registered": citizen.created_at.strftime('%b %d, %Y') if citizen else None,
            "prevComplaints": Complaint.query.filter_by(created_by=citizen.id).count() - 1 if citizen else 0,
        } if citizen else None,
        "history": history,
        "relatedComplaints": [
            {"id": f"CMP-{r.id:05d}", "rawId": r.id, "category": r.category,
             "status": r.status, "date": r.created_at.strftime('%b %d')}
            for r in related
        ],
        "resolution": resolution,
    })
    return base


# ─────────────────────────────────────────────────────────────────────────
# Complaint queue — powers ComplaintManagement.vue
# ─────────────────────────────────────────────────────────────────────────
@officer_bp.route('/complaints', methods=['GET'])
@role_required('Officer')
def list_complaints():
    officer = _current_officer()
    q = Complaint.query.filter_by(assigned_officer=officer.id)

    search = request.args.get('search', '').strip()
    if search:
        like = f"%{search}%"
        q = q.join(User, Complaint.created_by == User.id).filter(
            db.or_(Complaint.title.ilike(like), User.name.ilike(like))
        )

    status = request.args.get('status', 'All')
    if status != 'All':
        q = q.filter(Complaint.status == status)

    priority = request.args.get('priority', 'All')
    if priority != 'All':
        q = q.filter(Complaint.priority == priority)

    category = request.args.get('category', 'All')
    if category != 'All':
        q = q.filter(Complaint.category == category)

    rows = q.order_by(Complaint.created_at.desc()).all()
    all_rows = Complaint.query.filter_by(assigned_officer=officer.id).all()

    resolved_or_closed = [c for c in all_rows if c.status in ('Resolved', 'Closed') and c.updated_at]
    if resolved_or_closed:
        avg_hours = sum((c.updated_at - c.created_at).total_seconds() for c in resolved_or_closed) \
                    / len(resolved_or_closed) / 3600
        avg_resolution = f"{round(avg_hours / 24, 1)}d" if avg_hours >= 24 else f"{round(avg_hours, 1)}h"
    else:
        avg_resolution = 'N/A'

    summary_stats = {
        "total":       len(all_rows),
        "assigned":    sum(1 for c in all_rows if c.status == 'Assigned'),
        "in_progress": sum(1 for c in all_rows if c.status == 'In Progress'),
        "resolved":    sum(1 for c in all_rows if c.status == 'Resolved'),
        "emergency":   sum(1 for c in all_rows if c.priority == 'Emergency'),
        "avg_resolution": avg_resolution,
    }

    return jsonify(
        success=True,
        complaints=[_serialize_officer_complaint(c) for c in rows],
        summary_stats=summary_stats,
    ), 200


@officer_bp.route('/complaints/<int:complaint_id>', methods=['GET'])
@role_required('Officer')
def get_complaint(complaint_id):
    officer = _current_officer()
    c = Complaint.query.get(complaint_id)
    if not c:
        return jsonify(message="Complaint not found."), 404
    if c.assigned_officer != officer.id:
        return jsonify(message="This complaint is not assigned to you."), 403

    return jsonify(success=True, complaint=_serialize_complaint_detail(c)), 200


# ─────────────────────────────────────────────────────────────────────────
# Status & priority updates
# ─────────────────────────────────────────────────────────────────────────
@officer_bp.route('/complaints/<int:complaint_id>/status', methods=['PATCH'])
@role_required('Officer')
def update_status(complaint_id):
    officer = _current_officer()
    c = Complaint.query.get(complaint_id)
    if not c:
        return jsonify(message="Complaint not found."), 404
    if c.assigned_officer != officer.id:
        return jsonify(message="This complaint is not assigned to you."), 403

    data = request.get_json(silent=True) or {}
    new_status = data.get('status')
    if new_status not in OFFICER_SETTABLE_STATUSES:
        return jsonify(
            message=f"Officers can only set status to one of: {', '.join(sorted(OFFICER_SETTABLE_STATUSES))}."
        ), 400
    if c.status in ('Resolved', 'Closed'):
        return jsonify(message=f"Cannot change status of a complaint that is already {c.status}."), 400

    remark = (data.get('remark') or '').strip() or None
    old_status = c.status
    if new_status == old_status:
        return jsonify(message=f"Complaint is already {new_status}."), 400

    c.status = new_status
    db.session.add(StatusLog(complaint_id=c.id, old_status=old_status, new_status=new_status, remark=remark))
    db.session.add(Notification(
        user_id=c.created_by, complaint_id=c.id,
        title='Complaint Status Updated',
        message=f'Your complaint "{c.title}" status changed to {new_status}.',
        type='status_updated'
    ))
    log_activity(officer.id, 'complaint_status_updated',
                 f'Updated CMP-{c.id:05d} status to {new_status}.', complaint_id=c.id)
    db.session.commit()
    return jsonify(success=True, message='Status updated.', complaint=_serialize_officer_complaint(c)), 200


@officer_bp.route('/complaints/<int:complaint_id>/priority', methods=['PATCH'])
@role_required('Officer')
def update_priority(complaint_id):
    officer = _current_officer()
    c = Complaint.query.get(complaint_id)
    if not c:
        return jsonify(message="Complaint not found."), 404
    if c.assigned_officer != officer.id:
        return jsonify(message="This complaint is not assigned to you."), 403

    data = request.get_json(silent=True) or {}
    new_priority = data.get('priority')
    if new_priority not in VALID_PRIORITIES:
        return jsonify(message=f"Priority must be one of: {', '.join(sorted(VALID_PRIORITIES))}."), 400

    old_priority = c.priority
    c.priority = new_priority
    log_activity(officer.id, 'complaint_status_updated',
                 f'Changed CMP-{c.id:05d} priority from {old_priority} to {new_priority}.', complaint_id=c.id)
    db.session.commit()
    return jsonify(success=True, message='Priority updated.', complaint=_serialize_officer_complaint(c)), 200


# ─────────────────────────────────────────────────────────────────────────
# Send back to Admin for re-review
# ─────────────────────────────────────────────────────────────────────────
@officer_bp.route('/complaints/<int:complaint_id>/return-to-admin', methods=['PATCH'])
@role_required('Officer')
def return_to_admin(complaint_id):
    officer = _current_officer()
    c = Complaint.query.get(complaint_id)
    if not c:
        return jsonify(message="Complaint not found."), 404
    if c.assigned_officer != officer.id:
        return jsonify(message="This complaint is not assigned to you."), 403

    data = request.get_json(silent=True) or {}
    remark = (data.get('remark') or '').strip()
    if not remark:
        return jsonify(message="A remark explaining why this is being sent back is required."), 400

    old_status = c.status
    c.status = 'Under Review'
    c.assigned_officer = None

    db.session.add(StatusLog(complaint_id=c.id, old_status=old_status, new_status='Under Review', remark=remark))

    admins = User.query.filter_by(role='Admin', status='active').all()
    for admin in admins:
        db.session.add(Notification(
            user_id=admin.id, complaint_id=c.id,
            title='Complaint Returned by Officer',
            message=f'{officer.name} sent CMP-{c.id:05d} ("{c.title}") back for re-review: {remark}',
            type='status_updated'
        ))
    db.session.add(Notification(
        user_id=c.created_by, complaint_id=c.id,
        title='Complaint Under Re-Review',
        message=f'Your complaint "{c.title}" has been sent back to admin for re-review.',
        type='status_updated'
    ))
    log_activity(officer.id, 'complaint_returned',
                 f'Returned CMP-{c.id:05d} to admin: {remark}', complaint_id=c.id)
    db.session.commit()
    return jsonify(success=True, message='Complaint returned to admin.'), 200


# ─────────────────────────────────────────────────────────────────────────
# Worker roster (scoped to the officer's department) & assignment
# ─────────────────────────────────────────────────────────────────────────
@officer_bp.route('/workers', methods=['GET'])
@role_required('Officer')
def list_department_workers():
    officer = _current_officer()
    if not officer.department_id:
        return jsonify(success=True, workers=[]), 200

    workers = User.query.filter_by(role='Worker', department_id=officer.department_id, status='active').all()
    open_statuses = ('Assigned', 'In Progress')

    result = []
    for w in workers:
        active_tasks = (
            db.session.query(Assignment)
            .join(Complaint, Assignment.complaint_id == Complaint.id)
            .filter(Assignment.worker_id == w.id, Complaint.status.in_(open_statuses))
            .count()
        )
        result.append({
            "id": w.id,
            "name": w.name,
            "department": officer.member_department.department_name if officer.member_department else None,
            "activeTasks": active_tasks,
            "experienceYears": None,  # not modelled yet
        })
    return jsonify(success=True, workers=result), 200


@officer_bp.route('/complaints/<int:complaint_id>/assign-worker', methods=['PATCH'])
@role_required('Officer')
def assign_worker(complaint_id):
    officer = _current_officer()
    c = Complaint.query.get(complaint_id)
    if not c:
        return jsonify(message="Complaint not found."), 404
    if c.assigned_officer != officer.id:
        return jsonify(message="This complaint is not assigned to you."), 403
    if c.status not in ('Assigned', 'In Progress'):
        return jsonify(message=f"Cannot assign a worker to a complaint with status '{c.status}'."), 400

    data = request.get_json(silent=True) or {}
    worker_id = data.get('worker_id')
    if not worker_id:
        return jsonify(message="worker_id is required."), 400

    worker = User.query.get(worker_id)
    if not worker or worker.role != 'Worker':
        return jsonify(message="Worker not found."), 404
    if worker.status != 'active':
        return jsonify(message="Cannot assign a task to an inactive worker."), 400
    if worker.department_id != officer.department_id:
        return jsonify(message="Worker is not in your department."), 400

    priority = (data.get('priority') or '').strip()
    if priority and priority not in VALID_PRIORITIES:
        return jsonify(message=f"Priority must be one of: {', '.join(sorted(VALID_PRIORITIES))}."), 400
    if priority:
        c.priority = priority

    notes = (data.get('notes') or '').strip()

    old_status = c.status
    c.status = 'In Progress'

    db.session.add(Assignment(complaint_id=c.id, worker_id=worker.id, assigned_by=officer.id))
    remark = f'Assigned to field worker {worker.name}.'
    if notes:
        remark += f' Instructions: {notes}'
    db.session.add(StatusLog(
        complaint_id=c.id, old_status=old_status, new_status=c.status,
        remark=remark
    ))

    db.session.add(Notification(
        user_id=worker.id, complaint_id=c.id,
        title='New Task Assigned',
        message=f'You have been assigned CMP-{c.id:05d}: "{c.title}".' + (f' Note: {notes}' if notes else ''),
        type='assigned'
    ))
    db.session.add(Notification(
        user_id=c.created_by, complaint_id=c.id,
        title='Field Worker Assigned',
        message=f'A field worker has been assigned to your complaint "{c.title}".',
        type='assigned'
    ))
    log_activity(officer.id, 'worker_assigned',
                 f'Assigned CMP-{c.id:05d} to worker {worker.name}.', complaint_id=c.id)
    db.session.commit()
    return jsonify(success=True, message=f'Assigned to {worker.name}.', complaint=_serialize_officer_complaint(c)), 200

# ─────────────────────────────────────────────────────────────────────────
# Dashboard — KPIs, emergency queue, recent complaints, worker snapshot.
# Scoped entirely to complaints assigned to this officer and workers in
# their own department. Powers Dashboard.vue.
# ─────────────────────────────────────────────────────────────────────────
@officer_bp.route('/dashboard', methods=['GET'])
@role_required('Officer')
def dashboard():
    officer = _current_officer()
    base = Complaint.query.filter_by(assigned_officer=officer.id)

    total = base.count()
    assigned = base.filter_by(status='Assigned').count()
    in_progress = base.filter_by(status='In Progress').count()
    resolved = base.filter(Complaint.status.in_(['Resolved', 'Closed'])).count()
    emergency = base.filter(Complaint.priority == 'Emergency', Complaint.status.notin_(['Resolved', 'Closed'])).count()

    dept_workers = []
    if officer.department_id:
        dept_workers = User.query.filter_by(role='Worker', department_id=officer.department_id, status='active').all()

    open_statuses = ('Assigned', 'In Progress')

    def worker_active_tasks(worker_id):
        return (
            db.session.query(Assignment)
            .join(Complaint, Assignment.complaint_id == Complaint.id)
            .filter(Assignment.worker_id == worker_id, Complaint.status.in_(open_statuses))
            .count()
        )

    def worker_completed_tasks(worker_id):
        return (
            db.session.query(Assignment)
            .join(Complaint, Assignment.complaint_id == Complaint.id)
            .filter(Assignment.worker_id == worker_id, Complaint.status.in_(['Resolved', 'Closed']))
            .count()
        )

    worker_summaries = []
    for w in dept_workers:
        active_tasks = worker_active_tasks(w.id)
        worker_summaries.append({
            "id": w.id,
            "name": w.name,
            "activeTasks": active_tasks,
            "completedTasks": worker_completed_tasks(w.id),
            "status": 'Busy' if active_tasks > 0 else 'Available',
        })
    active_workers = sum(1 for w in worker_summaries if w["activeTasks"] > 0)
    top_workers = sorted(worker_summaries, key=lambda w: w["completedTasks"], reverse=True)[:5]

    resolved_rows = base.filter(Complaint.status.in_(['Resolved', 'Closed']), Complaint.updated_at.isnot(None)).all()
    if resolved_rows:
        avg_resolution_hours = round(
            sum((c.updated_at - c.created_at).total_seconds() for c in resolved_rows) / len(resolved_rows) / 3600, 1
        )
    else:
        avg_resolution_hours = None

    rating_avg = (
        db.session.query(db.func.avg(Feedback.rating))
        .join(Complaint, Feedback.complaint_id == Complaint.id)
        .filter(Complaint.assigned_officer == officer.id)
        .scalar()
    )
    avg_rating = round(float(rating_avg), 1) if rating_avg is not None else None

    feedback_rows = (
        db.session.query(Feedback)
        .join(Complaint, Feedback.complaint_id == Complaint.id)
        .filter(Complaint.assigned_officer == officer.id)
        .order_by(Feedback.submitted_at.desc())
        .all()
    )
    feedback_total = len(feedback_rows)
    if feedback_total:
        positive_pct = round(sum(1 for f in feedback_rows if f.rating >= 4) / feedback_total * 100)
        negative_pct = round(sum(1 for f in feedback_rows if f.rating <= 2) / feedback_total * 100)
        recent_comment = feedback_rows[0].comments
    else:
        positive_pct = None
        negative_pct = None
        recent_comment = None

    emergency_rows = (
        base.filter(Complaint.priority == 'Emergency', Complaint.status.notin_(['Resolved', 'Closed']))
        .order_by(Complaint.created_at.desc()).limit(5).all()
    )
    recent_rows = base.order_by(Complaint.created_at.desc()).limit(8).all()

    status_breakdown = {
        "Assigned":    assigned,
        "In Progress": in_progress,
        "Resolved":    base.filter_by(status='Resolved').count(),
        "Closed":      base.filter_by(status='Closed').count(),
    }

    now = now_ist()
    day_keys = [(now - timedelta(days=i)).date() for i in range(6, -1, -1)]
    trend_counts = {d: 0 for d in day_keys}
    for c in base.all():
        if c.created_at and c.created_at.date() in trend_counts:
            trend_counts[c.created_at.date()] += 1
    weekly_trend = [{"day": d.strftime('%a'), "count": trend_counts[d]} for d in day_keys]

    recent_notes = (
        Notification.query.filter_by(user_id=officer.id)
        .order_by(Notification.created_at.desc()).limit(5).all()
    )

    return jsonify(
        success=True,
        officer={
            "name": officer.name,
            "department": officer.member_department.department_name if officer.member_department else None,
        },
        kpi={
            "total":               total,
            "assigned":            assigned,
            "inProgress":          in_progress,
            "resolved":            resolved,
            "emergency":           emergency,
            "activeWorkers":       active_workers,
            "totalDeptWorkers":    len(dept_workers),
            "avgResolutionHours":  avg_resolution_hours,
            "avgRating":           avg_rating,
            "feedbackTotal":       feedback_total,
            "feedbackPositivePct": positive_pct,
            "feedbackNegativePct": negative_pct,
            "recentFeedbackComment": recent_comment,
        },
        statusBreakdown=status_breakdown,
        weeklyTrend=weekly_trend,
        emergencyComplaints=[_serialize_officer_complaint(c) for c in emergency_rows],
        recentComplaints=[_serialize_officer_complaint(c) for c in recent_rows],
        workerAvailability=worker_summaries[:6],
        topWorkers=top_workers,
        recentNotifications=[
            {
                "id": n.id, "title": n.title, "message": n.message,
                "isRead": n.is_read, "createdAt": n.created_at.isoformat() if n.created_at else None
            }
            for n in recent_notes
        ],
    ), 200


# ─────────────────────────────────────────────────────────────────────────
# Notifications — powers Notifications.vue
# ─────────────────────────────────────────────────────────────────────────
@officer_bp.route('/notifications', methods=['GET'])
@role_required('Officer')
def list_notifications():
    officer = _current_officer()
    notes = Notification.query.filter_by(user_id=officer.id).order_by(Notification.created_at.desc()).all()

    return jsonify(
        success=True,
        summary={
            "all":    len(notes),
            "unread": sum(1 for n in notes if not n.is_read),
            "read":   sum(1 for n in notes if n.is_read),
        },
        notifications=[
            {
                "id":          n.id,
                "title":       n.title,
                "message":     n.message,
                "type":        n.type,
                "complaintId": f"CMP-{n.complaint_id:05d}" if n.complaint_id else None,
                "isRead":      n.is_read,
                "createdAt":   n.created_at.isoformat() if n.created_at else None,
            }
            for n in notes
        ]
    ), 200


@officer_bp.route('/notifications/<int:notification_id>/read', methods=['PATCH'])
@role_required('Officer')
def mark_notification_read(notification_id):
    officer = _current_officer()
    note = Notification.query.get(notification_id)
    if not note or note.user_id != officer.id:
        return jsonify(message="Notification not found."), 404

    note.is_read = True
    db.session.commit()
    return jsonify(success=True), 200


@officer_bp.route('/notifications/read-all', methods=['PATCH'])
@role_required('Officer')
def mark_all_notifications_read():
    officer = _current_officer()
    Notification.query.filter_by(user_id=officer.id, is_read=False).update({"is_read": True})
    db.session.commit()
    return jsonify(success=True), 200


# ─────────────────────────────────────────────────────────────────────────
# Recent activity feed — powers the "Recent Activities" panel on
# Profile.vue. Mirrors the citizen implementation.
# ─────────────────────────────────────────────────────────────────────────
@officer_bp.route('/activity', methods=['GET'])
@role_required('Officer')
def list_activity():
    officer = _current_officer()

    try:
        limit = int(request.args.get('limit', 10))
    except ValueError:
        limit = 10
    limit = max(1, min(limit, 100))

    rows = (
        ActivityLog.query.filter_by(user_id=officer.id)
        .order_by(ActivityLog.created_at.desc())
        .limit(limit)
        .all()
    )

    return jsonify(
        success=True,
        activity=[
            {
                "id":          a.id,
                "type":        a.activity_type,
                "description": a.description,
                "complaintId": f"CMP-{a.complaint_id:05d}" if a.complaint_id else None,
                "createdAt":   a.created_at.isoformat() if a.created_at else None,
            }
            for a in rows
        ]
    ), 200


# ─────────────────────────────────────────────────────────────────────────
# Profile — powers Profile.vue. Only exposes fields that actually exist on
# User: no Employee ID cards, ward assignments, office locations, years of
# experience, documents, or achievements — none of that is modelled yet.
# Performance numbers (resolved count, avg rating) are computed from real
# Complaint/Feedback rows, the same way the dashboard does.
# ─────────────────────────────────────────────────────────────────────────
@officer_bp.route('/profile', methods=['GET'])
@role_required('Officer')
def get_profile():
    officer = _current_officer()
    dept = officer.member_department

    last_login = (
        ActivityLog.query
        .filter(ActivityLog.user_id == officer.id, ActivityLog.activity_type == 'login')
        .order_by(ActivityLog.created_at.desc())
        .first()
    )

    resolved_count = Complaint.query.filter(
        Complaint.assigned_officer == officer.id,
        Complaint.status.in_(['Resolved', 'Closed'])
    ).count()

    rating_avg = (
        db.session.query(db.func.avg(Feedback.rating))
        .join(Complaint, Feedback.complaint_id == Complaint.id)
        .filter(Complaint.assigned_officer == officer.id)
        .scalar()
    )
    avg_rating = round(float(rating_avg), 1) if rating_avg is not None else None

    return jsonify(
        success=True,
        profile={
            "id":            officer.id,
            "fullName":      officer.name,
            "email":         officer.email,
            "mobile":        officer.phone,
            "gender":        officer.gender,
            "dob":           officer.dob.strftime('%Y-%m-%d') if officer.dob else None,
            "nationality":   officer.nationality,
            "profilePhoto":  officer.profile_photo,
            "designation":   officer.designation,
            "department":    dept.department_name if dept else None,
            "empId":         f"OFC-{officer.id:04d}",
            "memberSince":   officer.created_at.strftime('%B %d, %Y') if officer.created_at else None,
            "lastLogin":     last_login.created_at.strftime('%b %d, %Y %I:%M %p') if last_login else None,
            "resolvedCount": resolved_count,
            "avgRating":     avg_rating,
        }
    ), 200


@officer_bp.route('/profile', methods=['PUT'])
@role_required('Officer')
def update_profile():
    officer = _current_officer()

    data = request.get_json()
    if not data:
        return jsonify(message="Request body must be JSON."), 400

    full_name = data.get('fullName', '').strip()
    mobile    = data.get('mobile', '').strip()
    gender    = data.get('gender', '').strip()

    if not full_name:
        return jsonify(message="Full Name is required."), 400
    if not mobile or not mobile.isdigit() or len(mobile) != 10:
        return jsonify(message="Enter a valid 10-digit mobile number."), 400

    officer.name  = full_name
    officer.phone = mobile
    if gender:
        officer.gender = gender

    log_activity(officer.id, 'profile_updated', 'Updated profile details.')
    db.session.commit()

    return jsonify(success=True, message="Profile updated successfully."), 200


@officer_bp.route('/profile/photo', methods=['POST'])
@role_required('Officer')
def upload_profile_photo():
    officer = _current_officer()

    if 'photo' not in request.files:
        return jsonify(message="No photo file was provided."), 400

    try:
        photo_url = _save_uploaded_image(request.files['photo'])
    except ValueError as e:
        return jsonify(message=str(e)), 400

    if not photo_url:
        return jsonify(message="No photo file was provided."), 400

    officer.profile_photo = photo_url
    log_activity(officer.id, 'profile_photo_updated', 'Updated profile photo.')
    db.session.commit()

    return jsonify(success=True, profilePhoto=photo_url), 200


@officer_bp.route('/profile/photo', methods=['DELETE'])
@role_required('Officer')
def delete_profile_photo():
    officer = _current_officer()
    officer.profile_photo = None
    log_activity(officer.id, 'profile_photo_removed', 'Removed profile photo.')
    db.session.commit()
    return jsonify(success=True), 200