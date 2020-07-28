from mongoengine import fields
from flask_mongoengine import Document


class User(Document):
    username = fields.StringField(unique=True, required=True)
    password = fields.StringField(required=True)
