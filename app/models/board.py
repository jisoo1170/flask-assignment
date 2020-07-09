from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, ReferenceField

from .user import User


class Board(Document):
    user = ReferenceField(User)
    title = StringField(max_length=100, required=True)
    content = StringField(required=True)


class Comment(EmbeddedDocument):
    content = StringField()
