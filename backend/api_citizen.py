import json
import os
import uuid
from datetime import datetime, timedelta

from flask import Blueprint, current_app, jsonify, request # type: ignore
from flask_jwt_extended import get_jwt_identity # type: ignore
from werkzeug.utils import secure_filename # type: ignore

from models import db, User, Complaint, StatusLog, ComplaintImages, Feedback, Notification, ActivityLog, now_ist
from api_auth_utils import log_activity, role_required, is_valid_email
from mail import send_complaint_submitted_email

citizen_bp = Blueprint('citizen', __name__, url_prefix='/api/citizen')


# ─────────────────────────────────────────────────────────────────────────
# Category -> Department mapping. There's no department-selection field on
# the submit form, so the department is inferred from the chosen category.
# Adjust freely if your real department list differs.
# ─────────────────────────────────────────────────────────────────────────
CATEGORY_DEPARTMENT_MAP = {
    'Garbage Collection':        'Sanitation Department',
    'Overflowing Dustbin':       'Sanitation Department',
    'Illegal Waste Dumping':     'Sanitation Department',
    'Potholes':                  'Roads & Infrastructure',
    'Road Damage':               'Roads & Infrastructure',
    'Public Property Damage':    'Roads & Infrastructure',
    'Broken Streetlight':        'Electrical Department',
    'Water Leakage':             'Water & Drainage Department',
    'Blocked Drainage':          'Water & Drainage Department',
    'Other':                     'General Administration',
}
VALID_CATEGORIES = set(CATEGORY_DEPARTMENT_MAP.keys())
VALID_PRIORITIES = {'Low', 'Medium', 'High', 'Emergency'}

ALLOWED_IMAGE_TYPES = {'.png', '.jpg', '.jpeg'}
MAX_IMAGE_BYTES = 5 * 1024 * 1024

def _save_uploaded_image(file_storage):
    """Saves an uploaded complaint/feedback image to disk and returns the
    public URL path to store in the DB. Returns None if no file given."""
    if not file_storage or not file_storage.filename:
        return None

    ext = os.path.splitext(file_storage.filename)[1].lower()
    if ext not in ALLOWED_IMAGE_TYPES:
        raise ValueError('Only PNG, JPG, and JPEG images are allowed.')

    file_storage.seek(0, os.SEEK_END)
    size = file_storage.tell()
    file_storage.seek(0)
    if size > MAX_IMAGE_BYTES:
        raise ValueError('Image exceeds the 5MB size limit.')

    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}{ext}"
    filename = secure_filename(filename)
    file_storage.save(os.path.join(upload_dir, filename))

    return f"/api/uploads/{filename}"


def _create_notification(user_id, title, message, complaint_id=None, ntype='info'):
    note = Notification(
        user_id=user_id,
        complaint_id=complaint_id,
        title=title,
        message=message,
        type=ntype
    )
    db.session.add(note)


def _serialize_complaint(c, include_full=False):
    officer = User.query.get(c.assigned_officer) if c.assigned_officer else None
    latest_assignment = max(c.assignments, key=lambda a: a.assigned_at, default=None)
    worker = User.query.get(latest_assignment.worker_id) if latest_assignment else None

    data = {
        "id":         f"CMP-{c.id:05d}",
        "raw_id":     c.id,
        "title":      c.title,
        "category":   c.category,
        "priority":   c.priority,
        "department": c.department,
        "status":     c.status,
        "location":   c.location,
        "created_at": c.created_at.isoformat() if c.created_at else None,
        "updated_at": c.updated_at.isoformat() if c.updated_at else None,
        "has_feedback": c.feedback is not None,
        "officer":    {"name": officer.name} if officer else None,
        "worker":     {"name": worker.name} if worker else None,
    }
    if include_full:
        data.update({
            "description":   c.description,
            "city":          c.city,
            "ward":          c.ward,
            "area":          c.area,
            "street":        c.street,
            "landmark":      c.landmark,
            "incident_date": c.incident_date.isoformat() if c.incident_date else None,
            "visit_time":    c.visit_time,
            "urgency_note":  c.urgency_note,
            "is_escalated":  c.is_escalated,
            "images":        [img.image_url for img in c.images],
        })
    return data


# ─────────────────────────────────────────────────────────────────────────
# Submit a new complaint. Accepts multipart/form-data so an image can be
# attached in the same request.
# ─────────────────────────────────────────────────────────────────────────
@citizen_bp.route('/complaints', methods=['POST'])
@role_required('Citizen')
def submit_complaint():
    user_id = int(get_jwt_identity())
    citizen = User.query.get(user_id)

    # multipart/form-data puts regular fields in request.form, not request.json
    form = request.form

    title       = form.get('title', '').strip()
    category    = form.get('category', '').strip()
    priority    = form.get('priority', 'Medium').strip()
    description = form.get('description', '').strip()
    city        = form.get('city', '').strip()
    ward        = form.get('ward', '').strip()
    area        = form.get('area', '').strip()
    street      = form.get('street', '').strip()
    landmark    = form.get('landmark', '').strip()
    incident_date_raw = form.get('incidentDate', '').strip()
    visit_time  = form.get('visitTime', '').strip()
    urgency_note = form.get('urgencyNote', '').strip()

    # ── validation (mirrors SubmitComplaint.vue's validateForm()) ─────────
    if not title:
        return jsonify(message="Title is required."), 400
    if category not in VALID_CATEGORIES:
        return jsonify(message=f"Invalid category. Choose from: {', '.join(sorted(VALID_CATEGORIES))}."), 400
    if priority not in VALID_PRIORITIES:
        return jsonify(message=f"Invalid priority. Choose from: {', '.join(sorted(VALID_PRIORITIES))}."), 400
    if len(description) < 30:
        return jsonify(message="Description must be at least 30 characters."), 400
    if not ward:
        return jsonify(message="Ward number is required."), 400
    if not area:
        return jsonify(message="Area/Locality is required."), 400
    if not street:
        return jsonify(message="Street name is required."), 400

    incident_date = None
    if incident_date_raw:
        try:
            incident_date = datetime.strptime(incident_date_raw, '%Y-%m-%d').date()
        except ValueError:
            return jsonify(message="Invalid incident date format, expected YYYY-MM-DD."), 400

    # ── handle optional image upload ───────────────────────────────────────
    image_url = None
    if 'image' in request.files:
        try:
            image_url = _save_uploaded_image(request.files['image'])
        except ValueError as e:
            return jsonify(message=str(e)), 400

    department = CATEGORY_DEPARTMENT_MAP.get(category, 'General Administration')
    location_summary = ", ".join(p for p in [street, area, f"Ward {ward}", city] if p)

    complaint = Complaint(
        title=title,
        category=category,
        description=description,
        priority=priority,
        department=department,
        location=location_summary,
        city=city or None,
        ward=ward,
        area=area,
        street=street,
        landmark=landmark or None,
        incident_date=incident_date,
        visit_time=visit_time or None,
        urgency_note=urgency_note or None,
        created_by=user_id,
        status='Pending'
    )
    db.session.add(complaint)
    db.session.flush()
    
    if image_url:
        db.session.add(ComplaintImages(complaint_id=complaint.id, image_url=image_url))

    db.session.add(StatusLog(
        complaint_id=complaint.id,
        old_status=None,
        new_status='Pending',
        remark='Complaint submitted by citizen.'
    ))

    _create_notification(
        user_id=user_id,
        title='Complaint Submitted',
        message=f'Your complaint "{title}" has been submitted and is awaiting review.',
        complaint_id=complaint.id,
        ntype='submitted'
    )

    log_activity(
        user_id, 'complaint_submitted',
        f'Submitted complaint "{title}".',
        complaint_id=complaint.id
    )

    db.session.commit()

    if citizen:
        send_complaint_submitted_email(
            to_email=citizen.email,
            name=citizen.name,
            complaint_id=f"CMP-{complaint.id:05d}",
            title=title,
            category=category
        )

    return jsonify(
        success=True,
        message="Complaint submitted successfully.",
        complaint=_serialize_complaint(complaint)
    ), 201


# ─────────────────────────────────────────────────────────────────────────
# List the logged-in citizen's own complaints. Supports ?status= and
# ?search= query params, matching MyComplaints.vue's filter bar.
# ─────────────────────────────────────────────────────────────────────────
@citizen_bp.route('/complaints', methods=['GET'])
@role_required('Citizen')
def list_complaints():
    user_id = int(get_jwt_identity())

    query = Complaint.query.filter_by(created_by=user_id)

    status = request.args.get('status', 'All')
    if status and status != 'All':
        query = query.filter_by(status=status)

    search = request.args.get('search', '').strip()
    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(Complaint.title.ilike(like), Complaint.category.ilike(like))
        )

    complaints = query.order_by(Complaint.created_at.desc()).all()

    return jsonify(
        success=True,
        complaints=[_serialize_complaint(c) for c in complaints]
    ), 200


# ─────────────────────────────────────────────────────────────────────────
# Summary counts for MyComplaints.vue's stat cards and Dashboard.vue.
# ─────────────────────────────────────────────────────────────────────────
@citizen_bp.route('/complaints/summary', methods=['GET'])
@role_required('Citizen')
def complaints_summary():
    user_id = int(get_jwt_identity())
    base = Complaint.query.filter_by(created_by=user_id)

    return jsonify(
        success=True,
        summary={
            "total":         base.count(),
            "pending":       base.filter_by(status='Pending').count(),
            "under_review":  base.filter_by(status='Under Review').count(),
            "assigned":      base.filter_by(status='Assigned').count(),
            "in_progress":   base.filter_by(status='In Progress').count(),
            "resolved":      base.filter_by(status='Resolved').count(),
            "closed":        base.filter_by(status='Closed').count(),
        }
    ), 200


# ─────────────────────────────────────────────────────────────────────────
# Full details for one complaint. Ownership-checked: a citizen can only
# view their own complaints, even with a valid complaint ID.
# ─────────────────────────────────────────────────────────────────────────
@citizen_bp.route('/complaints/<int:complaint_id>', methods=['GET'])
@role_required('Citizen')
def get_complaint(complaint_id):
    user_id = int(get_jwt_identity())
    complaint = Complaint.query.get(complaint_id)

    if not complaint:
        return jsonify(message="Complaint not found."), 404
    if complaint.created_by != user_id:
        return jsonify(message="You do not have access to this complaint."), 403

    return jsonify(success=True, complaint=_serialize_complaint(complaint, include_full=True)), 200


# ─────────────────────────────────────────────────────────────────────────
# Tracking view: current status + the real status-change history.
# ─────────────────────────────────────────────────────────────────────────
@citizen_bp.route('/complaints/<int:complaint_id>/tracking', methods=['GET'])
@role_required('Citizen')
def track_complaint(complaint_id):
    user_id = int(get_jwt_identity())
    complaint = Complaint.query.get(complaint_id)

    if not complaint:
        return jsonify(message="Complaint not found."), 404
    if complaint.created_by != user_id:
        return jsonify(message="You do not have access to this complaint."), 403

    logs = StatusLog.query.filter_by(complaint_id=complaint_id).order_by(StatusLog.changed_at.asc()).all()

    return jsonify(
        success=True,
        complaint=_serialize_complaint(complaint),
        activity_log=[
            {
                "old_status": log.old_status,
                "new_status": log.new_status,
                "remark":     log.remark,
                "changed_at": log.changed_at.isoformat() if log.changed_at else None
            }
            for log in logs
        ]
    ), 200


# ─────────────────────────────────────────────────────────────────────────
# Submit feedback for a resolved complaint. One feedback per complaint
# ─────────────────────────────────────────────────────────────────────────
@citizen_bp.route('/complaints/<int:complaint_id>/feedback', methods=['POST'])
@role_required('Citizen')
def submit_feedback(complaint_id):
    user_id = int(get_jwt_identity())
    complaint = Complaint.query.get(complaint_id)

    if not complaint:
        return jsonify(message="Complaint not found."), 404
    if complaint.created_by != user_id:
        return jsonify(message="You do not have access to this complaint."), 403
    if complaint.status != 'Resolved':
        return jsonify(message="Feedback can only be submitted for resolved complaints."), 400
    if complaint.feedback is not None:
        return jsonify(message="Feedback has already been submitted for this complaint."), 409

    data = request.get_json()
    if not data:
        return jsonify(message="Request body must be JSON."), 400

    overall_rating = data.get('overallRating', 0)
    comment        = data.get('comment', '').strip()
    improvement    = data.get('improvement', '').strip()
    recommend      = data.get('recommend', '').strip()
    categories     = data.get('categories', [])
    service_ratings = data.get('serviceRatings', {})
    anonymous      = bool(data.get('anonymous', False))

    if not isinstance(overall_rating, int) or not (1 <= overall_rating <= 5):
        return jsonify(message="Overall rating must be an integer from 1 to 5."), 400
    if len(comment) < 20:
        return jsonify(message="Comment must be at least 20 characters."), 400
    if len(comment) > 1000:
        return jsonify(message="Comment cannot exceed 1000 characters."), 400
    if recommend and recommend not in {'Yes', 'No', 'Maybe'}:
        return jsonify(message="Recommend must be one of: Yes, No, Maybe."), 400

    feedback = Feedback(
        complaint_id=complaint_id,
        rating=overall_rating,
        service_ratings=json.dumps(service_ratings) if service_ratings else None,
        categories=json.dumps(categories) if categories else None,
        comments=comment,
        improvement=improvement or None,
        would_recommend=recommend or None,
        is_anonymous=anonymous
    )
    db.session.add(feedback)

    log_activity(
        user_id, 'feedback_submitted',
        f'Submitted feedback for complaint CMP-{complaint_id:05d}.',
        complaint_id=complaint_id
    )

    db.session.commit()

    return jsonify(success=True, message="Thank you! Your feedback has been submitted."), 201


# ─────────────────────────────────────────────────────────────────────────
# Fetch the feedback already submitted for one complaint.
# ─────────────────────────────────────────────────────────────────────────
@citizen_bp.route('/complaints/<int:complaint_id>/feedback', methods=['GET'])
@role_required('Citizen')
def get_feedback(complaint_id):
    user_id = int(get_jwt_identity())
    complaint = Complaint.query.get(complaint_id)

    if not complaint:
        return jsonify(message="Complaint not found."), 404
    if complaint.created_by != user_id:
        return jsonify(message="You do not have access to this complaint."), 403
    if complaint.feedback is None:
        return jsonify(message="No feedback has been submitted for this complaint."), 404

    fb = complaint.feedback
    return jsonify(
        success=True,
        feedback={
            "rating":          fb.rating,
            "service_ratings": json.loads(fb.service_ratings) if fb.service_ratings else {},
            "categories":      json.loads(fb.categories) if fb.categories else [],
            "comment":         fb.comments,
            "improvement":     fb.improvement,
            "would_recommend": fb.would_recommend,
            "is_anonymous":    fb.is_anonymous,
            "submitted_at":    fb.submitted_at.isoformat() if fb.submitted_at else None
        }
    ), 200


# ─────────────────────────────────────────────────────────────────────────
# Past feedback the citizen has submitted, for Feedback.vue's sidebar.
# ─────────────────────────────────────────────────────────────────────────
@citizen_bp.route('/feedback', methods=['GET'])
@role_required('Citizen')
def list_feedback():
    user_id = int(get_jwt_identity())

    rows = (
        db.session.query(Feedback, Complaint)
        .join(Complaint, Feedback.complaint_id == Complaint.id)
        .filter(Complaint.created_by == user_id)
        .order_by(Feedback.submitted_at.desc())
        .all()
    )

    return jsonify(
        success=True,
        feedback=[
            {
                "complaint_id": f"CMP-{c.id:05d}",
                "rating":       fb.rating,
                "comment":      fb.comments,
                "submitted_at": fb.submitted_at.isoformat() if fb.submitted_at else None
            }
            for fb, c in rows
        ]
    ), 200


# ─────────────────────────────────────────────────────────────────────────
# Notifications inbox.
# ─────────────────────────────────────────────────────────────────────────
@citizen_bp.route('/notifications', methods=['GET'])
@role_required('Citizen')
def list_notifications():
    user_id = int(get_jwt_identity())
    notes = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()

    return jsonify(
        success=True,
        summary={
            "all":    len(notes),
            "unread": sum(1 for n in notes if not n.is_read),
            "read":   sum(1 for n in notes if n.is_read),
        },
        notifications=[
            {
                "id":           n.id,
                "title":        n.title,
                "message":      n.message,
                "type":         n.type,
                "complaint_id": f"CMP-{n.complaint_id:05d}" if n.complaint_id else None,
                "is_read":      n.is_read,
                "created_at":   n.created_at.isoformat() if n.created_at else None
            }
            for n in notes
        ]
    ), 200


@citizen_bp.route('/notifications/<int:notification_id>/read', methods=['PATCH'])
@role_required('Citizen')
def mark_notification_read(notification_id):
    user_id = int(get_jwt_identity())
    note = Notification.query.get(notification_id)

    if not note or note.user_id != user_id:
        return jsonify(message="Notification not found."), 404

    note.is_read = True
    db.session.commit()
    return jsonify(success=True), 200


@citizen_bp.route('/notifications/read-all', methods=['PATCH'])
@role_required('Citizen')
def mark_all_notifications_read():
    user_id = int(get_jwt_identity())
    Notification.query.filter_by(user_id=user_id, is_read=False).update({"is_read": True})
    db.session.commit()
    return jsonify(success=True), 200


# ─────────────────────────────────────────────────────────────────────────
# Recent Activity feed
# ─────────────────────────────────────────────────────────────────────────
@citizen_bp.route('/activity', methods=['GET'])
@role_required('Citizen')
def list_activity():
    user_id = int(get_jwt_identity())

    try:
        limit = int(request.args.get('limit', 20))
    except ValueError:
        limit = 20
    limit = max(1, min(limit, 100))

    query = ActivityLog.query.filter_by(user_id=user_id)

    activity_type = request.args.get('type', '').strip()
    if activity_type:
        query = query.filter_by(activity_type=activity_type)

    rows = query.order_by(ActivityLog.created_at.desc()).limit(limit).all()

    return jsonify(
        success=True,
        activity=[
            {
                "id":            a.id,
                "type":          a.activity_type,
                "description":   a.description,
                "complaint_id":  f"CMP-{a.complaint_id:05d}" if a.complaint_id else None,
                "created_at":    a.created_at.isoformat() if a.created_at else None
            }
            for a in rows
        ]
    ), 200


# ─────────────────────────────────────────────────────────────────────────
# Profile — extends /api/me with the address/city/state/pincode/gender
# fields Profile.vue needs that the general auth endpoint doesn't return.
# ─────────────────────────────────────────────────────────────────────────
@citizen_bp.route('/profile', methods=['GET'])
@role_required('Citizen')
def get_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    last_login = (
        ActivityLog.query
        .filter(
            ActivityLog.user_id == user.id,
            ActivityLog.activity_type == "login"
        )
        .order_by(ActivityLog.created_at.desc())
        .first()
    )
    return jsonify(
        success=True,
        profile={
            "id":         user.id,
            "fullName":   user.name,
            "email":      user.email,
            "mobile":     user.phone,
            "address":    user.address,
            "city":       user.city,
            "state":      user.state,
            "pincode":    user.pincode,
            "gender":     user.gender,
            "dob":        user.dob.isoformat() if user.dob else None,
            "nationality": user.nationality,
            "emergencyContact": user.emergency_contact,
            "recoveryEmail":    user.recovery_email,
            "profilePhoto": user.profile_photo,
            "accountId":  f"CVC-USR-{user.id:04d}",
            "memberSince": user.created_at.strftime('%B %d, %Y') if user.created_at else None,
            "lastLogin": last_login.created_at.strftime('%b %d, %Y %I:%M %p') if last_login else None
        }
    ), 200


@citizen_bp.route('/profile', methods=['PUT'])
@role_required('Citizen')
def update_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    data = request.get_json()
    if not data:
        return jsonify(message="Request body must be JSON."), 400

    full_name = data.get('fullName', '').strip()
    email     = data.get('email', '').strip().lower()
    mobile    = data.get('mobile', '').strip()
    address   = data.get('address', '').strip()
    city      = data.get('city', '').strip()
    state     = data.get('state', '').strip()
    pincode   = data.get('pincode', '').strip()
    gender    = data.get('gender', '').strip()
    dob_str          = data.get('dob', '').strip()
    nationality      = data.get('nationality', '').strip()
    emergency        = data.get('emergencyContact', '').strip()
    recovery_email   = data.get('recoveryEmail', '').strip().lower()

    if not full_name:
        return jsonify(message="Full Name is required."), 400
    if not mobile or not mobile.isdigit() or len(mobile) != 10:
        return jsonify(message="Enter a valid 10-digit mobile number."), 400
    if not address:
        return jsonify(message="Address is required."), 400
    if not city:
        return jsonify(message="City is required."), 400
    if not state:
        return jsonify(message="State is required."), 400
    if not pincode or not pincode.isdigit() or len(pincode) != 6:
        return jsonify(message="Enter a valid 6-digit pincode."), 400
    if emergency and (not emergency.isdigit() or len(emergency) != 10):
        return jsonify(message="Enter a valid 10-digit emergency contact number."), 400
    if recovery_email:
        if not is_valid_email(recovery_email):
            return jsonify(message="Enter a valid recovery email address."), 400
        if recovery_email == email or recovery_email == user.email:
            return jsonify(message="Recovery email must be different from your primary email."), 400

    dob = None
    if dob_str:
        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify(message="Date of birth must be in YYYY-MM-DD format."), 400
        if dob >= now_ist().date():
            return jsonify(message="Date of birth must be in the past."), 400

    if email and email != user.email:
        if User.query.filter(User.email == email, User.id != user_id).first():
            return jsonify(message="This email is already in use by another account."), 409
        user.email = email

    user.name    = full_name
    user.phone   = mobile
    user.address = address
    user.city    = city
    user.state   = state
    user.pincode = pincode
    if gender:
        user.gender = gender
    user.dob               = dob
    user.nationality        = nationality or None
    user.emergency_contact = emergency or None
    user.recovery_email    = recovery_email or None

    log_activity(user_id, 'profile_updated', 'Updated profile details.')
    db.session.commit()

    return jsonify(success=True, message="Profile updated successfully."), 200


# ─────────────────────────────────────────────────────────────────────────
# Profile photo — upload (replace) or remove the citizen's avatar.
# Reuses the same _save_uploaded_image() helper as complaint image uploads.
# ─────────────────────────────────────────────────────────────────────────
@citizen_bp.route('/profile/photo', methods=['POST'])
@role_required('Citizen')
def upload_profile_photo():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if 'photo' not in request.files:
        return jsonify(message="No photo file was provided."), 400

    try:
        photo_url = _save_uploaded_image(request.files['photo'])
    except ValueError as e:
        return jsonify(message=str(e)), 400

    if not photo_url:
        return jsonify(message="No photo file was provided."), 400

    user.profile_photo = photo_url
    log_activity(user_id, 'profile_photo_updated', 'Updated profile photo.')
    db.session.commit()

    return jsonify(success=True, profilePhoto=photo_url), 200


@citizen_bp.route('/profile/photo', methods=['DELETE'])
@role_required('Citizen')
def delete_profile_photo():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    user.profile_photo = None
    log_activity(user_id, 'profile_photo_removed', 'Removed profile photo.')
    db.session.commit()

    return jsonify(success=True), 200


# ─────────────────────────────────────────────────────────────────────────
# Dashboard summary: stats + recent complaints + recent
# notifications, in one call, matching what Dashboard.vue actually shows.
# ─────────────────────────────────────────────────────────────────────────
@citizen_bp.route('/dashboard', methods=['GET'])
@role_required('Citizen')
def dashboard():
    user_id = int(get_jwt_identity())
    base = Complaint.query.filter_by(created_by=user_id)

    recent = base.order_by(Complaint.created_at.desc()).limit(5).all()
    recent_notes = (
        Notification.query.filter_by(user_id=user_id)
        .order_by(Notification.created_at.desc())
        .limit(5)
        .all()
    )
    recent_activity = (
        ActivityLog.query.filter_by(user_id=user_id)
        .order_by(ActivityLog.created_at.desc())
        .limit(5)
        .all()
    )

    # A complaint needs feedback if it's Resolved and has no Feedback row yet.
    pending_feedback = (
        base.filter_by(status='Resolved')
        .filter(~Complaint.id.in_(db.session.query(Feedback.complaint_id)))
        .first()
    )

    # Category breakdown for the Dashboard's "Issues by Category" widget.
    category_counts = (
        db.session.query(Complaint.category, db.func.count(Complaint.id))
        .filter(Complaint.created_by == user_id)
        .group_by(Complaint.category)
        .all()
    )

    priority_counts = (
        db.session.query(Complaint.priority, db.func.count(Complaint.id))
        .filter(Complaint.created_by == user_id)
        .group_by(Complaint.priority)
        .all()
    )

    escalated_count = base.filter_by(is_escalated=True).count()

    resolved_rows = base.filter(
        Complaint.status.in_(['Resolved', 'Closed']),
        Complaint.updated_at.isnot(None)
    ).all()
    if resolved_rows:
        avg_resolution_days = round(
            sum((c.updated_at - c.created_at).total_seconds() for c in resolved_rows)
            / len(resolved_rows) / 86400, 1
        )
    else:
        avg_resolution_days = None

    total_count = base.count()
    resolved_or_closed_count = base.filter(Complaint.status.in_(['Resolved', 'Closed'])).count()
    resolution_rate = round((resolved_or_closed_count / total_count) * 100, 1) if total_count else 0.0

    # Avg. first response time: how long between submission and the first
    # status change made *by the department* (i.e. the first StatusLog row
    # that isn't the initial "submitted" entry). Gives citizens a sense of
    # how quickly their issue gets picked up, separate from full resolution time.
    first_response_hours = []
    for c in base.all():
        first_action = (
            StatusLog.query.filter_by(complaint_id=c.id)
            .filter(StatusLog.old_status.isnot(None))
            .order_by(StatusLog.changed_at.asc())
            .first()
        )
        if first_action and first_action.changed_at and c.created_at:
            first_response_hours.append((first_action.changed_at - c.created_at).total_seconds() / 3600)
    avg_first_response_hours = round(sum(first_response_hours) / len(first_response_hours), 1) if first_response_hours else None

    # Avg. rating the citizen has given across their own feedback submissions.
    rating_avg = (
        db.session.query(db.func.avg(Feedback.rating))
        .join(Complaint, Feedback.complaint_id == Complaint.id)
        .filter(Complaint.created_by == user_id)
        .scalar()
    )
    avg_rating = round(float(rating_avg), 1) if rating_avg is not None else None

    # Complaints that have sat open (not resolved/closed) for more than 7 days —
    # surfaced on the dashboard so citizens can spot stalled issues.
    OPEN_STATUSES = ['Pending', 'Under Review', 'Assigned', 'In Progress']
    aging_cutoff = now_ist() - timedelta(days=7)
    aging_open_count = base.filter(
        Complaint.status.in_(OPEN_STATUSES),
        Complaint.created_at < aging_cutoff
    ).count()
    oldest_aging_complaint = (
        base.filter(
            Complaint.status.in_(OPEN_STATUSES),
            Complaint.created_at < aging_cutoff
        )
        .order_by(Complaint.created_at.asc())
        .first()
    )

    now = now_ist()
    month_keys = []
    y, m = now.year, now.month
    for _ in range(6):
        month_keys.append((y, m))
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    month_keys.reverse()

    trend_counts = {key: 0 for key in month_keys}
    for c in base.all():
        if c.created_at:
            key = (c.created_at.year, c.created_at.month)
            if key in trend_counts:
                trend_counts[key] += 1

    monthly_trend = [
        {"month": datetime(y, m, 1).strftime('%b'), "count": trend_counts[(y, m)]}
        for (y, m) in month_keys
    ]

    return jsonify(
        success=True,
        category_breakdown={cat: count for cat, count in category_counts},
        priority_breakdown={pri: count for pri, count in priority_counts},
        monthly_trend=monthly_trend,
        summary={
            "total":       base.count(),
            "pending":     base.filter_by(status='Pending').count(),
            "under_review": base.filter_by(status='Under Review').count(),
            "assigned":    base.filter_by(status='Assigned').count(),
            "in_progress": base.filter_by(status='In Progress').count(),
            "resolved":    base.filter_by(status='Resolved').count(),
            "closed":      base.filter_by(status='Closed').count(),
            "escalated":   escalated_count,
            "unread_notifications": Notification.query.filter_by(user_id=user_id, is_read=False).count(),
            "avg_resolution_days": avg_resolution_days,
            "resolution_rate": resolution_rate,
            "avg_first_response_hours": avg_first_response_hours,
            "avg_rating": avg_rating,
            "aging_open": aging_open_count,
        },
        pending_feedback_complaint_id=(f"CMP-{pending_feedback.id:05d}" if pending_feedback else None),
        oldest_aging_complaint=(_serialize_complaint(oldest_aging_complaint) if oldest_aging_complaint else None),
        recent_complaints=[_serialize_complaint(c) for c in recent],
        recent_notifications=[
            {
                "id": n.id, "title": n.title, "message": n.message,
                "is_read": n.is_read, "created_at": n.created_at.isoformat() if n.created_at else None
            }
            for n in recent_notes
        ],
        recent_activity=[
            {
                "id":           a.id,
                "type":         a.activity_type,
                "description":  a.description,
                "complaint_id": f"CMP-{a.complaint_id:05d}" if a.complaint_id else None,
                "created_at":   a.created_at.isoformat() if a.created_at else None
            }
            for a in recent_activity
        ]
    ), 200