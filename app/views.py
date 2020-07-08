from flask_classful import FlaskView
from flask import request

from app.models import Board
from app.serailziers import BoardSchema


class BoardView(FlaskView):
    def __init__(self):
        self.schema = BoardSchema()

    def index(self):
        board = Board.objects()
        return self.schema.dumps(board, many=True), 200

    def get(self, pk):
        board = Board.objects.get(pk=pk)
        return self.schema.dumps(board)

    def post(self):
        try:
            title = request.values.get('title')
            content = request.values.get('content')
            board = Board(title=title, content=content)
            board.save()
            return self.schema.dumps(board), 201
        except Exception:
            return {'error': '글을 저장하지 못했습니다'}, 404

    def put(self, pk):
        title = request.values.get('title')
        content = request.values.get('content')
        board = Board.objects.get(pk=pk)
        board.update(title=title, content=content)
        return self.schema.dumps(board), 200

    def delete(self, pk):
        Board.objects(pk=pk).delete()
        return {'message': '삭제 완료!'}, 200
