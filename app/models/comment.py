from mongoengine import Document, fields, CASCADE

from .user import User
from .board import Board


class Comment(Document):
    board_id = fields.ReferenceField('Board', dbref=False, reverse_delete_rule=CASCADE)
    user = fields.ReferenceField(User, reverse_delete_rule=CASCADE)
    content = fields.StringField()
    likes = fields.ListField(fields.ReferenceField(User, dbref=False, reverse_delete_rule=CASCADE))
    num_of_likes = fields.IntField(min_value=0, default=0)


class Recomment(Document):
    comment_id = fields.ReferenceField('Comment', dbref=False, reverse_delete_rule=CASCADE)
    user = fields.ReferenceField(User)
    content = fields.StringField()
    likes = fields.ListField(fields.ReferenceField(User, dbref=False, reverse_delete_rule=CASCADE))
