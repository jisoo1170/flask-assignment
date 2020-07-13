from mongoengine import Document, fields


class User(Document):
    username = fields.StringField(unique=True, required=True)
    password = fields.StringField(required=True)
