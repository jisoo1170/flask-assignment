from marshmallow import fields, Schema, post_dump

from .user import UserSchema


class BoardSchema(Schema):
    id = fields.String()
    user = fields.Nested(UserSchema, only=['username'])
    title = fields.String()
    content = fields.String()
    # comments = fields.Nested(CommentSchema, many=True)
    tags = fields.List(fields.String())
    likes = fields.List(fields.Nested(UserSchema, only=['username']))
    num_of_likes = fields.Integer()

    # class Meta:
        # fields = ("id", "user", "content", "tags", "likes", "num_of_likes")
        # ordered = True

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        key = "boards" if many else "board"
        return {key: data}
