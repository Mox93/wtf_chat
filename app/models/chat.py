from . import db
from .user import User
from flask_mongoengine import Document
from mongoengine.queryset.visitor import Q


class Chat(Document):
    meta = {"collection": "chats", "allow_inheritance": True}

    @classmethod
    def find_by_id(cls, _id):
        return cls.objects(id=_id).first()


class PersonalChat(Chat):
    user_1 = db.ReferenceField(User, required=True, reverse_delete_rule=0)
    user_2 = db.ReferenceField(User, required=True, reverse_delete_rule=0)

    @property
    def members(self):
        return [self.user_1, self.user_2]

    def recipient(self, user):
        if self.user_1 == user:
            return self.user_2
        if self.user_2 == user:
            return self.user_1

    @classmethod
    def find_by_user(cls, user_id):
        return cls.objects(Q(user_1=user_id) | Q(user_2=user_id))


class GroupChat(Chat):
    members = db.ListField(db.ReferenceField(User, required=True, reverse_delete_rule=0), required=True)
    name = db.StringField()

    @classmethod
    def find_by_user(cls, user_id):
        return cls.objects(members=user_id)
