from functools import wraps
import re

from flask import jsonify, request # type: ignore
from flask_jwt_extended import ( # type: ignore
    get_jwt, get_jwt_identity, jwt_required, verify_jwt_in_request
)
from flask_limiter import Limiter # type: ignore
from flask_limiter.util import get_remote_address # type: ignore

from models import db, User, ActivityLog, TokenBlocklist, now_ist

VALID_ROLES = {'Admin', 'Citizen', 'Officer', 'Worker'}

limiter = Limiter(key_func=get_remote_address)

def is_token_revoked(jti):
    """DB-backed replacement for the old `jti in blocklist` check."""
    return TokenBlocklist.query.filter_by(jti=jti).first() is not None


def revoke_token(jti, expires_at, user_id=None):
    """Adds a jti to the blocklist. Caller is responsible for committing."""
    if is_token_revoked(jti):
        return
    db.session.add(TokenBlocklist(jti=jti, user_id=user_id, expires_at=expires_at))


def purge_expired_blocklist_entries():
    """Optional housekeeping — call periodically."""
    TokenBlocklist.query.filter(TokenBlocklist.expires_at < now_ist()).delete()
    db.session.commit()

# ─────────────────────────────────────────────────────────────────────────
# Recognised activity_type values for ActivityLog rows.
# ─────────────────────────────────────────────────────────────────────────
ACTIVITY_TYPES = {
    'register',
    'login',
    'logout',
    'password_changed',
    'password_reset_requested',
    'password_reset_completed',
    'profile_updated',
    'profile_photo_updated',
    'profile_photo_removed',
    'complaint_submitted',
    'feedback_submitted',
    'officer_approved',
    'officer_rejected',
    'officer_suspended',
    'officer_reactivated',
    'officer_updated',
    'officer_transferred',
    'department_created',
    'department_updated',
    'department_deleted',
}


def log_activity(user_id, activity_type, description, complaint_id=None):
    """Adds an ActivityLog row to the session."""
    if activity_type not in ACTIVITY_TYPES:
        raise ValueError(f"Unknown activity_type: {activity_type!r}")

    entry = ActivityLog(
        user_id=user_id,
        complaint_id=complaint_id,
        activity_type=activity_type,
        description=description,
        ip_address=request.remote_addr if request else None
    )
    db.session.add(entry)
    return entry


def is_valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', email) is not None


def is_valid_phone(phone):
    return re.match(r'^\d{10}$', phone) is not None


def token_not_revoked(fn):
    """Reject requests whose JWT has been blocklisted (i.e. logged out)."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        jti = get_jwt()["jti"]
        if is_token_revoked(jti):
            return jsonify(message="Token has been revoked. Please log in again."), 401
        return fn(*args, **kwargs)
    return wrapper


def role_required(*roles):
    """Restrict a route to one or more roles.
    Usage:  @role_required('Admin')
            @role_required('Officer', 'Admin')
    """
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            jti = get_jwt()["jti"]
            if is_token_revoked(jti):
                return jsonify(message="Token has been revoked. Please log in again."), 401
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id))
            if not user:
                return jsonify(message="User not found."), 404
            if user.role not in roles:
                return jsonify(
                    message=f"Access denied. Required role(s): {', '.join(roles)}."
                ), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
