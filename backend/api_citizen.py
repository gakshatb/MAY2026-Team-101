import json
import os
import uuid
from datetime import datetime

from flask import Blueprint, current_app, jsonify, request # type: ignore
from flask_jwt_extended import get_jwt_identity # type: ignore
from werkzeug.utils import secure_filename # type: ignore

from models import db, User, Complaint, StatusLog, ComplaintImages, Feedback, Notification
from api_auth_utils import role_required

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
            "has_feedback":  c.feedback is not None,
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

    db.session.commit()

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
            "total":       base.count(),
            "pending":     base.filter_by(status='Pending').count(),
            "in_progress": base.filter_by(status='In Progress').count(),
            "resolved":    base.filter_by(status='Resolved').count(),
            "closed":      base.filter_by(status='Closed').count(),
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
    db.session.commit()

    return jsonify(success=True, message="Thank you! Your feedback has been submitted."), 201


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
# Profile — extends /api/me with the address/city/state/pincode/gender
# fields Profile.vue needs that the general auth endpoint doesn't return.
# ─────────────────────────────────────────────────────────────────────────
@citizen_bp.route('/profile', methods=['GET'])
@role_required('Citizen')
def get_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

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
            "accountId":  f"CVC-USR-{user.id:04d}",
            "memberSince": user.created_at.strftime('%B %d, %Y') if user.created_at else None
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

    db.session.commit()

    return jsonify(success=True, message="Profile updated successfully."), 200


# ─────────────────────────────────────────────────────────────────────────
# Combined dashboard summary: stats + recent complaints + recent
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

    return jsonify(
        success=True,
        category_breakdown={cat: count for cat, count in category_counts},
        summary={
            "total":       base.count(),
            "pending":     base.filter_by(status='Pending').count(),
            "in_progress": base.filter_by(status='In Progress').count(),
            "resolved":    base.filter_by(status='Resolved').count(),
            "closed":      base.filter_by(status='Closed').count(),
            "unread_notifications": Notification.query.filter_by(user_id=user_id, is_read=False).count(),
        },
        pending_feedback_complaint_id=(f"CMP-{pending_feedback.id:05d}" if pending_feedback else None),
        recent_complaints=[_serialize_complaint(c) for c in recent],
        recent_notifications=[
            {
                "id": n.id, "title": n.title, "message": n.message,
                "is_read": n.is_read, "created_at": n.created_at.isoformat() if n.created_at else None
            }
            for n in recent_notes
        ]
    ), 200
