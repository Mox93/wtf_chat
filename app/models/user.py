from . import db
from flask_mongoengine import Document


class PendingMsg(db.EmbeddedDocument):
    _id = db.StringField(required=True)
    msg = db.StringField(required=True)


class User(Document):
    meta = {"collection": "users"}

    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    user_name = db.StringField()
    pending_msgs = db.EmbeddedDocumentListField(PendingMsg)

    @classmethod
    def find_by_email(cls, email):
        return cls.objects(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.objects(id=_id).first()
