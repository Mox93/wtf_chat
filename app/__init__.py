# App
from flask import Flask
from config import PORT

app = Flask(__name__)
app.config["HOST"] = "localhost"
app.config["PORT"] = PORT
app.config["DEBUG"] = True


# CORS
from flask_cors import CORS

CORS(app)


# JWT
from flask_jwt_extended import JWTManager
from config import SECRET
# import secrets

app.config["JWT_SECRET_KEY"] = SECRET
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
jwt = JWTManager(app)


# Database
from app.models import db, DB_NAME, DB_HOST, DB_PORT

app.config["MONGODB_DB"] = DB_NAME
app.config["MONGODB_PORT"] = DB_PORT
app.config["MONGODB_HOST"] = DB_HOST

db.init_app(app)


# SocketIO
from config import NAMESPACE
from flask import request
from flask_socketio import SocketIO
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User

socket_IO = SocketIO(app)


@socket_IO.on("init", namespace=NAMESPACE)
@jwt_required
def init():
    current_user = get_jwt_identity()
    user = User.find_by_email(current_user["email"])
    user.sid = request.sid
    user.save()


# Blueprints
from app.api import api
from app.web import web

app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(web)
