from marshmallow import fields, Schema, post_dump

from .user import UserSchema


fields.Field.default_error_messages["required"] = "필수 항목 입니다"


class PostSchema(Schema):
    id = fields.String(dump_only=True)
    user = fields.Nested(UserSchema, only=['username'], dump_only=True)
    title = fields.String(required=True)
    content = fields.String(required=True)
    tags = fields.List(fields.String())
    likes = fields.List(fields.Nested(UserSchema, only=['username']), dump_only=True)
    num_of_likes = fields.Integer(dump_only=True)
    num_of_views = fields.Integer(dump_only=True)

    # @post_dump(pass_many=True)
    # def wrap(self, data, many, **kwargs):
    #     key = "boards" if many else "board"
    #     return {key: data}
