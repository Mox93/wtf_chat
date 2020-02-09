from . import db
from .user import User
from flask_mongoengine import Document


class Chat(Document):
    meta = {"collection": "chats", "allow_inheritance": True}

    @classmethod
    def find_by_id(cls, _id):
        return cls.objects(id=_id).first()

    def get_users(self):
        pass


class PersonalChat(Chat):
    user_1 = db.ReferenceField(User, required=True, reverse_delete_rule=1)
    user_2 = db.ReferenceField(User, required=True, reverse_delete_rule=1)

    def get_users(self):
        return self.user_1, self.user_2


class ChatGroup(Chat):
    users = db.ListField(db.ReferenceField(User, required=True, reverse_delete_rule=1), required=True)
    name = db.StringField()

    def get_users(self):
        return self.users
