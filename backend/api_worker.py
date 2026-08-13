import json

from flask import Blueprint, jsonify, request  # type: ignore
from flask_jwt_extended import get_jwt_identity  # type: ignore

from models import (
    db, Assignment, Complaint, ComplaintImages, Notification, StatusLog, User,
    Feedback, ActivityLog, Department, DepartmentApplication
)
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
        'updated_at': complaint.updated_at.isoformat() if complaint.updated_at else None,
    }
    if complaint.status in FINAL_STATUSES:
        feedback = Feedback.query.filter_by(complaint_id=complaint.id).first()
        data['rating'] = feedback.rating if feedback else None
        data['feedback_comment'] = feedback.comments if feedback else None
        if include_full and feedback:
            data['feedback'] = {
                'rating':          feedback.rating,
                'service_ratings': json.loads(feedback.service_ratings) if feedback.service_ratings else {},
                'categories':      json.loads(feedback.categories) if feedback.categories else [],
                'comment':         feedback.comments,
                'improvement':     feedback.improvement,
                'would_recommend': feedback.would_recommend,
                'is_anonymous':    feedback.is_anonymous,
                'submitted_at':    feedback.submitted_at.isoformat() if feedback.submitted_at else None,
            }
        elif include_full:
            data['feedback'] = None
    if include_full:
        data.update({
            'description': complaint.description,
            'department': complaint.department,
            'city': complaint.city,
            'ward': complaint.ward,
            'street': complaint.street,
            'landmark': complaint.landmark,
            'officer_phone': officer.phone if officer else None,
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
    dept = worker.member_department

    last_login = (
        ActivityLog.query
        .filter(ActivityLog.user_id == worker.id, ActivityLog.activity_type == 'login')
        .order_by(ActivityLog.created_at.desc())
        .first()
    )

    completed_tasks = _worker_tasks(worker.id, FINAL_STATUSES)
    completed_count = len(completed_tasks)

    resolved_rows = [t for t in completed_tasks if t.updated_at and t.created_at]
    if resolved_rows:
        total_seconds = sum((t.updated_at - t.created_at).total_seconds() for t in resolved_rows)
        avg_completion_hours = round((total_seconds / len(resolved_rows)) / 3600, 1)
    else:
        avg_completion_hours = None

    rating_avg = (
        db.session.query(db.func.avg(Feedback.rating))
        .join(Complaint, Feedback.complaint_id == Complaint.id)
        .join(Assignment, Assignment.complaint_id == Complaint.id)
        .filter(Assignment.worker_id == worker.id)
        .scalar()
    )
    avg_rating = round(float(rating_avg), 1) if rating_avg is not None else None

    return jsonify(
        success=True,
        profile={
            'id': worker.id,
            'name': worker.name,
            'email': worker.email,
            'phone': worker.phone,
            'address': worker.address,
            'city': worker.city,
            'state': worker.state,
            'pincode': worker.pincode,
            'gender': worker.gender,
            'dob': worker.dob.strftime('%Y-%m-%d') if worker.dob else None,
            'nationality': worker.nationality,
            'emergencyContact': worker.emergency_contact,
            'designation': worker.designation,
            'profile_photo': worker.profile_photo,
            'department': dept.department_name if dept else None,
            'empId': f'FW-{worker.id:04d}',
            'memberSince': worker.created_at.strftime('%B %d, %Y') if worker.created_at else None,
            'lastLogin': last_login.created_at.strftime('%b %d, %Y %I:%M %p') if last_login else None,
            'completedCount': completed_count,
            'avgCompletionHours': avg_completion_hours,
            'avgRating': avg_rating,
        }
    ), 200


@worker_bp.route('/profile', methods=['PUT'])
@role_required('Worker')
def update_profile():
    worker = _current_worker()
    data = request.get_json(silent=True) or {}
    for field in ('name', 'phone', 'address', 'city', 'state', 'pincode', 'gender', 'nationality'):
        if field in data:
            value = str(data[field]).strip()
            if field == 'name' and not value:
                return jsonify(message='Name cannot be empty.'), 400
            setattr(worker, field, value or None)
    if 'emergencyContact' in data:
        worker.emergency_contact = str(data['emergencyContact']).strip() or None
    if 'dob' in data and data['dob']:
        from datetime import datetime
        try:
            worker.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify(message='DOB must be in YYYY-MM-DD format.'), 400
    log_activity(worker.id, 'profile_updated', 'Updated worker profile.')
    db.session.commit()
    return get_profile()


@worker_bp.route('/profile/photo', methods=['POST'])
@role_required('Worker')
def upload_profile_photo():
    worker = _current_worker()
    if 'photo' not in request.files:
        return jsonify(message='No photo file was provided.'), 400
    try:
        photo_url = _save_uploaded_image(request.files['photo'])
    except ValueError as error:
        return jsonify(message=str(error)), 400
    if not photo_url:
        return jsonify(message='No photo file was provided.'), 400
    worker.profile_photo = photo_url
    log_activity(worker.id, 'profile_photo_updated', 'Updated profile photo.')
    db.session.commit()
    return jsonify(success=True, profilePhoto=photo_url), 200


@worker_bp.route('/profile/photo', methods=['DELETE'])
@role_required('Worker')
def delete_profile_photo():
    worker = _current_worker()
    worker.profile_photo = None
    log_activity(worker.id, 'profile_photo_removed', 'Removed profile photo.')
    db.session.commit()
    return jsonify(success=True), 200


# ─────────────────────────────────────────────────────────────────────────
# Department Applications — a worker requesting to transfer into a
# different department. Reviewed by Admin.
# ─────────────────────────────────────────────────────────────────────────
def _serialize_department_application(app):
    return {
        'id': app.id,
        'departmentId': app.department_id,
        'departmentName': app.department.department_name if app.department else None,
        'departmentCode': app.department.code if app.department else None,
        'status': app.status,
        'message': app.message,
        'remark': app.remark,
        'appliedAt': app.applied_at.isoformat() if app.applied_at else None,
        'reviewedAt': app.reviewed_at.isoformat() if app.reviewed_at else None,
    }


def _worker_has_ongoing_task(worker_id):
    """A worker with an active (Assigned/In Progress) task must finish or
    hand it off before switching departments."""
    return len(_worker_tasks(worker_id, OPEN_STATUSES)) > 0


@worker_bp.route('/departments', methods=['GET'])
@role_required('Worker')
def list_departments():
    worker = _current_worker()
    departments = Department.query.filter_by(status='Active').order_by(Department.department_name).all()
    can_apply = not _worker_has_ongoing_task(worker.id)

    # This worker's most recent application per department, so the UI can
    # show Not Applied / Pending / Approved / Rejected / Withdrawn per card.
    my_apps = DepartmentApplication.query.filter_by(worker_id=worker.id).order_by(
        DepartmentApplication.applied_at.desc()
    ).all()
    latest_by_dept = {}
    for app in my_apps:
        if app.department_id not in latest_by_dept:
            latest_by_dept[app.department_id] = app

    result = []
    for dept in departments:
        head = User.query.get(dept.user_id) if dept.user_id else None
        worker_count = User.query.filter_by(department_id=dept.id, role='Worker').count()
        is_current = dept.id == worker.department_id
        my_app = latest_by_dept.get(dept.id)
        result.append({
            'id': dept.id,
            'name': dept.department_name,
            'code': dept.code,
            'description': dept.description,
            'head': head.name if head else None,
            'workerCount': worker_count,
            'isCurrentDepartment': is_current,
            'applicationStatus': 'Current' if is_current else (my_app.status if my_app and my_app.status == 'Pending' else 'Not Applied'),
            'application': _serialize_department_application(my_app) if my_app and my_app.status == 'Pending' else None,
        })
    return jsonify(success=True, departments=result, canApply=can_apply), 200


@worker_bp.route('/department-applications', methods=['GET'])
@role_required('Worker')
def list_my_department_applications():
    worker = _current_worker()
    apps = DepartmentApplication.query.filter_by(worker_id=worker.id).order_by(
        DepartmentApplication.applied_at.desc()
    ).all()
    return jsonify(success=True, applications=[_serialize_department_application(a) for a in apps]), 200


@worker_bp.route('/department-applications', methods=['POST'])
@role_required('Worker')
def apply_to_department():
    worker = _current_worker()
    data = request.get_json(silent=True) or {}
    department_id = data.get('departmentId')
    if not department_id:
        return jsonify(message='departmentId is required.'), 400

    dept = Department.query.get(int(department_id))
    if not dept or dept.status != 'Active':
        return jsonify(message='Department not found.'), 404
    if dept.id == worker.department_id:
        return jsonify(message='You are already in this department.'), 400
    if _worker_has_ongoing_task(worker.id):
        return jsonify(message='You cannot apply to a new department while you have an ongoing task. Finish or hand off your current task first.'), 400

    existing = DepartmentApplication.query.filter_by(
        worker_id=worker.id, department_id=dept.id, status='Pending'
    ).first()
    if existing:
        return jsonify(message='You already have a pending application to this department.'), 400

    message = (data.get('message') or '').strip()[:500] or None
    application = DepartmentApplication(worker_id=worker.id, department_id=dept.id, message=message)
    db.session.add(application)
    db.session.flush()

    log_activity(worker.id, 'department_application_submitted',
                 f'Applied to join {dept.department_name}.')

    for admin in User.query.filter_by(role='Admin', status='active').all():
        db.session.add(Notification(
            user_id=admin.id,
            title='New Department Application',
            message=f'{worker.name} applied to join {dept.department_name}.',
            type='system'
        ))

    db.session.commit()
    return jsonify(success=True, application=_serialize_department_application(application)), 201


@worker_bp.route('/department-applications/<int:application_id>', methods=['DELETE'])
@role_required('Worker')
def withdraw_department_application(application_id):
    worker = _current_worker()
    application = DepartmentApplication.query.filter_by(id=application_id, worker_id=worker.id).first()
    if not application:
        return jsonify(message='Application not found.'), 404
    if application.status != 'Pending':
        return jsonify(message='Only a pending application can be withdrawn.'), 400

    application.status = 'Withdrawn'
    application.reviewed_at = None
    log_activity(worker.id, 'department_application_withdrawn',
                 f'Withdrew application to {application.department.department_name}.')
    db.session.commit()
    return jsonify(success=True), 200