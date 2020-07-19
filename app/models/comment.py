from mongoengine import Document, EmbeddedDocument, fields, CASCADE
from bson import ObjectId

from .user import User


class Recomment(EmbeddedDocument):
    id = fields.ObjectIdField(default=ObjectId)
    user = fields.ReferenceField(User)
    content = fields.StringField()
    likes = fields.ListField(fields.StringField())


class Comment(Document):
    board_id = fields.StringField()
    user = fields.ReferenceField(User, reverse_delete_rule=CASCADE)
    content = fields.StringField()
    recomments = fields.EmbeddedDocumentListField(Recomment)
    likes = fields.ListField(fields.StringField())
    num_of_likes = fields.IntField(min_value=0, default=0)