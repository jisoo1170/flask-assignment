from flask_classful import FlaskView
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.board import Board, Comment, Recomment
from app.models.user import User
from app.serailziers.board import BoardSchema


class BoardView(FlaskView):
    def index(self):
        board = Board.objects()
        return BoardSchema(exclude=['comments']).dumps(board, many=True), 200

    def get(self, id):
        board = Board.objects.get(id=id)
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
    def put(self, id):
        board = Board.objects.get(id=id)
        user = User.objects.get(id=get_jwt_identity())

        # 권한 확인
        if board.user != user:
            return {'error': '권한이 없습니다'}, 401

        title = request.values.get('title')
        content = request.values.get('content')
        board.modify(title=title, content=content)
        return BoardSchema().dumps(board), 200

    @jwt_required
    def delete(self, id):
        board = Board.objects.get(id=id)
        user = User.objects.get(id=get_jwt_identity())

        # 권한 확인
        if board.user != user:
            return {'error': '권한이 없습니다'}, 401

        board.delete()
        return {'message': '삭제 완료!'}, 200


class CommentView(FlaskView):
    route_base = 'board/<board_id>/comment'

    @jwt_required
    def post(self, board_id):
        content = request.values.get('content')
        user = User.objects.get(id=get_jwt_identity())

        comment = Comment(user=user, content=content)

        board = Board.objects.get(id=board_id)
        board.comments.append(comment)
        board.save()
        return BoardSchema().dumps(board), 201

    @jwt_required
    def put(self, board_id, id):
        content = request.values.get('content')
        user = User.objects.get(id=get_jwt_identity())

        board = Board.objects.get(id=board_id)
        comment = board.comments.get(id=id)

        if comment.user != user:
            return {'error': '권한이 없습니다'}, 401

        comment.content = content
        board.save()

        return BoardSchema().dumps(board), 200

    @jwt_required
    def delete(self, board_id, id):
        user = User.objects.get(id=get_jwt_identity())

        board = Board.objects.get(id=board_id)
        comment = board.comments.get(id=id)

        # 권한 확인
        if comment.user != user:
            return {'error': '권한이 없습니다'}, 401

        board.comments.remove(comment)
        board.save()
        return {'message': '삭제 완료!'}, 200


class RecommentView(FlaskView):
    route_base = 'board/<board_id>/comment/<comment_id>/recomment'

    @jwt_required
    def post(self, board_id, comment_id):
        user = User.objects.get(id=get_jwt_identity())
        content = request.values.get('content')
        recomment = Recomment(user=user, content=content)

        board = Board.objects.get(id=board_id)
        comment = board.comments.get(id=comment_id)
        comment.recomments.append(recomment)
        board.save()
        return BoardSchema().dumps(board), 201
