from flask import Blueprint, jsonify, request  # type: ignore
from flask_jwt_extended import get_jwt_identity  # type: ignore

from models import db, Assignment, Complaint, ComplaintImages, Notification, StatusLog, User
from api_auth_utils import log_activity, role_required
from api_citizen import _save_uploaded_image

worker_bp = Blueprint('worker', __name__, url_prefix='/api/worker')

OPEN_STATUSES = ('Assigned', 'In Progress')
FINAL_STATUSES = ('Resolved', 'Closed')


def _current_worker():
    return User.query.get(int(get_jwt_identity()))


def _assignment_for(worker_id, complaint_id):
    """Return the current assignment, if this complaint belongs to this worker."""
    latest = Assignment.query.filter_by(complaint_id=complaint_id).order_by(
        Assignment.assigned_at.desc()
    ).first()
    return latest if latest and latest.worker_id == worker_id else None


def _serialize_task(complaint, include_full=False):
    assignment = Assignment.query.filter_by(complaint_id=complaint.id).order_by(
        Assignment.assigned_at.desc()
    ).first()
    officer = User.query.get(complaint.assigned_officer) if complaint.assigned_officer else None
    data = {
        'id': f'CMP-{complaint.id:05d}',
        'raw_id': complaint.id,
        'title': complaint.title,
        'category': complaint.category,
        'priority': complaint.priority,
        'status': complaint.status,
        'area': complaint.area or complaint.city or complaint.location,
        'location': complaint.location,
        'assigned_at': assignment.assigned_at.isoformat() if assignment else None,
        'officer': officer.name if officer else None,
        'officer_id': officer.id if officer else None,
        'created_at': complaint.created_at.isoformat() if complaint.created_at else None,
    }
    if include_full:
        data.update({
            'description': complaint.description,
            'department': complaint.department,
            'city': complaint.city,
            'ward': complaint.ward,
            'street': complaint.street,
            'landmark': complaint.landmark,
            'images': [image.image_url for image in complaint.images],
            'history': [{
                'old_status': entry.old_status,
                'new_status': entry.new_status,
                'remark': entry.remark,
                'changed_at': entry.changed_at.isoformat(),
            } for entry in sorted(complaint.status_logs, key=lambda item: item.changed_at, reverse=True)],
        })
    return data


def _worker_tasks(worker_id, statuses=None):
    assignments = Assignment.query.filter_by(worker_id=worker_id).order_by(Assignment.assigned_at.desc()).all()
    complaint_ids = []
    for assignment in assignments:
        if assignment.complaint_id not in complaint_ids and _assignment_for(worker_id, assignment.complaint_id):
            complaint_ids.append(assignment.complaint_id)
    if not complaint_ids:
        return []
    query = Complaint.query.filter(Complaint.id.in_(complaint_ids))
    if statuses:
        query = query.filter(Complaint.status.in_(statuses))
    return query.order_by(Complaint.updated_at.desc(), Complaint.created_at.desc()).all()


@worker_bp.route('/dashboard', methods=['GET'])
@role_required('Worker')
def dashboard():
    worker = _current_worker()
    tasks = _worker_tasks(worker.id)
    active = [task for task in tasks if task.status in OPEN_STATUSES]
    completed = [task for task in tasks if task.status in FINAL_STATUSES]
    emergency = [task for task in active if task.priority == 'Emergency']
    return jsonify(success=True, dashboard={
        'worker': {'id': worker.id, 'name': worker.name, 'department': worker.member_department.department_name if worker.member_department else None},
        'counts': {'total': len(tasks), 'active': len(active), 'in_progress': sum(t.status == 'In Progress' for t in active), 'completed': len(completed), 'emergency': len(emergency)},
        'current_task': _serialize_task(active[0], True) if active else None,
        'assigned_tasks': [_serialize_task(task) for task in active[:8]],
        'emergencies': [_serialize_task(task) for task in emergency],
    }), 200


@worker_bp.route('/tasks', methods=['GET'])
@role_required('Worker')
def list_tasks():
    worker = _current_worker()
    status = request.args.get('status', 'active').strip()
    statuses = None if status == 'all' else FINAL_STATUSES if status == 'completed' else OPEN_STATUSES
    tasks = _worker_tasks(worker.id, statuses)
    search = request.args.get('search', '').strip().lower()
    if search:
        tasks = [task for task in tasks if search in task.title.lower() or search in task.category.lower()]
    return jsonify(success=True, tasks=[_serialize_task(task) for task in tasks]), 200


@worker_bp.route('/tasks/<int:complaint_id>', methods=['GET'])
@role_required('Worker')
def get_task(complaint_id):
    worker = _current_worker()
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return jsonify(message='Task not found.'), 404
    if not _assignment_for(worker.id, complaint_id):
        return jsonify(message='This task is not assigned to you.'), 403
    return jsonify(success=True, task=_serialize_task(complaint, True)), 200


@worker_bp.route('/tasks/<int:complaint_id>/status', methods=['PATCH'])
@role_required('Worker')
def update_task_status(complaint_id):
    worker = _current_worker()
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return jsonify(message='Task not found.'), 404
    if not _assignment_for(worker.id, complaint_id):
        return jsonify(message='This task is not assigned to you.'), 403
    if complaint.status in FINAL_STATUSES:
        return jsonify(message='A completed task cannot be updated.'), 400

    data = request.get_json(silent=True) or {}
    new_status = data.get('status')
    if new_status not in ('In Progress', 'Resolved'):
        return jsonify(message='Workers can only set a task to In Progress or Resolved.'), 400
    remark = (data.get('remark') or data.get('notes') or '').strip()
    if new_status == 'Resolved' and not remark:
        return jsonify(message='A resolution note is required when completing a task.'), 400
    if new_status == complaint.status:
        return jsonify(message=f'Task is already {new_status}.'), 400

    old_status = complaint.status
    complaint.status = new_status
    db.session.add(StatusLog(complaint_id=complaint.id, old_status=old_status, new_status=new_status, remark=remark or None))
    db.session.add(Notification(user_id=complaint.created_by, complaint_id=complaint.id,
        title='Complaint Resolved' if new_status == 'Resolved' else 'Work Started',
        message=f'Your complaint "{complaint.title}" is now {new_status}.', type='resolved' if new_status == 'Resolved' else 'status_updated'))
    if complaint.assigned_officer:
        db.session.add(Notification(user_id=complaint.assigned_officer, complaint_id=complaint.id,
            title='Worker Task Update', message=f'{worker.name} changed CMP-{complaint.id:05d} to {new_status}.', type='status_updated'))
    log_activity(worker.id, 'task_completed' if new_status == 'Resolved' else 'complaint_status_updated',
                 f'Updated CMP-{complaint.id:05d} to {new_status}.', complaint_id=complaint.id)
    db.session.commit()
    return jsonify(success=True, message='Task updated.', task=_serialize_task(complaint, True)), 200


@worker_bp.route('/tasks/<int:complaint_id>/photos', methods=['POST'])
@role_required('Worker')
def upload_task_photo(complaint_id):
    worker = _current_worker()
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return jsonify(message='Task not found.'), 404
    if not _assignment_for(worker.id, complaint_id):
        return jsonify(message='This task is not assigned to you.'), 403
    try:
        image_url = _save_uploaded_image(request.files.get('image'))
    except ValueError as error:
        return jsonify(message=str(error)), 400
    if not image_url:
        return jsonify(message='An image is required.'), 400
    db.session.add(ComplaintImages(complaint_id=complaint.id, image_url=image_url))
    log_activity(worker.id, 'complaint_status_updated', f'Added a work photo to CMP-{complaint.id:05d}.', complaint_id=complaint.id)
    db.session.commit()
    return jsonify(success=True, image_url=image_url), 201


@worker_bp.route('/notifications', methods=['GET'])
@role_required('Worker')
def list_notifications():
    worker = _current_worker()
    notes = Notification.query.filter_by(user_id=worker.id).order_by(Notification.created_at.desc()).all()
    return jsonify(success=True, notifications=[{'id': note.id, 'title': note.title, 'message': note.message, 'type': note.type, 'is_read': note.is_read, 'complaint_id': note.complaint_id, 'created_at': note.created_at.isoformat()} for note in notes]), 200


@worker_bp.route('/notifications/<int:notification_id>/read', methods=['PATCH'])
@role_required('Worker')
def mark_notification_read(notification_id):
    worker = _current_worker()
    note = Notification.query.filter_by(id=notification_id, user_id=worker.id).first()
    if not note:
        return jsonify(message='Notification not found.'), 404
    note.is_read = True
    db.session.commit()
    return jsonify(success=True), 200


@worker_bp.route('/notifications/read-all', methods=['PATCH'])
@role_required('Worker')
def mark_all_notifications_read():
    worker = _current_worker()
    Notification.query.filter_by(user_id=worker.id, is_read=False).update({'is_read': True})
    db.session.commit()
    return jsonify(success=True), 200


@worker_bp.route('/profile', methods=['GET'])
@role_required('Worker')
def get_profile():
    worker = _current_worker()
    return jsonify(success=True, profile={
        'id': worker.id, 'name': worker.name, 'email': worker.email, 'phone': worker.phone,
        'address': worker.address, 'city': worker.city, 'state': worker.state,
        'pincode': worker.pincode, 'designation': worker.designation,
        'profile_photo': worker.profile_photo,
        'department': worker.member_department.department_name if worker.member_department else None,
    }), 200


@worker_bp.route('/profile', methods=['PUT'])
@role_required('Worker')
def update_profile():
    worker = _current_worker()
    data = request.get_json(silent=True) or {}
    for field in ('name', 'phone', 'address', 'city', 'state', 'pincode'):
        if field in data:
            value = str(data[field]).strip()
            if field == 'name' and not value:
                return jsonify(message='Name cannot be empty.'), 400
            setattr(worker, field, value or None)
    log_activity(worker.id, 'profile_updated', 'Updated worker profile.')
    db.session.commit()
    return get_profile()
