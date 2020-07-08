from flask_classful import FlaskView
from flask import request

from app.models import Board


class BoardView(FlaskView):
    route_base = '/'

    def index(self):
        board = Board.objects()
        return board.to_json()

    def get(self, pk):
        board = Board.objects(pk=pk)
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

    def put(self, pk):
        title = request.values.get('title')
        content = request.values.get('content')
        board = Board.objects(pk=pk)
        board.update(title=title, content=content)
        return board.to_json()

    def delete(self, pk):
        Board.objects(pk=pk).delete()
        return {'message': '삭제 완료!'}
