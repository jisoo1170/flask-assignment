from marshmallow import fields, Schema

from .user import UserSchema


class CommentSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchema, only=['username'])
    comment = fields.Str()


class BoardSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchema, only=['username'])
    title = fields.Str()
    content = fields.Str()
    comments = fields.Nested(CommentSchema, many=True)
