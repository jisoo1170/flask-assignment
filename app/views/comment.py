from flask_classful import FlaskView, route
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.board import Board
from app.models.comment import Comment, Recomment
from app.models.user import User
from app.serailziers.comment import CommentSchema, RecommentSchema


class CommentView(FlaskView):
    route_base = 'board/<board_id>/comment'

    def index(self, board_id):
        try:
            Board.objects.get(id=board_id)
        except Exception:
            return {'error': '존재하지 않는 게시글입니다.'}, 404

        comments = Comment.objects(board_id=board_id)
        return CommentSchema().dump(comments, many=True), 200

    @jwt_required
    def post(self, board_id):
        user = User.objects.get(id=get_jwt_identity())

        comment = Comment(board_id=board_id, user=user, content=request.json['content'])
        comment.save()
        return CommentSchema().dump(comment), 201

    @jwt_required
    def put(self, board_id, id):
        try:
            comment = Comment.objects.get(id=id)
        except Exception:
            return {'error': '존재하지 않는 댓글입니다.'}, 404

        user = User.objects.get(id=get_jwt_identity())
        if comment.user != user:
            return {'error': '권한이 없습니다'}, 401

        comment.modify(content=request.json['content'])
        return CommentSchema().dump(comment), 200

    @jwt_required
    def delete(self, board_id, id):
        try:
            comment = Comment.objects.get(id=id)
        except Exception:
            return {'error': '존재하지 않는 댓글입니다.'}, 404

        user = User.objects.get(id=get_jwt_identity())
        # 권한 확인
        if comment.user != user:
            return {'error': '권한이 없습니다'}, 401

        comment.delete()
        return {'message': '삭제 완료!'}, 200

    @jwt_required
    @route('/<id>/like', methods=['POST'])
    def like(self, board_id, id):
        try:
            comment = Comment.objects.get(id=id)
        except Exception:
            return {'error': '존재하지 않는 댓글입니다.'}, 404

        user = User.objects.get(id=get_jwt_identity())
        # 이미 좋아요를 누른 경우 좋아요 취소
        print(comment.likes)
        if user in comment.likes:
            comment.modify(pull__likes=user)
        else:
            comment.modify(add_to_set__likes=[user])
        comment.modify(num_of_likes=len(comment.likes))
        return CommentSchema().dump(comment), 200


class RecommentView(FlaskView):
    route_base = 'board/<board_id>/comment/<comment_id>/recomment'

    @jwt_required
    def post(self, board_id, comment_id):
        user = User.objects.get(id=get_jwt_identity())
        recomment = Recomment(user=user, comment_id=comment_id, content=request.json['content'])
        recomment.save()
        return RecommentSchema().dump(recomment), 201

    @jwt_required
    def put(self, board_id, comment_id, id):
        try:
            recomment = Recomment.objects.get(id=id)
        except Exception:
            return {'error': '존재하지 않는 대댓글입니다.'}, 404

        user = User.objects.get(id=get_jwt_identity())
        if recomment.user != user:
            return {'error': '권한이 없습니다'}, 401

        recomment.modify(content=request.json['content'])
        return RecommentSchema().dump(recomment), 200

    @jwt_required
    def delete(self, board_id, comment_id, id):
        try:
            recomment = Recomment.get(id=id)
        except Exception:
            return {'error': '존재하지 않는 대댓글입니다.'}, 404

        user = User.objects.get(id=get_jwt_identity())

        if recomment.user != user:
            return {'error': '권한이 없습니다'}, 401

        recomment.delete()
        return {'message': '삭제 완료!'}, 204

    @jwt_required
    @route('/<id>/like', methods=['POST'])
    def like(self, board_id, comment_id, id):
        try:
            recomment = Recomment.objects.get(id=id)
        except Exception:
            return {'error': '존재하지 않는 대댓글입니다.'}, 404

        user = User.objects.get(id=get_jwt_identity())
        # 이미 좋아요를 누른 경우 좋아요 취소
        if user in recomment.likes:
            recomment.modify(pull__likes=user)
        else:
            recomment.modify(add_to_set__likes=[user])
        return RecommentSchema().dump(recomment), 200