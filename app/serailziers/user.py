from marshmallow import fields, Schema, post_load

from app.models.user import User


class UserSchema(Schema):
    id = fields.Str()
    username = fields.String(required=True, error_messages={"required": {"message": "사용자 이름은 필수 항목입니다."}})
    password = fields.String(load_only=True, required=True, error_messages={"required": {"message": "비밀번호는 필수 항목입니다."}})
