from marshmallow import fields, Schema, validate

from .user import UserSchema

not_empty = validate.Length(min=1)
fields.Field.default_error_messages = {
    "required": "Missing data for required field.",
    "null": "Field may not be null.",
    "validator_failed": "Invalid value.",
}


class PostSchema(Schema):
    id = fields.String(dump_only=True)
    user = fields.Nested(UserSchema, only=["username"], dump_only=True)
    title = fields.String(required=True, validate=not_empty)
    content = fields.String(required=True, validate=not_empty)
    tags = fields.List(fields.String())
    likes = fields.List(fields.Nested(UserSchema, only=["username"]), dump_only=True)
    num_of_likes = fields.Integer(dump_only=True)
    num_of_views = fields.Integer(dump_only=True)


class PostCreateSchema(PostSchema):
    class Meta:
        fields = ("title", "content", "tags")


class PostUpdateSchema(PostSchema):
    class Meta:
        fields = ("title", "content", "tags")


class PostPaginationSchema(Schema):
    items = fields.Nested(PostSchema, many=True)
    page = fields.Integer(missing=1)
    per_page = fields.Integer(missing=10)
    total = fields.Integer()
