from .board import BoardView
from .user import UserView


def register_api(app):
    BoardView.register(app)
    UserView.register(app)

