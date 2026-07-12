from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from app.models import db, User

VALID_ROLES = ["citizen", "officer", "worker"]


class RegisterAPI(Resource):

    def post(self):

        data = request.get_json()

        name = data.get("name", "").strip()
        email = data.get("email", "").strip().lower()
        mobile = data.get("mobile", "").strip()
        role = data.get("role", "").strip().lower()
        address = data.get("address", "").strip()
        city = data.get("city", "").strip()
        pincode = data.get("pincode", "").strip()
        password = data.get("password", "")

        # ---------- Validation ----------

        if not name:
            return {"message": "Name is required"}, 400

        if not email:
            return {"message": "Email is required"}, 400

        if not mobile:
            return {"message": "Mobile number is required"}, 400

        if role not in VALID_ROLES:
            return {"message": "Invalid role"}, 400

        if not address:
            return {"message": "Address is required"}, 400

        if not city:
            return {"message": "City is required"}, 400

        if not pincode:
            return {"message": "Pincode is required"}, 400

        if len(password) < 8:
            return {"message": "Password must contain at least 8 characters"}, 400

        # Email already exists

        user = User.query.filter_by(email=email).first()

        if user:
            return {
                "message": "Email already registered."
            },409

        hashed_password = generate_password_hash(password)

        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            mobile=mobile,
            role=role,
            address=address,
            city=city,
            pincode=pincode
        )

        db.session.add(new_user)
        db.session.commit()

        return {
            "success": True,
            "message": "Registration successful."
        },201