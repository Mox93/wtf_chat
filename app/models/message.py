from . import db
from .user import User
from .chat import Chat
from flask_mongoengine import Document


class Message(Document):
    meta = {"collection": "messages"}

    sender = db.ReferenceField(User, required=True, reverse_delete_rule=0)
    chat = db.ReferenceField(Chat, required=True, reverse_delete_rule=2)
    body = db.StringField(required=True)
    time_stamp = db.DateTimeField(required=True)
