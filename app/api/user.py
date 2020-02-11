from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_refresh_token_required, get_raw_jwt
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from .auth import create_tokens, refresh_access_token, blacklist
from . import api


@api.route("/enter", methods=["POST"])
def enter():
    data = request.get_json()

    user = User.find_by_email(data["email"])
    if user:
        if check_password_hash(user.password, data["password"]):
            response = {
                "data": {
                    "_id": str(user.id), **create_tokens(user, data.get("remember_me", False))
                }
            }
        else:
            response = {"error": "wrong password."}
    else:
        user = User(email=data["email"])
        user.password = generate_password_hash(data['password'], method="sha256")

        user.save()
        response = {
            "data": {
                "_id": str(user.id), **create_tokens(user, data.get("remember_me", False))
            }
        }

    print(response)
    return jsonify(response)


@api.route("/user-name", methods=["POST"])
@jwt_required
def user_name():
    data = request.get_json()
    current_user = get_jwt_identity()

    user = User.find_by_email(current_user["email"])

    if user:
        user.user_name = data["user_name"]
        user.save()
        response = {
            "data": {
                **create_tokens(user, data.get("remember_me", False))
            }
        }

    else:
        response = {"error": "couldn't find user."}

    print(response)
    return jsonify(response)


@api.route("/exit", methods=["POST"])
@jwt_refresh_token_required
def exit():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)


@api.route("/refresh", methods=["GET"])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()

    user = User.find_by_email(current_user["email"])
    if user:
        response = {"data": refresh_access_token(user)}
    else:
        response = {"error": "couldn't find user."}

    print(response)
    return jsonify(response)


@api.route("/contacts", methods=["GET"])
@jwt_required
def contacts():
    current_user = get_jwt_identity()

    user = User.find_by_email(current_user["email"])
    if user:
        response = {"data": {
            "contacts": [{"user_name": u.user_name, "email": u.email} for u in user.contacts]
        }}
    else:
        response = {"error": "couldn't find user."}

    print(response)
    return jsonify(response)


@api.route("/add-contact", methods=["POST"])
@jwt_required
def add_contact():
    data = request.get_json()
    current_user = get_jwt_identity()

    user = User.find_by_email(current_user["email"])
    new_contact = User.find_by_email(data["email"])
    if user:
        if new_contact:
            if new_contact.id in [c.id for c in user.contacts]:
                response = {"error": "this user is already in your contacts."}
            elif new_contact.id == user.id:
                response = {"error": "you can't add yourself."}
            else:
                user.contacts.append(new_contact)
                user.save()
                response = {"data": {"email": new_contact.email, "user_name": new_contact.user_name}}
        else:
            response = {"error": "couldn't find contact."}
    else:
        response = {"error": "couldn't find user."}

    print(response)
    return jsonify(response)


@api.route("/remove-contact", methods=["DELETE"])
@jwt_required
def remove_contact():
    data = request.get_json()
    current_user = get_jwt_identity()

    user = User.find_by_email(current_user["email"])
    contact = User.find_by_email(data["email"])
    if user:
        if contact:
            if contact.id in [c.id for c in user.contacts]:
                user.contacts = list(filter(lambda u: contact.id != u.id, user.contacts))
                user.save()
                response = {"data": {"ok": True}}
            else:
                response = {"error": "this user is not in your contacts."}
        else:
            response = {"error": "couldn't find contact."}
    else:
        response = {"error": "couldn't find user."}

    print(response)
    return jsonify(response)
