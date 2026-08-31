from datetime import datetime, timedelta
import secrets

from flask import Blueprint, current_app, jsonify, request # type: ignore
from werkzeug.security import check_password_hash, generate_password_hash # type: ignore
from flask_jwt_extended import ( # type: ignore
    create_access_token, create_refresh_token, decode_token,
    get_jwt, get_jwt_identity, jwt_required
)

from models import db, User, PasswordResetOTP, LoginSession, now_ist, IST

from api_auth_utils import (
    VALID_ROLES, is_token_revoked, is_valid_email, is_valid_phone, limiter,
    log_activity, parse_user_agent, revoke_token, token_not_revoked
)
from mail import (
    send_welcome_email, send_registration_pending_email,
    send_password_reset_otp_email, send_password_changed_email,
)

auth_bp = Blueprint('auth', __name__, url_prefix='/api')


def _exp_to_ist(exp):
    return datetime.fromtimestamp(exp, tz=IST).replace(tzinfo=None)


# ─────────────────────────────────────────────────────────────────────────
# Register a new user (citizen, officer, worker).
# ─────────────────────────────────────────────────────────────────────────
@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
    data = request.get_json()
    if not data:
        return jsonify(message="Request body must be JSON."), 400

    name    = data.get("fullName",  "").strip()
    email   = data.get("email",     "").strip().lower()
    mobile  = data.get("mobile",    "").strip()
    role    = data.get("role",      "").strip().capitalize()   # normalize to Title case
    address = data.get("address",   "").strip()
    city    = data.get("city",      "").strip()
    pincode = data.get("pincode",   "").strip()
    password = data.get("password", "")

    # ── field validation ─────────────────────────────────────────────
    if not name:
        return jsonify(message="Name is required."), 400
    if not email:
        return jsonify(message="Email is required."), 400
    if not is_valid_email(email):
        return jsonify(message="Invalid email format."), 400
    if not mobile:
        return jsonify(message="Mobile number is required."), 400
    if not is_valid_phone(mobile):
        return jsonify(message="Mobile must be a 10-digit number."), 400
    if role not in VALID_ROLES:
        return jsonify(message=f"Invalid role. Choose from: {', '.join(VALID_ROLES)}."), 400
    if role == 'Admin':
        return jsonify(message="Admin accounts cannot be created via registration."), 403
    if not address:
        return jsonify(message="Address is required."), 400
    if not city:
        return jsonify(message="City is required."), 400
    if not pincode:
        return jsonify(message="Pincode is required."), 400
    if len(password) < 8:
        return jsonify(message="Password must be at least 8 characters."), 400

    # ── duplicate check ──────────────────────────────────────────────
    if User.query.filter_by(email=email).first():
        return jsonify(message="This email is already registered."), 409

    # ── create user ──────────────────────────────────────────────────
    # Citizens are usable immediately. Officer/Worker accounts need an
    # admin to approve them (see api_admin.py) before they can log in.
    initial_status = 'active' if role == 'Citizen' else 'pending'

    new_user = User(
        name=name,
        email=email,
        phone=mobile,
        password=generate_password_hash(password),
        address=address,
        city=city,
        state=data.get("state", "").strip() or None,
        pincode=pincode,
        gender=data.get("gender", "").strip() or None,
        role=role,
        status=initial_status
    )
    db.session.add(new_user)
    db.session.flush()   # get new_user.id before we log against it

    log_activity(new_user.id, 'register', f'Account created as {role}.')
    db.session.commit()

    if initial_status == 'active':
        send_welcome_email(to_email=email, name=name)
    else:
        send_registration_pending_email(to_email=email, name=name, role=role)

    message = (
        "Registration successful. You can now log in."
        if initial_status == 'active'
        else "Registration successful. Your account is pending admin approval before you can log in."
    )
    return jsonify(success=True, message=message), 201


# ─────────────────────────────────────────────────────────────────────────
# Authenticate user, return JWT access token + basic user info.
# ─────────────────────────────────────────────────────────────────────────
@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    if not data:
        return jsonify(message="Request body must be JSON."), 400

    email    = data.get("email",    "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify(message="Email and password are required."), 400

    user = User.query.filter_by(email=email).first()
    device, os_name, browser = parse_user_agent(request.headers.get('User-Agent'))

    if not user or not check_password_hash(user.password, password):
        if user:
            db.session.add(LoginSession(
                user_id=user.id, device=device, os=os_name, browser=browser,
                ip_address=request.remote_addr, status='Failed'
            ))
            db.session.commit()
        return jsonify(message="Invalid email or password."), 401

    if user.status == 'pending':
        return jsonify(message="Your account is pending admin approval."), 403
    if user.status != 'active':
        return jsonify(message="Your account has been disabled. Contact support."), 403

    access_token  = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    refresh_claims = decode_token(refresh_token)

    db.session.add(LoginSession(
        user_id=user.id,
        jti=refresh_claims['jti'],
        device=device, os=os_name, browser=browser,
        ip_address=request.remote_addr,
        status='Success',
        last_active_at=now_ist(),
        expires_at=_exp_to_ist(refresh_claims['exp'])
    ))
    log_activity(user.id, 'login', 'Logged in.')
    db.session.commit()

    return jsonify(
        success=True,
        access_token=access_token,
        refresh_token=refresh_token,
        user={
            "id":    user.id,
            "name":  user.name,
            "email": user.email,
            "role":  user.role,
            "profilePhoto": user.profile_photo
        }
    ), 200


# ─────────────────────────────────────────────────────────────────────────
# Revoke the current access token by adding its JTI to the blocklist.
# ─────────────────────────────────────────────────────────────────────────
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    revoke_token(claims["jti"], _exp_to_ist(claims["exp"]), user_id=user_id)

    data = request.get_json(silent=True) or {}
    refresh_token = data.get("refresh_token")
    if refresh_token:
        try:
            refresh_claims = decode_token(refresh_token)
            revoke_token(
                refresh_claims["jti"],
                _exp_to_ist(refresh_claims["exp"]),
                user_id=user_id
            )
            session = LoginSession.query.filter_by(jti=refresh_claims["jti"]).first()
            if session:
                session.revoked_at = now_ist()
        except Exception:
            pass

    log_activity(user_id, 'logout', 'Logged out.')
    db.session.commit()

    return jsonify(success=True, message="Logged out successfully."), 200


# ─────────────────────────────────────────────────────────────────────────
# Use refresh token to get a new access token without re-login.
# ─────────────────────────────────────────────────────────────────────────
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    jti = get_jwt()["jti"]
    if is_token_revoked(jti):
        return jsonify(message="Token has been revoked. Please log in again."), 401

    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user or user.status != 'active':
        return jsonify(message="User not found or disabled."), 403

    session = LoginSession.query.filter_by(jti=jti).first()
    if session:
        session.last_active_at = now_ist()
        db.session.commit()

    new_access_token = create_access_token(identity=str(user_id))
    return jsonify(
        success=True,
        access_token=new_access_token
    ), 200


# ─────────────────────────────────────────────────────────────────────────
# Return the currently logged-in user's profile.
# ─────────────────────────────────────────────────────────────────────────
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
@token_not_revoked
def me():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return jsonify(message="User not found."), 404

    return jsonify(
        success=True,
        user={
            "id":         user.id,
            "name":       user.name,
            "email":      user.email,
            "phone":      user.phone,
            "role":       user.role,
            "status":     user.status,
            "profilePhoto": user.profile_photo,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
    ), 200


# ─────────────────────────────────────────────────────────────────────────
# Step 1 of password reset — generate a 6-digit OTP and "send" it.
# ─────────────────────────────────────────────────────────────────────────
@auth_bp.route('/forgot-password', methods=['POST'])
@limiter.limit("5 per hour")
def forgot_password():
    data = request.get_json()
    if not data:
        return jsonify(message="Request body must be JSON."), 400

    email = data.get("email", "").strip().lower()
    if not email:
        return jsonify(message="Email is required."), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify(
            success=True,
            message="If this email is registered, an OTP has been sent."
        ), 200

    # Generate 6-digit OTP, valid for 10 minutes.
    otp = str(secrets.randbelow(900000) + 100000)   # 100000–999999

    PasswordResetOTP.query.filter_by(email=email).delete()
    db.session.add(PasswordResetOTP(
        email=email,
        otp_hash=generate_password_hash(otp),
        attempts=0,
        expires_at=now_ist() + timedelta(minutes=10)
    ))

    log_activity(user.id, 'password_reset_requested', 'Requested a password reset OTP.')
    db.session.commit()

    send_password_reset_otp_email(to_email=user.email, name=user.name, otp=otp)

    response_data = dict(success=True, message="OTP sent successfully.")
    if current_app.debug:
        response_data["dev_otp"] = otp

    return jsonify(**response_data), 200


# ─────────────────────────────────────────────────────────────────────────
# Step 2 of password reset — verify OTP and set new password.
# ─────────────────────────────────────────────────────────────────────────
@auth_bp.route('/reset-password', methods=['POST'])
@limiter.limit("5 per minute")
def reset_password():
    data = request.get_json()
    if not data:
        return jsonify(message="Request body must be JSON."), 400

    email        = data.get("email",       "").strip().lower()
    otp          = data.get("otp",         "").strip()
    new_password = data.get("newPassword", "")

    if not email or not otp or not new_password:
        return jsonify(message="Email, OTP, and new password are required."), 400

    if len(new_password) < 8:
        return jsonify(message="Password must be at least 8 characters."), 400

    # ── OTP validation ───────────────────────────────────────────────
    record = PasswordResetOTP.query.filter_by(email=email).first()

    if not record:
        return jsonify(message="No OTP request found for this email."), 400

    if now_ist() > record.expires_at:
        db.session.delete(record)
        db.session.commit()
        return jsonify(message="OTP has expired. Please request a new one."), 400

    if record.attempts >= PasswordResetOTP.MAX_ATTEMPTS:
        db.session.delete(record)
        db.session.commit()
        return jsonify(message="Too many incorrect attempts. Please request a new OTP."), 429

    if not check_password_hash(record.otp_hash, otp):
        record.attempts += 1
        db.session.commit()
        return jsonify(message="Invalid OTP."), 400

    # ── update password ──────────────────────────────────────────────
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify(message="User not found."), 404

    user.password = generate_password_hash(new_password)
    log_activity(user.id, 'password_reset_completed', 'Password reset via OTP.')

    # OTP is single-use — remove after successful reset
    db.session.delete(record)
    db.session.commit()

    send_password_changed_email(to_email=user.email, name=user.name)

    return jsonify(
        success=True,
        message="Password reset successful. You can now log in."
    ), 200


# ─────────────────────────────────────────────────────────────────────────
# Change password for a logged-in user (requires current password).
# ─────────────────────────────────────────────────────────────────────────
@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
@token_not_revoked
@limiter.limit("10 per hour")
def change_password():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return jsonify(message="User not found."), 404

    data = request.get_json()
    if not data:
        return jsonify(message="Request body must be JSON."), 400

    current_password = data.get("currentPassword", "")
    new_password     = data.get("newPassword",     "")

    if not current_password or not new_password:
        return jsonify(message="Current password and new password are required."), 400

    if not check_password_hash(user.password, current_password):
        return jsonify(message="Current password is incorrect."), 400

    if len(new_password) < 8:
        return jsonify(message="New password must be at least 8 characters."), 400

    if current_password == new_password:
        return jsonify(message="New password must be different from current password."), 400

    user.password = generate_password_hash(new_password)
    log_activity(user.id, 'password_changed', 'Password changed.')
    db.session.commit()

    send_password_changed_email(to_email=user.email, name=user.name)

    return jsonify(
        success=True,
        message="Password changed successfully."
    ), 200