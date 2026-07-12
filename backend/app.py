from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from werkzeug.security import generate_password_hash

from app.models import db, User

# Authentication APIs
from app.resources.authentication.register import RegisterAPI
from app.resources.authentication.login import LoginAPI

app = Flask(__name__)

# Enable CORS
CORS(app)

# --------------------------------
# Configuration
# --------------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///civicdesk.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your-secret-key"  # Change this in production

# --------------------------------
# Initialize Extensions
# --------------------------------
db.init_app(app)
api = Api(app)
jwt = JWTManager(app)

# --------------------------------
# Register API Routes
# --------------------------------
api.add_resource(RegisterAPI, "/api/register")
api.add_resource(LoginAPI, "/api/login")

# --------------------------------
# Create Default Administrator
# --------------------------------
def create_default_admin():
    admin = User.query.filter_by(role="administrator").first()

    if not admin:
        default_admin = User(
            name="Administrator",
            email="admin@gmail.com",
            mobile="9999999999",
            role="administrator",
            address="Municipal Office",
            city="Thane",
            pincode="421302",
            password=generate_password_hash("Admin@123")
        )

        db.session.add(default_admin)
        db.session.commit()

        print("✅ Default administrator created.")
        print("Email: admin@gmail.com")
        print("Password: Admin@123")
    else:
        print("ℹ️ Administrator already exists.")

# --------------------------------
# Create Database & Run Server
# --------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_default_admin()

    app.run(debug=True)