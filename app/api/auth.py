from app import jwt
from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token


blacklist = set()


@jwt.token_in_blacklist_loader
def blacklist_lookup(token):
    jti = token["jti"]
    return jti in blacklist


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    result = {"mode": "development"}
    return result


@jwt.user_identity_loader
def user_identity_lookup(user):
    return {  # "_id": str(user.id),
            "email": user.email,
            "user_name": user.user_name}


def create_tokens(user, remember_me=False):
    access_token = create_access_token(identity=user, expires_delta=timedelta(minutes=10), fresh=False)
    if remember_me:
        refresh_token = create_refresh_token(identity=user, expires_delta=timedelta(days=365))
    else:
        refresh_token = create_refresh_token(identity=user, expires_delta=timedelta(days=1))

    return dict(access=access_token, refresh=refresh_token)


def create_fresh_token(user):
    access_token = create_access_token(identity=user, expires_delta=timedelta(minutes=1), fresh=True)
    return dict(access=access_token)


def refresh_access_token(user):
    print("Refreshing...")
    new_token = create_access_token(identity=user, expires_delta=timedelta(minutes=10), fresh=False)
    return dict(access=new_token)
