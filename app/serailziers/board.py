from marshmallow import fields, Schema, post_dump

from .user import UserSchema


class RecommentSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchema, only=['username'])
    content = fields.Str()

    class Meta:
        fields = ("id", "user", "content")
        ordered = True


class CommentSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchema, only=['username'])
    content = fields.Str()
    recomments = fields.Nested(RecommentSchema, many=True)

    class Meta:
        fields = ("id", "user", "content", "recomments")
        ordered = True


class BoardSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchema, only=['username'])
    title = fields.Str()
    content = fields.Str()
    comments = fields.Nested(CommentSchema, many=True)

    class Meta:
        fields = ("id", "user", "title", "content", "comments")
        ordered = True

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        key = "boards" if many else "board"
        return {key: data}
