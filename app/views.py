from flask_classful import FlaskView
from flask import request

from app import app
from app.models import Board


class BoardView(FlaskView):
    route_base = '/'

    def get(self):
        board = Board.objects()
        return board.to_json()

    def post(self):
        try:
            title = request.values.get('title')
            content = request.values.get('content')
            board = Board(title=title, content=content)
            board.save()
            return {'message': '저장 완료!'}
        except Exception:
            return {'error': '글을 저장하지 못했습니다'}


BoardView.register(app)
