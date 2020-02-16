# Config
import json

err_msg = """==================================================
Please create a "config.json" file in the project's root directory with the following fields:
    - host : <str: i.e. "0.0.0.0">
    - port : <int: i.e. 5000>
    - secret : <str: i.e. "a random value" >
Once you've done that press Enter to continue."""

while True:
    try:
        with open("config.json", "r") as config:
            config = json.load(config)
        HOST = config["host"]
        SECRET = config["secret"]
        PORT = config["port"]
        break

    except (FileNotFoundError, KeyError):
        input(err_msg)


# App
from flask import Flask

app = Flask(__name__)
app.config["HOST"] = "localhost"
app.config["PORT"] = PORT
app.config["DEBUG"] = True


# CORS
from flask_cors import CORS

CORS(app)


# JWT
from flask_jwt_extended import JWTManager
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
    return render_template("index.html", host=f"http://{HOST}:{PORT}/")
