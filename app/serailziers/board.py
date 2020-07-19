from marshmallow import fields, Schema, post_dump

from .user import UserSchema


class BoardSchema(Schema):
    id = fields.String()
    user = fields.Nested(UserSchema, only=['username'])
    title = fields.String()
    content = fields.String()
    tags = fields.List(fields.String())
    likes = fields.List(fields.Nested(UserSchema, only=['username']))
    num_of_likes = fields.Integer()
    num_of_views = fields.Integer()

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        key = "boards" if many else "board"
        return {key: data}
