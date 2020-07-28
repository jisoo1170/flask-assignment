from flask_classful import FlaskView, route
from flask import request, jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.models.post import Post
from app.models.comment import Comment, Recomment
from app.models.user import User
from app.serailziers.comment import CommentSchema, RecommentSchema
from app.views import get_paginated_list
from app.views.auth import login_required


class CommentView(FlaskView):
    def index(self, post_id):
        Post.objects.get_or_404(id=post_id)
        comments = Comment.objects(post=post_id).order_by('-num_of_likes')
        return jsonify(get_paginated_list(
            model='comments', results=comments, schema=CommentSchema(),
            url=f'/posts/{post_id}/comments', params='',
            start=int(request.args.get('start', 1)), limit=20
        )), 200

    @jwt_required
    @login_required
    def post(self, post_id):
        try:
            data = CommentSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400
        comment = Comment(user=g.user, post=post_id, **data)
        comment.save()
        return CommentSchema().dump(comment), 201

    @jwt_required
    @login_required
    def patch(self, post_id, id):
        comment = Comment.objects.get_or_404(id=id)
        if comment.user != g.user:
            return {'message': '권한이 없습니다'}, 403
        try:
            data = CommentSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400
        comment.modify(**data)
        return CommentSchema().dump(comment), 200

    @jwt_required
    @login_required
    def delete(self, post_id, id):
        comment = Comment.objects.get_or_404(id=id)
        # 권한 확인
        if comment.user != g.user:
            return {'message': '권한이 없습니다'}, 403
        comment.delete()
        return {}, 204

    @jwt_required
    @login_required
    @route('/<id>/likes', methods=['POST'])
    def like(self, post_id, id):
        comment = Comment.objects.get_or_404(id=id)
        # 이미 좋아요를 누른 경우 좋아요 취소
        if g.user in comment.likes:
            comment.modify(pull__likes=g.user)
        else:
            comment.modify(add_to_set__likes=[g.user])
        comment.modify(num_of_likes=len(comment.likes))
        return CommentSchema().dump(comment), 200


class RecommentView(FlaskView):
    decorators = [jwt_required, login_required]

    def post(self, post_id, comment_id):
        try:
            data = RecommentSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400
        recomment = Recomment(user=g.user, comment=comment_id, **data)
        recomment.save()
        return RecommentSchema().dump(recomment), 201

    def patch(self, post_id, comment_id, id):
        recomment = Recomment.objects.get_or_404(id=id)
        if recomment.user != g.user:
            return {'message': '권한이 없습니다'}, 403
        try:
            data = RecommentSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400
        recomment.modify(**data)
        return RecommentSchema().dump(recomment), 200

    def delete(self, post_id, comment_id, id):
        recomment = Recomment.objects.get_or_404(id=id)
        if recomment.user != g.user:
            return {'message': '권한이 없습니다'}, 403
        recomment.delete()
        return {}, 204

    @route('/<id>/likes', methods=['POST'])
    def like(self, post_id, comment_id, id):
        recomment = Recomment.objects.get_or_404(id=id)
        # 이미 좋아요를 누른 경우 좋아요 취소
        if g.user in recomment.likes:
            recomment.modify(pull__likes=g.user)
        else:
            recomment.modify(add_to_set__likes=[g.user])
        return RecommentSchema().dump(recomment), 200
