from mongoengine import Document, EmbeddedDocument, fields
from bson import ObjectId

from .user import User


class Comment(EmbeddedDocument):
    id = fields.ObjectIdField(default=ObjectId)
    user = fields.ReferenceField(User)
    comment = fields.StringField()


class Board(Document):
    user = fields.ReferenceField(User)
    title = fields.StringField(max_length=100, required=True)
    content = fields.StringField(required=True)
    comments = fields.EmbeddedDocumentListField(Comment)
