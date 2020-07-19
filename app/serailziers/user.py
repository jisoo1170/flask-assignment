from marshmallow import fields, Schema


class UserSchema(Schema):
    id = fields.Str()
    username = fields.String()
