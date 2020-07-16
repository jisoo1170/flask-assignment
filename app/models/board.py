from mongoengine import Document, fields

from .user import User


class Board(Document):
    user = fields.ReferenceField(User)
    title = fields.StringField(max_length=100, required=True)
    content = fields.StringField(required=True)
    # comments = fields.EmbeddedDocumentListField(Comment)
    tags = fields.ListField(fields.StringField(max_length=20))
    likes = fields.ListField(fields.ReferenceField(User))
    num_of_likes = fields.IntField(min_value=0, default=0)
