from .board import BoardView
from .comment import CommentView, RecommentView
from .user import UserView
from .search import SearchView


def register_api(app):
    UserView.register(app)
    BoardView.register(app)
    CommentView.register(app)
    RecommentView.register(app)
    SearchView.register(app)
