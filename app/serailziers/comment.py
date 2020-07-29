from marshmallow import fields, Schema, post_dump

from .user import UserSchema
from app.models.comment import Recomment


fields.Field.default_error_messages["required"] = "필수 항목 입니다"


class RecommentSchema(Schema):
    id = fields.String(dump_only=True)
    user = fields.Nested(UserSchema, only=['username'], dump_only=True)
    content = fields.String(required=True)
    num_of_likes = fields.Function(lambda obj: len(obj.likes), dump_only=True)


class CommentSchema(Schema):
    id = fields.String(dump_only=True)
    user = fields.Nested(UserSchema, only=['username'], dump_only=True)
    content = fields.String(required=True)
    recomments = fields.Method('get_recomments', dump_only=True)
    num_of_likes = fields.Integer()

    def get_recomments(self, obj):
        return RecommentSchema().dump(Recomment.objects(comment=str(obj.id)), many=True)

    # @post_dump(pass_many=True)
    # def wrap(self, data, many, **kwargs):
    #     key = "comments" if many else "comment"
    #     return {key: data}


class CommentPaginationSchema(Schema):
    items = fields.Nested(CommentSchema, many=True)
    page = fields.Integer(missing=1)
    per_page = fields.Integer(missing=10)
    total = fields.Integer()


class RecommentPaginationSchema(Schema):
    items = fields.Nested(RecommentSchema, many=True)
    page = fields.Integer(missing=1)
    per_page = fields.Integer(missing=10)
    total = fields.Integer()
