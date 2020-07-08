from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField


class Board(Document):
    title = StringField(max_length=100)
    content = StringField()


class Comment(EmbeddedDocument):
    content = StringField()
