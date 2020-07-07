from flask_classful import FlaskView

from app import app
from app.models import Board


class BoardView(FlaskView):
    def get(self):
        board = Board.objects()
        return board.to_json()
    

BoardView.register(app)
