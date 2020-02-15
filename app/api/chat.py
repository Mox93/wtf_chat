from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from flask_socketio import emit
from . import api, request
from app.models.chat import Chat, PersonalChat, GroupChat
from app.models.user import User, PendingMsg
from bson import ObjectId


@api.route("/chats", methods=["GET"])
@jwt_required
def chats():
    current_user = get_jwt_identity()
    user = User.find_by_email(current_user["email"])

    if user:
        personal_chats = PersonalChat.find_by_user(user.id)
        group_chats = GroupChat.find_by_user(user.id)
        response = {"data": {"chats": []}}

        for chat in personal_chats:
            recipient = chat.recipient(user)
            response["data"]["chats"].append(
                {"_id": str(chat.id),
                 "recipient": {"email": recipient.email, "user_name": recipient.user_name}}
            )
        for chat in group_chats:
            response["data"]["chats"].append(
                {"_id": str(chat.id),
                 "members": [{"email": member.email, "user_name": member.user_name} for member in chat.members],
                 "name": chat.name}
            )
    else:
        response = {"error": "user not found."}

    print(response)
    return jsonify(response)


@api.route("/new-chat", methods=["POST"])
@jwt_required
def new_chat():
    data = request.get_json()
    current_user = get_jwt_identity()

    creator = User.find_by_email(current_user["email"])

    if creator:
        if "recipient" in data and "members" in data:
            response = {"error": "can't have both 'recipient' and 'members' in the request"}
        elif "recipient" in data:
            recipient = User.find_by_email(data["recipient"])
            if recipient:
                personal_chats = list(
                    filter(lambda c: c.recipient(creator) == recipient,
                           PersonalChat.find_by_user(creator.id)))
                if personal_chats:
                    chat = personal_chats[0]
                else:
                    chat = PersonalChat(user_1=creator, user_2=recipient)
                    chat.save()

                response = {"data": {"chat_id": str(chat.id),
                                     "recipient": {"email": recipient.email, "user_name": recipient.user_name}}}
            else:
                response = {"error": "couldn't find the user you're trying to add."}

        elif "members" in data:
            members = list(filter(lambda user: user,
                                  (User.find_by_email(email) for email in data["members"])))
            if members:
                members.append(creator)
                chat = GroupChat(members=members)
                chat.save()
                response = {
                    "data": {"chat_id": str(chat.id),
                             "members": [{
                                 "email": member.email,
                                 "user_name": member.user_name} for member in chat.members]}}
            else:
                response = {"error": "couldn't find any of the users you're trying to add."}
        else:
            response = {"error": "couldn't find 'recipient' nor 'members' in the request"}
    else:
        response = {"error": "couldn't find your account."}

    print(response)
    return jsonify(response)


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
            pending_msg = PendingMsg(_id=ObjectId(), sender=sender, chat_id=chat.id,
                                     msg=data["msg"], time_stamp=time_stamp)
            response = {"data": {
                "id": str(pending_msg._id), "from": sender, "chat_id": str(chat.id),
                "msg": data["msg"], "time_stamp": time_stamp
            }}
            print(response)
            for user in recipients:
                user.pending_msgs.append(pending_msg)
                user.save()

                emit("new message", response, room=user.sid)


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

    print(response)
    return jsonify(response)
