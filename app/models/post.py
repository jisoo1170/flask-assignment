from mongoengine import fields, CASCADE
from flask_mongoengine import Document

from .user import User


class Post(Document):
    user = fields.ReferenceField(User, reverse_delete_rule=CASCADE, dbref=False)
    title = fields.StringField(max_length=100, required=True, null=False)
    content = fields.StringField(required=True, null=False)
    tags = fields.ListField(fields.StringField(max_length=20))
    likes = fields.ListField(fields.ReferenceField(User, reverse_delete_rule=CASCADE, dbref=False))
    num_of_likes = fields.IntField(min_value=0, default=0)
    num_of_views = fields.IntField(min_value=0, default=0)

    def read(self):
        self.num_of_views += 1
        self.save()

    def like(self, user):
        self.likes.append(user)
        self.num_of_likes += 1
        self.save()

    def unlike(self, user):
        self.likes.remove(user)
        self.num_of_likes -= 1
        self.save()
