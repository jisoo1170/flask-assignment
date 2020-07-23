from flask_classful import FlaskView, route
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.models.post import Post
from app.models.user import User
from app.serailziers.post import PostSchema
from app.views import get_paginated_list


class PostView(FlaskView):
    def index(self):
        posts = Post.objects()
        order = request.args.get('order')
        tag = request.args.get('tag')
        params = []
        if tag:
            params.append(f'&tag={tag}')
        if order:
            posts = posts.order_by(f'-{order}')
            params.append(f'&order={order}')
        return jsonify(get_paginated_list(
            model='posts', results=posts, schema=PostSchema(exclude=['likes']),
            url='/posts', params=''.join(params),
            start=int(request.args.get('start', 1)), limit=3
        )), 200

    def get(self, post_id):
        post = Post.objects.get_or_404(id=post_id)
        post.modify(inc__num_of_views=1)
        return PostSchema().dump(post), 200

    @jwt_required
    def post(self):
        try:
            data = PostSchema().load(request.json)
            if 'tags' in data:
                data['tags'] = [x.lower() for x in data['tags']]
        except ValidationError as err:
            return err.messages, 400

        post = Post(user=get_jwt_identity(), **data)
        post.save()
        return PostSchema().dump(post), 201

    @jwt_required
    def patch(self, id):
        post = Post.objects.get_or_404(id=id)
        user = User.objects.get(id=get_jwt_identity())
        # 권한 확인
        if post.user != user:
            return {'message': '권한이 없습니다'}, 403

        try:
            data = PostSchema().load(request.json)
        except ValidationError as err:
            err.messages, 400

        post.modify(**data)
        return PostSchema().dump(post), 200

    @jwt_required
    def delete(self, id):
        post = Post.objects.get_or_404(id=id)
        user = User.objects.get(id=get_jwt_identity())
        # 권한 확인
        if post.user != user:
            return {'message': '권한이 없습니다'}, 403

        post.delete()
        return {}, 204

    @jwt_required
    @route('/<id>/likes', methods=['POST'])
    def like(self, id):
        post = Post.objects.get_or_404(id=id)
        user = User.objects.get(id=get_jwt_identity())
        # 이미 좋아요를 누른 경우 좋아요 취소
        if user in post.likes:
            post.modify(pull__likes=user)
        else:
            post.modify(add_to_set__likes=[user])
        post.modify(num_of_likes=len(post.likes))
        return PostSchema().dump(post), 200
