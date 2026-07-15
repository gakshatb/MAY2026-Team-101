from functools import wraps
from models import db, User, ContactMessage
from datetime import datetime, timedelta
from flask import jsonify, request # type: ignore
from werkzeug.security import check_password_hash, generate_password_hash # type: ignore
from flask_jwt_extended import ( # type: ignore
    get_jwt, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_required, verify_jwt_in_request
)
import re
import secrets

def init_routes(app):

    # ─────────────────────────────────────────────────────────────────────
    # TOKEN BLOCKLIST
    # In-memory set for revoked JTIs (logout).
    # ─────────────────────────────────────────────────────────────────────
    blocklist = set()

    # ─────────────────────────────────────────────────────────────────────
    # In-memory OTP store for forgot password
    # { email: { otp: str, expires_at: datetime } }
    # ─────────────────────────────────────────────────────────────────────
    otp_store = {}

    # ─────────────────────────────────────────────────────────────────────
    # DECORATORS
    # ─────────────────────────────────────────────────────────────────────

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

    # ─────────────────────────────────────────────────────────────────────
    # HELPER
    # ─────────────────────────────────────────────────────────────────────

    def is_valid_email(email):
        return re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', email) is not None

    def is_valid_phone(phone):
        return re.match(r'^\d{10}$', phone) is not None

    VALID_ROLES = {'Admin', 'Citizen', 'Officer', 'Worker'}

    # =========================================================================
    # AUTH ROUTES
    # =========================================================================

    # ─────────────────────────────────────────────────────────────────────────
    # Register a new user (citizen, officer, worker).
    # Admin accounts are seeded in init_db — cannot be registered via API.
    # ─────────────────────────────────────────────────────────────────────────
    @app.route('/api/register', methods=['POST'])
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
        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            phone=mobile,
            role=role,
            status='active'
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify(
            success=True,
            message="Registration successful. You can now log in."
        ), 201


    # ─────────────────────────────────────────────────────────────────────────
    # Authenticate user, return JWT access token + basic user info.
    # ─────────────────────────────────────────────────────────────────────────
    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json()
        if not data:
            return jsonify(message="Request body must be JSON."), 400

        email    = data.get("email",    "").strip().lower()
        password = data.get("password", "")

        if not email or not password:
            return jsonify(message="Email and password are required."), 400

        user = User.query.filter_by(email=email).first()

        # same message for both "not found" and "wrong password" — avoids
        # revealing which emails are registered (security best practice)
        if not user or not check_password_hash(user.password, password):
            return jsonify(message="Invalid email or password."), 401

        if user.status != 'active':
            return jsonify(message="Your account has been disabled. Contact support."), 403

        access_token  = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return jsonify(
            success=True,
            access_token=access_token,
            refresh_token=refresh_token,
            user={
                "id":    user.id,
                "name":  user.name,
                "email": user.email,
                "role":  user.role
            }
        ), 200


    # ─────────────────────────────────────────────────────────────────────────
    # Revoke the current access token by adding its JTI to the blocklist.
    # Frontend must also delete the token from localStorage/sessionStorage.
    # ─────────────────────────────────────────────────────────────────────────
    @app.route('/api/logout', methods=['POST'])
    @jwt_required()
    def logout():
        jti = get_jwt()["jti"]
        blocklist.add(jti)
        return jsonify(success=True, message="Logged out successfully."), 200


    # ─────────────────────────────────────────────────────────────────────────
    # Use refresh token to get a new access token without re-login.
    # Frontend should call this when it receives a 401 on any protected route.
    # ─────────────────────────────────────────────────────────────────────────
    @app.route('/api/refresh', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh():
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user or user.status != 'active':
            return jsonify(message="User not found or disabled."), 403

        new_access_token = create_access_token(identity=str(user_id))
        return jsonify(
            success=True,
            access_token=new_access_token
        ), 200


    # ─────────────────────────────────────────────────────────────────────────
    # Return the currently logged-in user's profile.
    # Frontend uses this on app load to restore session state.
    # ─────────────────────────────────────────────────────────────────────────
    @app.route('/api/me', methods=['GET'])
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
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
        ), 200


    # ─────────────────────────────────────────────────────────────────────────
    # Step 1 of password reset — generate a 6-digit OTP and "send" it.
    # ─────────────────────────────────────────────────────────────────────────
    @app.route('/api/forgot-password', methods=['POST'])
    def forgot_password():
        data = request.get_json()
        if not data:
            return jsonify(message="Request body must be JSON."), 400

        email = data.get("email", "").strip().lower()
        if not email:
            return jsonify(message="Email is required."), 400

        user = User.query.filter_by(email=email).first()

        # Always return 200 even if email not found — prevents email enumeration
        if not user:
            return jsonify(
                success=True,
                message="If this email is registered, an OTP has been sent."
            ), 200

        # Generate 6-digit OTP, valid for 10 minutes
        otp = str(secrets.randbelow(900000) + 100000)   # 100000–999999
        otp_store[email] = {
            "otp":        otp,
            "expires_at": datetime.now() + timedelta(minutes=10)
        }
        print(f"[DEBUG] OTP for {email}: {otp} (valid for 10 minutes)")
        response_data = dict(success=True, message="OTP sent successfully.")
        if app.debug:
            response_data["dev_otp"] = otp
        return jsonify(**response_data), 200


    # ─────────────────────────────────────────────────────────────────────────
    # Step 2 of password reset — verify OTP and set new password.
    # ─────────────────────────────────────────────────────────────────────────
    @app.route('/api/reset-password', methods=['POST'])
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
        record = otp_store.get(email)

        if not record:
            return jsonify(message="No OTP request found for this email."), 400

        if datetime.now() > record["expires_at"]:
            otp_store.pop(email, None)
            return jsonify(message="OTP has expired. Please request a new one."), 400

        if record["otp"] != otp:
            return jsonify(message="Invalid OTP."), 400

        # ── update password ──────────────────────────────────────────────
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify(message="User not found."), 404

        user.password = generate_password_hash(new_password)
        db.session.commit()

        # OTP is single-use — remove after successful reset
        otp_store.pop(email, None)

        return jsonify(
            success=True,
            message="Password reset successful. You can now log in."
        ), 200


    # ─────────────────────────────────────────────────────────────────────────
    # Change password for a logged-in user (requires current password).
    # ─────────────────────────────────────────────────────────────────────────
    @app.route('/api/change-password', methods=['POST'])
    @jwt_required()
    @token_not_revoked
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
            return jsonify(message="Current password is incorrect."), 401

        if len(new_password) < 8:
            return jsonify(message="New password must be at least 8 characters."), 400

        if current_password == new_password:
            return jsonify(message="New password must be different from current password."), 400

        user.password = generate_password_hash(new_password)
        db.session.commit()

        return jsonify(
            success=True,
            message="Password changed successfully."
        ), 200


    # ─────────────────────────────────────────────────────────────────────────
    # Public endpoint — no auth required.
    # Saves a contact form submission to the contact_messages table.
    # ─────────────────────────────────────────────────────────────────────────
    @app.route('/api/contact', methods=['POST'])
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
        print(f"[DEBUG] Saving contact message: {new_message}")
        db.session.add(new_message)
        db.session.commit()
 
        return jsonify(
            success=True,
            message="Your message has been received. We'll get back to you shortly."
        ), 201
 
    # =========================================================================
    # ── Add your future routes below this line ────────────────────────────────
    # Example:
    #   @app.route('/api/complaints', methods=['GET', 'POST'])
    #   @jwt_required()
    #   @token_not_revoked
    #   def complaints(): ...
    # =========================================================================