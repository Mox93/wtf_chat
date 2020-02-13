# Config
import json

with open("config.json", "r") as config:
    config = json.load(config)


# App
from flask import Flask

app = Flask(__name__)
app.config["HOST"] = "localhost"
app.config["PORT"] = config["port"]
app.config["DEBUG"] = True


# CORS
from flask_cors import CORS

CORS(app)


# JWT
from flask_jwt_extended import JWTManager
# import secrets

app.config["JWT_SECRET_KEY"] = config["secret"]
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
jwt = JWTManager(app)


# Database
from app.models import db, DB_NAME, DB_HOST, DB_PORT

app.config["MONGODB_DB"] = DB_NAME
app.config["MONGODB_PORT"] = DB_PORT
app.config["MONGODB_HOST"] = DB_HOST

db.init_app(app)


# API
from app.api import api

app.register_blueprint(api, url_prefix="/api")


# SocketIO
from flask_socketio import SocketIO

socket_IO = SocketIO(app)

from app.api.chat_events import *


# Testing
from flask import render_template


@app.route("/", methods=["GET", "POST"])
def test():
    return render_template("index.html", host=f"http://{config['host']}:{config['port']}/")
