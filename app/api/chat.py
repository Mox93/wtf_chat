from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api
from app.models.chat import PersonalChat, GroupChat
from app.models.user import User


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

                response = {"data": {
                    "chat_id": str(chat.id), "recipient": {"email": recipient.email, "user_name": recipient.user_name}
                }}
            else:
                response = {"error": "couldn't find the user you're trying to add."}

        elif "members" in data:
            members = list(filter(lambda user: user,
                                  (User.find_by_email(email) for email in data["members"])))
            if members:
                members.append(creator)
                chat = GroupChat(members=members)
                chat.save()
                response = {"data": {
                    "chat_id": str(chat.id),
                    "members": [{"email": member.email, "user_name": member.user_name} for member in chat.members]
                }}
            else:
                response = {"error": "couldn't find any of the users you're trying to add."}
        else:
            response = {"error": "couldn't find 'recipient' nor 'members' in the request"}
    else:
        response = {"error": "couldn't find your account."}

    return jsonify(response)
