from . import db
from flask_mongoengine import Document



class PendingMsg(db.EmbeddedDocument):
    _id = db.ObjectIdField(required=True)
    sender = db.ReferenceField("User", required=True)
    chat_id = db.ObjectIdField(required=True)
    msg = db.StringField(required=True)
    time_stamp = db.DateTimeField(required=True)


class User(Document):
    meta = {"collection": "users"}

    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    user_name = db.StringField()
    contacts = db.ListField(db.ReferenceField("self", reverse_delete_rule=4))
    pending_msgs = db.EmbeddedDocumentListField(PendingMsg)
    sid = db.StringField()

    @classmethod
    def find_by_email(cls, email):
        return cls.objects(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.objects(id=_id).first()
