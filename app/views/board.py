from flask_classful import FlaskView, route
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.models.board import Board
from app.models.comment import Comment
from app.models.user import User
from app.serailziers.board import BoardSchema


class BoardView(FlaskView):
    def index(self):
        boards = Board.objects()
        order = request.args.get('order')
        if order:
            boards = boards.order_by('-'+order)
        return BoardSchema(exclude=['user', 'likes', 'tags']).dump(boards, many=True), 200

    def get(self, board_id):
        try:
            board = Board.objects.get(id=board_id)
            board.modify(inc__num_of_views=1)
            return BoardSchema().dump(board), 200
        except Exception:
            return {'error': '존재하지 않는 게시글입니다.'}, 404

    @jwt_required
    def post(self):
        user = User.objects.get(id=get_jwt_identity())
        try:
            board = BoardSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400

        board.user = user
        board.save()
        return BoardSchema().dump(board), 201

    @jwt_required
    def put(self, id):
        try:
            board = Board.objects.get(id=id)
        except Exception:
            return {'error': '존재하지 않는 게시글입니다.'}, 404

        user = User.objects.get(id=get_jwt_identity())

        # 권한 확인
        if board.user != user:
            return {'error': '권한이 없습니다'}, 401

        try:
            data = BoardSchema().load(request.json)
        except ValidationError as err:
            err.messages, 400

        board.modify(title=data.title, content=data.title, tags=data.tags)
        return BoardSchema().dump(board), 200

    @jwt_required
    def delete(self, id):
        try:
            board = Board.objects.get(id=id)
        except Exception:
            return {'error': '존재하지 않는 게시글입니다.'}, 404
        user = User.objects.get(id=get_jwt_identity())

        # 권한 확인
        if board.user != user:
            return {'error': '권한이 없습니다'}, 401

        board.delete()
        return {'message': '삭제 완료!'}, 204

    @jwt_required
    @route('/<id>/like', methods=['POST'])
    def like(self, id):
        try:
            board = Board.objects.get(id=id)
        except Exception:
            return {'error': '존재하지 않는 게시글입니다.'}, 404
        user = User.objects.get(id=get_jwt_identity())

        # 이미 좋아요를 누른 경우 좋아요 취소
        if user in board.likes:
            board.modify(pull__likes=user)
        else:
            board.modify(add_to_set__likes=[user])
        board.modify(num_of_likes=len(board.likes))
        return BoardSchema().dump(board), 200