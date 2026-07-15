from flask import Blueprint, jsonify, request # type: ignore

from models import db, ContactMessage, Complaint, User
from api_auth_utils import is_valid_email

general_bp = Blueprint('general', __name__, url_prefix='/api')


# ─────────────────────────────────────────────────────────────────────────
# Public endpoint — no auth required.
# Saves a contact form submission to the contact_messages table.
# ─────────────────────────────────────────────────────────────────────────
@general_bp.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    if not data:
        return jsonify(message="Request body must be JSON."), 400

    name    = data.get("name",    "").strip()
    email   = data.get("email",   "").strip().lower()
    subject = data.get("subject", "General Inquiry").strip()
    message = data.get("message", "").strip()

    # ── validation ───────────────────────────────────────────────────────
    if len(name) < 3:
        return jsonify(message="Name must be at least 3 characters."), 400

    if not is_valid_email(email):
        return jsonify(message="Valid email address is required."), 400

    if not subject:
        return jsonify(message="Subject is required."), 400

    if len(message) < 20:
        return jsonify(message="Message must be at least 20 characters."), 400

    # ── save to DB ───────────────────────────────────────────────────────
    new_message = ContactMessage(
        name=name,
        email=email,
        subject=subject,
        message=message
    )
    db.session.add(new_message)
    db.session.commit()

    return jsonify(
        success=True,
        message="Your message has been received. We'll get back to you shortly."
    ), 201


# ─────────────────────────────────────────────────────────────────────────
# Public endpoint — no auth required.
# ─────────────────────────────────────────────────────────────────────────
@general_bp.route('/public-stats', methods=['GET'])
def public_stats():
    total_complaints = Complaint.query.count()
    resolved_complaints = Complaint.query.filter_by(status='Resolved').count()
    active_citizens = User.query.filter_by(role='Citizen', status='active').count()

    # Average resolution time (in hours) across complaints that have
    # actually been resolved and have both timestamps populated.
    resolved_rows = Complaint.query.filter(
        Complaint.status == 'Resolved',
        Complaint.updated_at.isnot(None)
    ).all()

    if resolved_rows:
        total_seconds = sum(
            (c.updated_at - c.created_at).total_seconds() for c in resolved_rows
        )
        avg_resolution_hours = round((total_seconds / len(resolved_rows)) / 3600, 1)
    else:
        avg_resolution_hours = 0

    return jsonify(
        success=True,
        stats={
            "total_complaints":     total_complaints,
            "resolved_complaints":  resolved_complaints,
            "active_citizens":      active_citizens,
            "avg_resolution_hours": avg_resolution_hours
        }
    ), 200


def init_routes(app):
    """Registers every blueprint with the Flask app."""
    from api_auth import auth_bp
    from api_citizen import citizen_bp
    from api_officer import officer_bp
    from api_admin import admin_bp
    from api_worker import worker_bp

    app.register_blueprint(general_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(citizen_bp)
    app.register_blueprint(officer_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(worker_bp)
