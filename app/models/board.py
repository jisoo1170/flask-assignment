from mongoengine import fields, CASCADE
from flask_mongoengine import Document

from .user import User


class Board(Document):
    user = fields.ReferenceField(User, reverse_delete_rule=CASCADE, dbref=False)
    title = fields.StringField(max_length=100, required=True)
    content = fields.StringField(required=True)
    tags = fields.ListField(fields.StringField(max_length=20))
    likes = fields.ListField(fields.ReferenceField(User, reverse_delete_rule=CASCADE, dbref=False))
    num_of_likes = fields.IntField(min_value=0, default=0)
    num_of_views = fields.IntField(min_value=0, default=0)
