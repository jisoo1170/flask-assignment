from flask_classful import FlaskView, route
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.models.board import Board
from app.models.comment import Comment, Recomment
from app.models.user import User
from app.serailziers.comment import CommentSchema, RecommentSchema
from app.views import get_paginated_list


class CommentView(FlaskView):
    route_base = 'board/<board_id>/comment'

    def index(self, board_id):
        Board.objects.get_or_404(id=board_id)
        comments = Comment.objects(board_id=board_id).order_by('-num_of_likes')
        return jsonify(get_paginated_list(
            model='comments', results=comments, schema=CommentSchema(),
            url=f'/board/{board_id}/comment', params='',
            start=int(request.args.get('start', 1)), limit=20
        )), 200

    @jwt_required
    def post(self, board_id):
        try:
            data = CommentSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400
        comment = Comment(user=get_jwt_identity(), board_id=board_id, **data)
        comment.save()
        return CommentSchema().dump(comment), 201

    @jwt_required
    def patch(self, board_id, id):
        comment = Comment.objects.get_or_404(id=id)
        user = User.objects.get(id=get_jwt_identity())
        if comment.user != user:
            return {'message': '권한이 없습니다'}, 403
        try:
            data = CommentSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400
        comment.modify(**data)
        return CommentSchema().dump(comment), 200

    @jwt_required
    def delete(self, board_id, id):
        comment = Comment.objects.get_or_404(id=id)
        user = User.objects.get(id=get_jwt_identity())
        # 권한 확인
        if comment.user != user:
            return {'message': '권한이 없습니다'}, 403
        comment.delete()
        return {}, 204

    @jwt_required
    @route('/<id>/like', methods=['POST'])
    def like(self, board_id, id):
        comment = Comment.objects.get_or_404(id=id)
        user = User.objects.get(id=get_jwt_identity())
        # 이미 좋아요를 누른 경우 좋아요 취소
        if user in comment.likes:
            comment.modify(pull__likes=user)
        else:
            comment.modify(add_to_set__likes=[user])
        comment.modify(num_of_likes=len(comment.likes))
        return CommentSchema().dump(comment), 200


class RecommentView(FlaskView):
    route_base = 'board/<board_id>/comment/<comment_id>/recomment'
    decorators = [jwt_required]

    def post(self, board_id, comment_id):
        try:
            data = RecommentSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400
        recomment = Recomment(user=get_jwt_identity(), comment_id=comment_id, **data)
        recomment.save()
        return RecommentSchema().dump(recomment), 201

    def patch(self, board_id, comment_id, id):
        recomment = Recomment.objects.get_or_404(id=id)
        user = User.objects.get(id=get_jwt_identity())
        if recomment.user != user:
            return {'message': '권한이 없습니다'}, 403
        try:
            data = RecommentSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400
        recomment.modify(**data)
        return RecommentSchema().dump(recomment), 200

    def delete(self, board_id, comment_id, id):
        recomment = Recomment.objects.get_or_404(id=id)
        user = User.objects.get(id=get_jwt_identity())
        if recomment.user != user:
            return {'message': '권한이 없습니다'}, 403
        recomment.delete()
        return {}, 204

    @route('/<id>/like', methods=['POST'])
    def like(self, board_id, comment_id, id):
        recomment = Recomment.objects.get_or_404(id=id)
        user = User.objects.get(id=get_jwt_identity())
        # 이미 좋아요를 누른 경우 좋아요 취소
        if user in recomment.likes:
            recomment.modify(pull__likes=user)
        else:
            recomment.modify(add_to_set__likes=[user])
        return RecommentSchema().dump(recomment), 200