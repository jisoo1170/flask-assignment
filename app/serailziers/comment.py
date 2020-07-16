from marshmallow import fields, Schema, post_dump

from .user import UserSchema


class RecommentSchema(Schema):
    id = fields.String()
    user = fields.Nested(UserSchema, only=['username'])
    content = fields.String()
    num_of_likes = fields.Function(lambda obj: len(obj.likes))


class CommentSchema(Schema):
    id = fields.String()
    user = fields.Nested(UserSchema, only=['username'])
    content = fields.String()
    recomments = fields.Nested(RecommentSchema, many=True)
    num_of_likes = fields.Function(lambda obj: len(obj.likes))

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        key = "comments" if many else "comment"
        return {key: data}
