from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_refresh_token_required, get_raw_jwt
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

    return jsonify(response)


@api.route("/exit", methods=["GET"])
@jwt_refresh_token_required
def exit_():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"data": {"ok": True}})


@api.route("/refresh", methods=["GET"])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()

    user = User.find_by_email(current_user["email"])
    if user:
        response = {"data": refresh_access_token(user)}
    else:
        response = {"error": "couldn't find user."}

    return jsonify(response)
