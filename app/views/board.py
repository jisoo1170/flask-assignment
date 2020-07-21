from flask_classful import FlaskView, route
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.models.board import Board
from app.models.user import User
from app.serailziers.board import BoardSchema
from app.views import get_paginated_list


class BoardView(FlaskView):
    def index(self):
        boards = Board.objects()
        order = request.args.get('order')
        if order:
            boards = boards.order_by('-'+order)
        return jsonify(get_paginated_list(
            model='boards', results=boards, schema=BoardSchema(exclude=['likes']),
            url='/board', params='&order=%s' % order,
            start=int(request.args.get('start', 1)), limit=15
        )), 200

    def get(self, board_id):
        board = Board.objects.get_or_404(id=board_id)
        board.modify(inc__num_of_views=1)
        return BoardSchema().dump(board), 200

    @jwt_required
    def post(self):
        user = User.objects.get(id=get_jwt_identity())
        try:
            data = BoardSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400

        board = Board(user=user, **data)
        board.save()
        return BoardSchema().dump(board), 201

    @jwt_required
    def patch(self, id):
        board = Board.objects.get_or_404(id=id)
        user = User.objects.get(id=get_jwt_identity())
        # 권한 확인
        if board.user != user:
            return {'message': '권한이 없습니다'}, 403

        try:
            data = BoardSchema().load(request.json)
        except ValidationError as err:
            err.messages, 400

        board.modify(**data)
        return BoardSchema().dump(board), 200

    @jwt_required
    def delete(self, id):
        board = Board.objects.get_or_404(id=id)
        user = User.objects.get(id=get_jwt_identity())
        # 권한 확인
        if board.user != user:
            return {'message': '권한이 없습니다'}, 403

        board.delete()
        return {}, 204

    @jwt_required
    @route('/<id>/like', methods=['POST'])
    def like(self, id):
        board = Board.objects.get_or_404(id=id)
        user = User.objects.get(id=get_jwt_identity())
        # 이미 좋아요를 누른 경우 좋아요 취소
        if user in board.likes:
            board.modify(pull__likes=user)
        else:
            board.modify(add_to_set__likes=[user])
        board.modify(num_of_likes=len(board.likes))
        return BoardSchema().dump(board), 200

    @route('/search')
    def search(self):
        # query params
        tag = request.args.get('tag')
        if not tag:
            return {'error': '검색어를 입력해주세요'}, 400
        boards = Board.objects(tags=tag.lower())
        return jsonify(get_paginated_list(
            model='boards', results=boards, schema=BoardSchema(exclude=['likes']),
            url='/search', params='&tag=%s'%tag,
            start=int(request.args.get('start', 1)), limit=15
        )), 200
