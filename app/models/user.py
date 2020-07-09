from mongoengine import Document
from mongoengine.fields import StringField
from flask_bcrypt import generate_password_hash


class User(Document):
    username = StringField(unique=True, required=True)
    password = StringField(required=True)
