from datetime import timedelta, datetime as dt

from flask import Blueprint, jsonify, request  # type: ignore
from flask_jwt_extended import get_jwt_identity  # type: ignore

from models import (
    db, User, Complaint, Department, Assignment, Notification, StatusLog,
    Feedback, ActivityLog, OfficerNote, now_ist
)
from api_auth_utils import log_activity, role_required

# Reuses the same image-upload helper citizens use for complaint photos —
# same validation, same Uploads folder, no need to duplicate it here.
from api_citizen import _save_uploaded_image

officer_bp = Blueprint('officer', __name__, url_prefix='/api/officer')

VALID_PRIORITIES = {'Low', 'Medium', 'High', 'Emergency'}
VALID_DURATIONS = {'Same Day', '1 Day', '2 Days', '3 Days', '1 Week'}

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
        "officerNotes": [
            {
                "id": note.id,
                "author": note.author.name if note.author else 'Unknown',
                "text": note.text,
                "timestamp": note.created_at.strftime('%b %d, %Y • %H:%M'),
            }
            for note in sorted(c.officer_notes, key=lambda n: n.created_at, reverse=True)
        ],
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
# Internal officer notes — private, never shown to the citizen or worker.
# Powers the "Internal Officer Notes" panel on ComplaintDetails.vue.
# ─────────────────────────────────────────────────────────────────────────
@officer_bp.route('/complaints/<int:complaint_id>/notes', methods=['POST'])
@role_required('Officer')
def add_note(complaint_id):
    officer = _current_officer()
    c = Complaint.query.get(complaint_id)
    if not c:
        return jsonify(message="Complaint not found."), 404
    if c.assigned_officer != officer.id:
        return jsonify(message="This complaint is not assigned to you."), 403

    data = request.get_json(silent=True) or {}
    text = (data.get('text') or '').strip()
    if not text:
        return jsonify(message="Note text is required."), 400
    if len(text) > 2000:
        return jsonify(message="Note is too long (2000 characters max)."), 400

    note = OfficerNote(complaint_id=c.id, author_id=officer.id, text=text)
    db.session.add(note)
    db.session.commit()

    return jsonify(success=True, note={
        "id": note.id,
        "author": officer.name,
        "text": note.text,
        "timestamp": note.created_at.strftime('%b %d, %Y • %H:%M'),
    }), 201


@officer_bp.route('/complaints/<int:complaint_id>/notes/<int:note_id>', methods=['DELETE'])
@role_required('Officer')
def delete_note(complaint_id, note_id):
    officer = _current_officer()
    c = Complaint.query.get(complaint_id)
    if not c:
        return jsonify(message="Complaint not found."), 404
    if c.assigned_officer != officer.id:
        return jsonify(message="This complaint is not assigned to you."), 403

    note = OfficerNote.query.filter_by(id=note_id, complaint_id=c.id).first()
    if not note:
        return jsonify(message="Note not found."), 404
    if note.author_id != officer.id:
        return jsonify(message="You can only delete your own notes."), 403

    db.session.delete(note)
    db.session.commit()
    return jsonify(success=True), 200


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
    if c.status not in ('Assigned',):
        return jsonify(message=f"Only complaints still at 'Assigned' (no worker yet) can be sent back. This one is '{c.status}'."), 400
    if Assignment.query.filter_by(complaint_id=c.id).first():
        return jsonify(message="A worker is already assigned to this complaint — reassign or complete it instead of sending it back."), 400

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
def _worker_avg_rating(worker_id):
    """Average citizen feedback rating across complaints this worker
    completed. Feedback is left against the complaint, not the worker
    directly, so we join through Assignment to attribute it."""
    avg = (
        db.session.query(db.func.avg(Feedback.rating))
        .join(Complaint, Feedback.complaint_id == Complaint.id)
        .join(Assignment, Assignment.complaint_id == Complaint.id)
        .filter(Assignment.worker_id == worker_id)
        .scalar()
    )
    return round(float(avg), 1) if avg is not None else None


def _worker_avg_resolution_hours(worker_id):
    """Avg hours between a worker being assigned and the complaint being
    marked Resolved/Closed, across their completed tasks."""
    rows = (
        db.session.query(Assignment.assigned_at, Complaint.updated_at)
        .join(Complaint, Assignment.complaint_id == Complaint.id)
        .filter(Assignment.worker_id == worker_id, Complaint.status.in_(('Resolved', 'Closed')))
        .all()
    )
    if not rows:
        return None
    hours = [(done - started).total_seconds() / 3600 for started, done in rows if done and started]
    return round(sum(hours) / len(hours), 1) if hours else None


def _serialize_worker(w, officer):
    open_statuses = ('Assigned', 'In Progress')
    active_tasks = (
        db.session.query(Assignment)
        .join(Complaint, Assignment.complaint_id == Complaint.id)
        .filter(Assignment.worker_id == w.id, Complaint.status.in_(open_statuses))
        .count()
    )
    completed_tasks = (
        db.session.query(Assignment)
        .join(Complaint, Assignment.complaint_id == Complaint.id)
        .filter(Assignment.worker_id == w.id, Complaint.status.in_(('Resolved', 'Closed')))
        .count()
    )
    total = active_tasks + completed_tasks
    completion_rate = round((completed_tasks / total) * 100) if total else None

    return {
        "id":                w.id,
        "empId":             f"WRK-{w.id:04d}",
        "name":              w.name,
        "email":             w.email,
        "phone":             w.phone,
        "profilePhoto":      w.profile_photo,
        "accountStatus":     w.status,
        "department":        officer.member_department.department_name if officer.member_department else None,
        "activeTasks":       active_tasks,
        "completedTasks":    completed_tasks,
        "completionRate":    completion_rate,
        "avgRating":         _worker_avg_rating(w.id),
        "avgResolutionHours": _worker_avg_resolution_hours(w.id),
        "memberSince":       w.created_at.strftime('%b %Y') if w.created_at else None,
    }


@officer_bp.route('/workers', methods=['GET'])
@role_required('Officer')
def list_department_workers():
    officer = _current_officer()
    if not officer.department_id:
        return jsonify(success=True, summary={}, workers=[]), 200

    workers = User.query.filter_by(role='Worker', department_id=officer.department_id).all()
    result = [_serialize_worker(w, officer) for w in workers]

    summary = {
        "total":     len(result),
        "active":    sum(1 for w in result if w['accountStatus'] == 'active'),
        "suspended": sum(1 for w in result if w['accountStatus'] == 'suspended'),
        "busyNow":   sum(1 for w in result if w['activeTasks'] > 0),
        "completedTotal": sum(w['completedTasks'] for w in result),
        "pendingTotal":   sum(w['activeTasks'] for w in result),
    }
    rated = [w['avgRating'] for w in result if w['avgRating'] is not None]
    summary["avgRating"] = round(sum(rated) / len(rated), 1) if rated else None

    return jsonify(success=True, summary=summary, workers=result), 200


@officer_bp.route('/workers/<int:worker_id>', methods=['GET'])
@role_required('Officer')
def get_worker_detail(worker_id):
    officer = _current_officer()
    w = User.query.get(worker_id)
    if not w or w.role != 'Worker' or w.department_id != officer.department_id:
        return jsonify(message="Worker not found in your department."), 404

    data = _serialize_worker(w, officer)

    current = (
        Complaint.query
        .join(Assignment, Assignment.complaint_id == Complaint.id)
        .filter(Assignment.worker_id == w.id, Complaint.status.in_(('Assigned', 'In Progress')))
        .order_by(Complaint.created_at.desc())
        .all()
    )
    data["currentAssignments"] = []
    for c in current:
        assignment = (
            Assignment.query.filter_by(complaint_id=c.id, worker_id=w.id)
            .order_by(Assignment.assigned_at.desc()).first()
        )
        data["currentAssignments"].append({
            "id": f"CMP-{c.id:05d}", "rawId": c.id, "category": c.category,
            "priority": c.priority, "status": c.status,
            "expectedCompletionDate": assignment.expected_completion_date.isoformat() if assignment and assignment.expected_completion_date else None,
            "expectedDuration": assignment.expected_duration if assignment else None,
        })

    # No per-worker action log exists yet (that lives in api_worker.py,
    # not built), so recent activity is approximated from status changes
    # on complaints this worker has been assigned to.
    recent_logs = (
        db.session.query(StatusLog)
        .join(Assignment, Assignment.complaint_id == StatusLog.complaint_id)
        .filter(Assignment.worker_id == w.id)
        .order_by(StatusLog.changed_at.desc())
        .limit(8)
        .all()
    )
    data["recentActivity"] = [
        {
            "action": f"Status changed to {log.new_status}",
            "complaintId": f"CMP-{log.complaint_id:05d}",
            "date": log.changed_at.strftime('%b %d, %Y %H:%M') if log.changed_at else None,
        }
        for log in recent_logs
    ]

    return jsonify(success=True, worker=data), 200


@officer_bp.route('/workers/<int:worker_id>/status', methods=['PATCH'])
@role_required('Officer')
def set_worker_status(worker_id):
    officer = _current_officer()
    w = User.query.get(worker_id)
    if not w or w.role != 'Worker' or w.department_id != officer.department_id:
        return jsonify(message="Worker not found in your department."), 404

    data = request.get_json(silent=True) or {}
    new_status = data.get('status')
    if new_status not in ('active', 'suspended'):
        return jsonify(message="status must be 'active' or 'suspended'."), 400

    if new_status == 'suspended':
        open_tasks = (
            db.session.query(Assignment)
            .join(Complaint, Assignment.complaint_id == Complaint.id)
            .filter(Assignment.worker_id == w.id, Complaint.status.in_(('Assigned', 'In Progress')))
            .count()
        )
        if open_tasks:
            return jsonify(message=f"{w.name} has {open_tasks} active task(s). Reassign them before suspending."), 400

    w.status = new_status
    log_activity(
        officer.id, 'worker_status_updated',
        f'{"Suspended" if new_status == "suspended" else "Reactivated"} worker {w.name}.',
    )
    db.session.commit()

    return jsonify(success=True, worker=_serialize_worker(w, officer)), 200


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
    remarks = (data.get('remarks') or '').strip()

    duration = (data.get('expectedDuration') or '').strip()
    if duration and duration not in VALID_DURATIONS:
        return jsonify(message=f"expectedDuration must be one of: {', '.join(sorted(VALID_DURATIONS))}."), 400

    expected_date = None
    raw_date = (data.get('expectedCompletionDate') or '').strip()
    if raw_date:
        try:
            expected_date = dt.strptime(raw_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify(message="expectedCompletionDate must be in YYYY-MM-DD format."), 400

    checks = data.get('checks') or {}

    old_status = c.status
    c.status = 'In Progress'

    db.session.add(Assignment(
        complaint_id=c.id, worker_id=worker.id, assigned_by=officer.id,
        expected_completion_date=expected_date,
        expected_duration=duration or None,
        internal_remarks=remarks or None,
        checklist_verified=bool(checks.get('verified')),
        checklist_materials=bool(checks.get('materials')),
        checklist_location=bool(checks.get('location')),
        checklist_notified=bool(checks.get('notified')),
    ))
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
    return jsonify(
        success=True,
        message=f'Assigned to {worker.name}.',
        complaint=_serialize_officer_complaint(c),
        assignment={
            'expectedCompletionDate': expected_date.isoformat() if expected_date else None,
            'expectedDuration': duration or None,
            'remarks': remarks or None,
            'checks': {
                'verified': bool(checks.get('verified')),
                'materials': bool(checks.get('materials')),
                'location': bool(checks.get('location')),
                'notified': bool(checks.get('notified')),
            },
        },
    ), 200

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


DATE_RANGE_DAYS = {'today': 1, 'week': 7, 'month': 30, 'quarter': 90, 'year': 365}


@officer_bp.route('/analytics', methods=['GET'])
@role_required('Officer')
def analytics():
    officer = _current_officer()
    base = Complaint.query.filter_by(assigned_officer=officer.id)

    date_range = request.args.get('date', 'month')
    days = DATE_RANGE_DAYS.get(date_range, 30)
    period_start = now_ist() - timedelta(days=days)

    category = request.args.get('category', 'all')
    ward = request.args.get('ward', 'all')

    period_rows = base.filter(Complaint.created_at >= period_start)
    if category != 'all':
        period_rows = period_rows.filter(Complaint.category == category)
    if ward != 'all':
        period_rows = period_rows.filter(Complaint.ward == ward)
    period_rows = period_rows.all()

    total = len(period_rows)
    resolved = sum(1 for c in period_rows if c.status in ('Resolved', 'Closed'))
    resolution_rate = round((resolved / total) * 100) if total else 0

    active_workers = User.query.filter_by(
        role='Worker', status='active', department_id=officer.department_id
    ).count()

    avg_rating = (
        db.session.query(db.func.avg(Feedback.rating))
        .join(Complaint, Feedback.complaint_id == Complaint.id)
        .filter(Complaint.assigned_officer == officer.id, Complaint.created_at >= period_start)
        .scalar()
    )
    avg_rating = round(float(avg_rating), 1) if avg_rating is not None else None

    # Daily volume trend: received vs resolved, for the selected window.
    day_buckets = {}
    for c in period_rows:
        day = c.created_at.strftime('%Y-%m-%d')
        day_buckets.setdefault(day, {"received": 0, "resolved": 0})
        day_buckets[day]["received"] += 1

    resolved_logs = (
        db.session.query(StatusLog)
        .join(Complaint, StatusLog.complaint_id == Complaint.id)
        .filter(
            Complaint.assigned_officer == officer.id,
            StatusLog.new_status == 'Resolved',
            StatusLog.changed_at >= period_start,
        )
        .all()
    )
    for log in resolved_logs:
        day = log.changed_at.strftime('%Y-%m-%d')
        day_buckets.setdefault(day, {"received": 0, "resolved": 0})
        day_buckets[day]["resolved"] += 1

    trend = [
        {"date": day, "received": v["received"], "resolved": v["resolved"]}
        for day, v in sorted(day_buckets.items())
    ]

    # Category breakdown (donut) + per-category resolution rate (bar) —
    # replaces the original "Department Performance" chart, which doesn't
    # make sense scoped to a single officer's own department.
    categories = {}
    for c in period_rows:
        categories.setdefault(c.category, {"total": 0, "resolved": 0})
        categories[c.category]["total"] += 1
        if c.status in ('Resolved', 'Closed'):
            categories[c.category]["resolved"] += 1

    category_breakdown = [{"category": k, "count": v["total"]} for k, v in categories.items()]
    category_performance = [
        {"category": k, "resolutionRate": round((v["resolved"] / v["total"]) * 100) if v["total"] else 0}
        for k, v in categories.items()
    ]

    # Status by ward (stacked bar) — uses real ward values as entered by
    # citizens, not fabricated W1..W5 labels.
    wards = {}
    for c in period_rows:
        w_label = c.ward or 'Unspecified'
        wards.setdefault(w_label, {"Resolved": 0, "In Progress": 0, "Pending": 0})
        if c.status in ('Resolved', 'Closed'):
            wards[w_label]["Resolved"] += 1
        elif c.status == 'In Progress':
            wards[w_label]["In Progress"] += 1
        else:
            wards[w_label]["Pending"] += 1
    ward_status = [{"ward": k, **v} for k, v in wards.items()]

    emergency_rows = (
        base.filter_by(priority='Emergency')
        .filter(Complaint.status.notin_(('Resolved', 'Closed')))
        .order_by(Complaint.created_at.asc())
        .all()
    )
    emergency_complaints = []
    for c in emergency_rows:
        assignment = Assignment.query.filter_by(complaint_id=c.id).order_by(Assignment.assigned_at.desc()).first()
        worker = User.query.get(assignment.worker_id) if assignment else None
        hours_pending = round((now_ist() - c.created_at).total_seconds() / 3600, 1)
        emergency_complaints.append({
            "id": f"CMP-{c.id:05d}", "rawId": c.id, "category": c.category,
            "area": c.area or c.city or '-', "worker": worker.name if worker else None,
            "hoursPending": hours_pending,
        })

    workers = User.query.filter_by(role='Worker', department_id=officer.department_id).all()
    top_workers = sorted(
        [_serialize_worker(w, officer) for w in workers],
        key=lambda w: w['completedTasks'], reverse=True
    )[:5]

    # Aging buckets — how long currently-open complaints (not period-
    # filtered, this is a snapshot of right now) have been sitting.
    open_rows = base.filter(Complaint.status.notin_(('Resolved', 'Closed'))).all()
    aging = {"0-2": 0, "3-5": 0, "6-10": 0, "10+": 0}
    for c in open_rows:
        age_days = (now_ist() - c.created_at).days
        if age_days <= 2:
            aging["0-2"] += 1
        elif age_days <= 5:
            aging["3-5"] += 1
        elif age_days <= 10:
            aging["6-10"] += 1
        else:
            aging["10+"] += 1

    # Rating distribution — real histogram from citizen feedback on this
    # officer's complaints within the selected period.
    rating_rows = (
        db.session.query(Feedback.rating)
        .join(Complaint, Feedback.complaint_id == Complaint.id)
        .filter(Complaint.assigned_officer == officer.id, Complaint.created_at >= period_start)
        .all()
    )
    rating_counts = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for (r,) in rating_rows:
        if r in rating_counts:
            rating_counts[r] += 1
    total_ratings = sum(rating_counts.values())

    return jsonify(
        success=True,
        kpis={
            "totalComplaints":  total,
            "activeWorkers":    active_workers,
            "resolutionRate":   resolution_rate,
            "citizenSatisfaction": avg_rating,
        },
        categoryOptions=sorted({c.category for c in base.all()}),
        wardOptions=sorted({c.ward for c in base.all() if c.ward}),
        trend=trend,
        categoryBreakdown=category_breakdown,
        categoryPerformance=category_performance,
        wardStatus=ward_status,
        emergencyComplaints=emergency_complaints,
        topWorkers=top_workers,
        aging=aging,
        ratingDistribution={
            "counts": rating_counts,
            "total": total_ratings,
        },
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