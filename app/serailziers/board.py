from marshmallow import fields, Schema

from .user import UserSchema


class CommentSchema(Schema):
    user = fields.Nested(UserSchema)
    content = fields.Str()


class BoardSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchema)
    title = fields.Str()
    content = fields.Str()
    comment = fields.Nested(CommentSchema, many=True)
