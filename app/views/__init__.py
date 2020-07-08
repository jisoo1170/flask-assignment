from .board import BoardView


def register_api(app):
    BoardView.register(app)
