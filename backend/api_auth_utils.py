from functools import wraps
import re

from flask import jsonify # type: ignore
from flask_jwt_extended import ( # type: ignore
    get_jwt, get_jwt_identity, jwt_required, verify_jwt_in_request
)

from models import User

blocklist = set()

VALID_ROLES = {'Admin', 'Citizen', 'Officer', 'Worker'}


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
        if jti in blocklist:
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
            if jti in blocklist:
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
