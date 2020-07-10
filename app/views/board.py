from flask_classful import FlaskView
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.board import Board, Comment
from app.models.user import User
from app.serailziers.board import BoardSchema


class BoardView(FlaskView):
    def index(self):
        board = Board.objects()
        return BoardSchema(exclude=['comments']).dumps(board, many=True), 200

    def get(self, pk):
        board = Board.objects.get(pk=pk)
        return BoardSchema().dumps(board)

    @jwt_required
    def post(self):
        try:
            user = get_jwt_identity()
            title = request.values.get('title')
            content = request.values.get('content')

            board = Board(user=user, title=title, content=content)
            board.save()
            return BoardSchema().dumps(board), 201
        except Exception:
            return {'error': '글을 저장하지 못했습니다'}, 404

    @jwt_required
    def put(self, pk):
        board = Board.objects.get(pk=pk)
        user = User.objects.get(pk=get_jwt_identity())

        # 권한 확인
        if board.user != user:
            return {'error': '권한이 없습니다'}, 401

        title = request.values.get('title')
        content = request.values.get('content')
        board.modify(title=title, content=content)
        return BoardSchema().dumps(board), 200

    @jwt_required
    def delete(self, pk):
        board = Board.objects.get(pk=pk)
        user = User.objects.get(pk=get_jwt_identity())

        # 권한 확인
        if board.user != user:
            return {'error': '권한이 없습니다'}, 401

        board.delete()
        return {'message': '삭제 완료!'}, 200


class CommentView(FlaskView):
    route_base = 'board/<board_pk>/comment'

    @jwt_required
    def post(self, board_pk):
        comment = request.values.get('content')
        user = User.objects.get(pk=get_jwt_identity())

        comment = Comment(user=user, comment=comment)

        board = Board.objects.get(pk=board_pk)
        board.comments.append(comment)
        board.save()
        return BoardSchema().dumps(board), 201

    # @jwt_required
    # def put(self, board_pk, pk):
    #     content = request.values.get('content')
    #     user = User.objects.get(pk=get_jwt_identity())
    #
    #     comment = Comment.objects.get(pk=pk)
    #
    #     if comment.user != user:
    #         return {'error': '권한이 없습니다'}, 401
    #
    #     board = Board.objects.get(pk=board_pk)
    #     comment.modify(content=content)
    #     return BoardSchema().dumps(board), 200
