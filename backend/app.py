import os
from flask import Flask # type: ignore
from flask_cors import CORS # type: ignore
from flask_jwt_extended import JWTManager # type: ignore
from dotenv import load_dotenv # type: ignore

from models import init_db
from api import init_routes
from api_auth_utils import limiter

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, '..', 'frontend'),
            static_url_path='',
            template_folder=os.path.join(BASE_DIR, '..', 'frontend'))

CORS(app)

DEBUG = os.environ.get("FLASK_DEBUG", "false").strip().lower() in ("1", "true", "yes", "on")

app.config["SQLALCHEMY_DATABASE_URI"]  = os.environ.get("DATABASE_URL", "sqlite:///civicdesk.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "super-secret-key")
app.config["UPLOAD_FOLDER"] = os.environ.get(
    "UPLOAD_FOLDER", os.path.join(BASE_DIR, 'Uploads')
)
app.config["DEBUG"] = DEBUG
app.config["RATELIMIT_STORAGE_URI"] = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")
app.config["RATELIMIT_DEFAULT"] = "300 per hour"

jwt = JWTManager(app)
limiter.init_app(app)

admin_config = {
    "name": os.getenv("ADMIN_NAME"),
    "email": os.getenv("ADMIN_EMAIL"),
    "phone": os.getenv("ADMIN_PHONE"),
    "password": os.getenv("ADMIN_PASSWORD"),
    "mail_password": os.getenv("ADMIN_MAIL_PASSWORD")
}

init_db(app, admin_config)
init_routes(app)

if __name__ == '__main__':
    app.run(debug=DEBUG)