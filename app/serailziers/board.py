from marshmallow import fields, Schema

from .user import UserSchema


class BoardSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchema)
    title = fields.Str()
    content = fields.Str()
