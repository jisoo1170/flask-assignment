from flask_classful import FlaskView, route
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

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
            return BoardSchema().dump(Board.objects.get(id=board_id)), 200
        except Exception:
            return {'error': '존재하지 않는 게시글입니다.'}, 404

    @jwt_required
    def post(self):
        try:
            user = get_jwt_identity()
            title = request.json['title']
            content = request.json['content']
            tags = request.json['tags']
            board = Board(title=title, content=content, user=user, tags=tags)
            board.save()
            return BoardSchema().dump(board), 201
        except Exception:
            return {'error': '글을 저장하지 못했습니다'}, 404

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

        title = request.json['title']
        content = request.json['content']
        tags = request.json['tags']
        board.modify(title=title, content=content, tags=tags)
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

        # 게시글에 달린 댓글 삭제
        Comment.objects(board_id=id).delete()

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