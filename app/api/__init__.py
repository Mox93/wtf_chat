from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_refresh_token_required, get_raw_jwt
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from .auth import create_tokens, refresh_access_token, blacklist

api = Blueprint("api", __name__)


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
        user = User(**data)
        user.password = generate_password_hash(data['password'], method="sha256")

        user.save()
        response = {
            "data": {
                "_id": str(user.id), **create_tokens(user, data.get("remember_me", False))
            }
        }

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
        
    return jsonify(response)


@api.route("/", methods=["GET", "POST"])
def test():
    return render_template("index.html")


