from mongoengine import Document, EmbeddedDocument, fields
from bson import ObjectId

from .user import User


class Recomment(EmbeddedDocument):
    id = fields.ObjectIdField(default=ObjectId)
    user = fields.ReferenceField(User)
    content = fields.StringField()


class Comment(EmbeddedDocument):
    id = fields.ObjectIdField(default=ObjectId)
    user = fields.ReferenceField(User)
    content = fields.StringField()
    recomments = fields.EmbeddedDocumentListField(Recomment)


class Board(Document):
    user = fields.ReferenceField(User)
    title = fields.StringField(max_length=100, required=True)
    content = fields.StringField(required=True)
    comments = fields.EmbeddedDocumentListField(Comment)
    tags = fields.ListField(fields.StringField(max_length=20))
    likes = fields.ListField(fields.StringField())
