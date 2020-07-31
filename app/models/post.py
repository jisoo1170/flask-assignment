from mongoengine import fields, CASCADE
from flask_mongoengine import Document

from .user import User
from ..errors import IllegalStateError


class Post(Document):
    user = fields.ReferenceField(User, reverse_delete_rule=CASCADE, dbref=False)
    title = fields.StringField(max_length=100, required=True, null=False)
    content = fields.StringField(required=True, null=False)
    tags = fields.ListField(fields.StringField(max_length=20))
    likes = fields.ListField(fields.ReferenceField(User, reverse_delete_rule=CASCADE, dbref=False))
    num_of_likes = fields.IntField(default=0)
    num_of_views = fields.IntField(min_value=0, default=0)

    def read(self):
        self.modify(inc__num_of_views=1)

    def like(self, user):
        if user in self.likes:
            raise IllegalStateError("이미 좋아요를 눌렀습니다.")
        self.modify(add_to_set__likes=[user], inc__num_of_likes=1)

    def unlike(self, user):
        if user not in self.likes:
            raise IllegalStateError("좋아요를 눌러주세요.")
        self.modify(pull__likes=user, inc__num_of_likes=-1)
