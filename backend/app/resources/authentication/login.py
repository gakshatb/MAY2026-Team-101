from flask import request
from flask_restful import Resource
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

from app.models import User


class LoginAPI(Resource):

    def post(self):

        data = request.get_json()

        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        if not email or not password:
            return {
                "message":"Email and password are required."
            },400

        user = User.query.filter_by(email=email).first()

        if not user:
            return {
                "message":"Invalid email or password."
            },401

        if not check_password_hash(user.password,password):
            return {
                "message":"Invalid email or password."
            },401

        if not user.is_active:
            return {
                "message":"Your account has been disabled."
            },403

        token = create_access_token(identity=user.id)

        return {
            "success":True,
            "token":token,
            "user":{
                "id":user.id,
                "name":user.name,
                "email":user.email,
                "role":user.role
            }
        },200