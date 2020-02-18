from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from flask_socketio import emit
from . import api
from app.models.chat import Chat
from app.models.user import User, PendingMsg
from bson import ObjectId
from config import NAMESPACE
import time


@api.route("/send-message", methods=["POST"])
@jwt_required
def send_message():
    data = request.get_json()
    current_user = get_jwt_identity()
    time_stamp = datetime.utcnow()

    sender = User.find_by_email(current_user["email"])
    chat = Chat.find_by_id(data.get("chat_id"))
    if chat:
        if sender in chat.members:
            pending_msg = PendingMsg(_id=ObjectId(), sender=sender, chat_id=chat.id,
                                     body=data["body"], time_stamp=time_stamp)
            response = {"data": {
                "_id": str(pending_msg._id), "sender": {"email": sender.email, "user_name": sender.user_name},
                "chat_id": str(chat.id), "body": pending_msg.body, "time_stamp": int(time_stamp.timestamp())
            }}
            for user in chat.members:
                user.pending_msgs.append(pending_msg)
                user.save()
                if user.sid and user != sender:
                    emit("new message", response, namespace=NAMESPACE, room=user.sid)
        else:
            response = {"error": "you aren't a part of this chat."}
    else:
        response = {"error": "couldn't find the chat you're trying to send to."}

    return response


@api.route("/confirm-receive", methods=["POST"])
@jwt_required
def confirm_receive():
    data = request.get_json()
    receiver = get_jwt_identity()
    user = User.find_by_email(receiver["email"])
    if user:
        user.pending_msgs = list(filter(lambda msg: msg._id != data["msg_id"], user.pending_msgs))
        user.save()
        response = {"data": {"ok": True}}
    else:
        response = {"error": "user not found."}

    return jsonify(response)
