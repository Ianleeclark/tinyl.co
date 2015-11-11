from app import db


class Url(db.Document):
    url = db.StringField(max_length=255, required=True, unique=True)
    encoded = db.StringField(max_length=33, required=True)
    fullenc = db.StringField(max_length=33, required=True)
    hits = db.IntField(default=0)
