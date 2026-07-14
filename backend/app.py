from flask import Flask # type: ignore
from flask_cors import CORS # type: ignore
from flask_jwt_extended import JWTManager # type: ignore

from models import init_db
from api import init_routes

jwt = JWTManager()

app = Flask(__name__, 
            static_folder='../Frontend/',
            static_url_path='',
            template_folder='../Frontend/')

CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///civicdesk.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your-secret-key"

init_db(app)
jwt.init_app(app)

init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)