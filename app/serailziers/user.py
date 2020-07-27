from marshmallow import fields, Schema


fields.Field.default_error_messages["required"] = "필수 항목 입니다"


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(load_only=True, required=True)


class UserFormSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)