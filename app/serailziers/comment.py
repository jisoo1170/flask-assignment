from marshmallow import fields, Schema, post_dump
from marshmallow.fields import Method

from .user import UserSchema
from app.models.comment import Recomment


class RecommentSchema(Schema):
    id = fields.String()
    user = fields.Nested(UserSchema, only=['username'])
    content = fields.String()
    num_of_likes = fields.Function(lambda obj: len(obj.likes))


class CommentSchema(Schema):
    id = fields.String()
    user = fields.Nested(UserSchema, only=['username'])
    content = fields.String()
    recomments = fields.Method('get_recomments')
    num_of_likes = fields.Function(lambda obj: len(obj.likes))

    def get_recomments(self, obj):
        return RecommentSchema().dump(Recomment.objects(comment_id=str(obj.id)), many=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        key = "comments" if many else "comment"
        return {key: data}
