import os
from flask import Flask # type: ignore
from flask_cors import CORS # type: ignore
from flask_jwt_extended import JWTManager # type: ignore
from dotenv import load_dotenv # type: ignore

from models import init_db
from api import init_routes

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, '..', 'frontend'),
            static_url_path='',
            template_folder=os.path.join(BASE_DIR, '..', 'frontend'))

CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"]  = os.environ.get("DATABASE_URL", "sqlite:///civicdesk.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "super-secret-key")

jwt = JWTManager(app)

init_db(app)
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)