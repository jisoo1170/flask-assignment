from marshmallow import fields, Schema

from .user import UserSchema


class RecommentSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchema, only=['username'])
    content = fields.Str()


class CommentSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchema, only=['username'])
    content = fields.Str()
    recomments = fields.Nested(RecommentSchema, many=True)


class BoardSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchema, only=['username'])
    title = fields.Str()
    content = fields.Str()
    comments = fields.Nested(CommentSchema, many=True)
