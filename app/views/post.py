from flask_classful import FlaskView, route
from flask import request, g
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.errors import IllegalStateError
from app.models.post import Post
from app.serailziers.post import PostSchema, PostPaginationSchema, PostUpdateSchema
from app.views.auth import login_required


class PostView(FlaskView):
    def index(self, per_page=10):
        posts = Post.objects()
        order = request.args.get('order')
        tag = request.args.get('tag')
        if tag:
            posts = posts(tags__iexact=tag)
        if order:
            posts = posts.order_by(f'-{order}')
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
            return err.messages, 422
        post = Post(user=g.user, **data)
        post.save()
        return PostSchema().dump(post), 201

    @jwt_required
    @login_required
    def patch(self, post_id):
        post = Post.objects.get_or_404(id=post_id)
        # 권한 확인
        if post.user != g.user:
            return {'message': '권한이 없습니다'}, 403
        try:
            data = PostUpdateSchema().load(request.json)
        except ValidationError as err:
            return {'message': err.messages}, 422
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
    def likes(self, id):
        post = Post.objects.get_or_404(id=id)
        try:
            post.like(g.user)
        except IllegalStateError as err:
            return {'message': err.message}, 409
        return PostSchema().dump(post), 200


    @jwt_required
    @login_required
    @route('/<id>/unlikes', methods=['DELETE'])
    def unlikes(self, id):
        post = Post.objects.get_or_404(id=id)
        try:
            post.unlike(g.user)
        except IllegalStateError as err:
            return {'message': err.message}, 409
        return PostSchema().dump(post), 200
