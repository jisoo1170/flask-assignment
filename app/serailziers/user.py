from marshmallow import fields, Schema, post_load

from app.models.user import User


fields.Field.default_error_messages["required"] = "필수 항목 입니다"


class UserSchema(Schema):
    id = fields.Str()
    username = fields.String(required=True)
    password = fields.String(load_only=True, required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)