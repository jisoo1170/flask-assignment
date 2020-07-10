from .board import BoardView, CommentView
from .user import UserView


def register_api(app):
    UserView.register(app)
    BoardView.register(app)
    CommentView.register(app)
