from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, ReferenceField, ListField, EmbeddedDocumentField

from .user import User


class Comment(EmbeddedDocument):
    user = ReferenceField(User)
    content = StringField()


class Board(Document):
    user = ReferenceField(User)
    title = StringField(max_length=100, required=True)
    content = StringField(required=True)
    comment = ListField(EmbeddedDocumentField(Comment))
