from flask_classful import FlaskView, route
from flask import request, jsonify, g
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.models.post import Post
from app.serailziers.post import PostSchema, PostPaginationSchema
from app.views import get_paginated_list
from app.views.auth import login_required


class PostView(FlaskView):
    def index(self, per_page=10):
        posts = Post.objects()
        order = request.args.get('order')
        tag = request.args.get('tag')
        params = []
        if tag:
            posts = posts(tags__iexact=tag)
            params.append(f'&tag={tag}')
        if order:
            posts = posts.order_by(f'-{order}')
            params.append(f'&order={order}')

        page = int(request.args.get('page', 1))
        paginated_posts = posts.paginate(page=page, per_page=per_page)
        return PostPaginationSchema().dump(paginated_posts)

    def get(self, post_id):
        post = Post.objects.get_or_404(id=post_id)
        post.read()
        return PostSchema().dump(post), 200

    @jwt_required
    @login_required
    def post(self):
        try:
            data = PostSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400

        post = Post(user=g.user, **data)
        post.save()
        return PostSchema().dump(post), 201

    @jwt_required
    @login_required
    def patch(self, id):
        post = Post.objects.get_or_404(id=id)
        # 권한 확인
        if post.user != g.user:
            return {'message': '권한이 없습니다'}, 403
        try:
            data = PostSchema().load(request.json)
        except ValidationError as err:
            err.messages, 400

        post.modify(**data)
        return PostSchema().dump(post), 200

    @jwt_required
    @login_required
    def delete(self, id):
        post = Post.objects.get_or_404(id=id)
        # 권한 확인
        if post.user != g.user:
            return {'message': '권한이 없습니다'}, 403

        post.delete()
        return {}, 204

    @jwt_required
    @login_required
    @route('/<id>/likes', methods=['POST'])
    def like(self, id):
        post = Post.objects.get_or_404(id=id)
        # 이미 좋아요를 누른 경우 좋아요 취소
        if g.user in post.likes:
            return {'message': '이미 좋아요를 눌렀습니다'}, 400
        post.like(g.user)
        return PostSchema().dump(post), 200


    @jwt_required
    @login_required
    @route('/<id>/unlikes', methods=['DELETE'])
    def unlike(self, id):
        post = Post.objects.get_or_404(id=id)
        if g.user not in post.likes:
            return {'message': '좋아요를 눌러주세요'}, 400
        post.unlike(g.user)
        return PostSchema().dump(post), 200
