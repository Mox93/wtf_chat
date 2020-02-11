from flask_socketio import emit
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import socket_IO
from datetime import datetime
from app.models.user import User
from app.models.chat import Chat


@socket_IO.on("message")
def message(msg):
    print(f"sid = {request.sid}")
    return msg


@socket_IO.on("initialization")
@jwt_required
def initialization():
    current_user = get_jwt_identity()
    user = User.find_by_email(current_user["email"])
    user.sid = request.sid
    user.save()


@socket_IO.on("send message")
def send_message(msg):
    time_stamp = datetime.utcnow()
    print(f"{msg.get('from')}: {msg.get('body')} <{time_stamp}>")
    emit("new message", f"{msg.get('from')}: {msg.get('body')} <{time_stamp}>", broadcast=True)


@socket_IO.on("confirm")
def confirm(data):
    print("Confirmed")
    user = User.find_by_email(data.get("email"))
    if user:
        print(f"{user.user_name} has received the message!")


@socket_IO.on("test")
def test(msg):
    print(f"resealed '{msg}' as a test!")
    return f"resealed '{msg}' as a test!"
