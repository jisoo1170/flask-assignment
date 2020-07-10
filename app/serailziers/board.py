from marshmallow import fields, Schema

from .user import UserSchema


class CommentSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchema, only=['username'])
    content = fields.Str()


class BoardSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchema, only=['username'])
    title = fields.Str()
    content = fields.Str()
    comment = fields.Nested(CommentSchema, many=True)
