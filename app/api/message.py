from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from flask_socketio import emit
from . import api, request
from app.models.chat import Chat, PersonalChat
from app.models.user import User, PendingMsg


@api.route("/new-chat", methods=["POST"])
@jwt_required
def new_chat():
    data = request.get_json()
    current_user = get_jwt_identity()
    other_user = data["email"]

    user_1 = User.find_by_email(current_user["email"])
    user_2 = User.find_by_email(other_user["email"])

    if user_1 and user_2:
        chat = PersonalChat(user_1, user_2)
        chat.save()
        response = {"data": {"chat_id": chat.id}}
    else:
        response = {"error": "couldn't find one of the users."}

    return response


@api.route("/send-message", methods=["POST"])
@jwt_required
def send_message():
    data = request.get_json()
    sender = get_jwt_identity()
    time_stamp = datetime.utcnow()
    chat = Chat.find_by_id(data.get("chat_id"))
    if chat:
        recipients = chat.get_users()
        if sender in recipients:
            response = {"from": sender, "chat_id": str(chat.id), "msg": data["msg"], "time_stamp": time_stamp}
            pending_msg = PendingMsg(sender=sender, chat_id=chat.id, msg=data["msg"], time_stamp=time_stamp)
            for user in recipients:
                user.pending_msgs.append(pending_msg)
                user.save()

                emit("received message", response, room=user.sid)
