from marshmallow import fields, Schema, post_dump

from .user import UserSchema


class RecommentSchema(Schema):
    id = fields.String()
    user = fields.Nested(UserSchema, only=['username'])
    content = fields.String()

    class Meta:
        fields = ("id", "user", "content")
        ordered = True


class CommentSchema(Schema):
    id = fields.String()
    user = fields.Nested(UserSchema, only=['username'])
    content = fields.String()
    recomments = fields.Nested(RecommentSchema, many=True)

    class Meta:
        fields = ("id", "user", "content", "recomments")
        ordered = True


class BoardSchema(Schema):
    id = fields.String()
    user = fields.Nested(UserSchema, only=['username'])
    title = fields.String()
    content = fields.String()
    comments = fields.Nested(CommentSchema, many=True)
    tags = fields.List(fields.String())
    likes = fields.List(fields.String())

    class Meta:
        # fields = ("id", "user", "title", "content", "tags", "comments")
        ordered = True

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        key = "boards" if many else "board"
        return {key: data}
