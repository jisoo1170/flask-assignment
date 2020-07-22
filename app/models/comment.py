from mongoengine import fields, CASCADE
from flask_mongoengine import Document

from .user import User


class Comment(Document):
    board_id = fields.LazyReferenceField('Board', dbref=False, reverse_delete_rule=CASCADE)
    user = fields.ReferenceField(User, reverse_delete_rule=CASCADE)
    content = fields.StringField()
    likes = fields.ListField(fields.LazyReferenceField(User, dbref=False, reverse_delete_rule=CASCADE))
    num_of_likes = fields.IntField(min_value=0, default=0)


class Recomment(Document):
    comment_id = fields.LazyReferenceField('Comment', dbref=False, reverse_delete_rule=CASCADE)
    user = fields.ReferenceField(User)
    content = fields.StringField()
    likes = fields.ListField(fields.LazyReferenceField(User, dbref=False, reverse_delete_rule=CASCADE))
