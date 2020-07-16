from flask_classful import FlaskView
from flask import request

from app.models.board import Board
from app.serailziers.board import BoardSchema


class SearchView(FlaskView):
    def get(self):
        # query params
        tag = request.args.get('tag')
        if not tag:
            return {'error': '검색어를 입력해주세요'}, 400
        boards = Board.objects(tags=tag.lower())
        return BoardSchema(exclude=['likes']).dump(boards, many=True), 200