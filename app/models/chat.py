from . import db
from .user import User
from flask_mongoengine import Document


class Chat(Document):
    meta = {"collection": "chats"}

    user_1 = db.LazyReferenceField(User, required=True, reverse_delete_rule=1)
    user_2 = db.LazyReferenceField(User, required=True, reverse_delete_rule=1)

    @classmethod
    def find_by_id(cls, _id):
        return cls.objects(id=_id).first()


class ChatGroup(Document):
    meta = {"collection": "chat_groups"}

    users = db.ListField(db.LazyReferenceField(User, required=True, reverse_delete_rule=1), required=True)
    name = db.StringField()

    @classmethod
    def find_by_id(cls, _id):
        return cls.objects(id=_id).first()
