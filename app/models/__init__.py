from flask_mongoengine import MongoEngine, Document

db = MongoEngine()

DB_NAME = "wtf_chat"
DB_PORT = 27017
DB_HOST = "localhost"


class ExtendedDocument(Document):
    meta = {"abstract": True}

    def json(self):
        pass

