from mongoengine import Document
from mongoengine.fields import StringField


class Board(Document):
    title = StringField(max_length=100)
    content = StringField()
