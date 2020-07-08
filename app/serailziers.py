from marshmallow import fields, Schema


class BoardSchema(Schema):
    id = fields.Str()
    title = fields.Str()
    content = fields.Str()
