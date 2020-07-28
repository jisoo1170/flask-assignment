from flask_classful import FlaskView, route
from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from marshmallow import ValidationError

from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment, Recomment
from app.serailziers.user import UserSchema
from app.serailziers.post import PostSchema
from app.serailziers.comment import CommentSchema, RecommentSchema

from app.views import get_paginated_list


class UserView(FlaskView):
    # 회원가입
    @route('/signup/', methods=['POST'])
    def signup(self):
        try:
            data = UserSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400

        if User.objects(username=data['username']):
            return {'message': '존재하는 닉네임입니다.'}, 409

        # 사용자 저장
        user = User(**data)
        user.save()
        return UserSchema().dump(user), 201

    # 로그인
    @route('/login', methods=['POST'])
    def login(self):
        try:
            data = UserSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400

        user = User.objects.get_or_404(username=data['username'])
        if data['password'] != user.password:
            return {'message': '패스워드가 일치하지않습니다.'}, 400

        # 토큰 발급
        token = {
            'access_token': create_access_token(identity=str(user.id)),
            'refresh_token': create_refresh_token(identity=str(user.id))
        }
        return jsonify(token), 200

    # 사용자 정보 보기 (마이페이지)
    @jwt_required
    @route('/me')
    def get_me(self):
        user = User.objects.get_or_404(id=get_jwt_identity())
        return UserSchema().dump(user), 200

    # 정보 수정
    @jwt_required
    @route('/me', methods=['PATCH'])
    def patch_me(self):
        user = User.objects.get_or_404(id=get_jwt_identity())
        try:
            data = UserSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400
        if User.objects(username=data['username']):
            return {'message': '존재하는 닉네임입니다.'}, 409
        user.modify(**data)
        return UserSchema().dump(user)

    # 사용자 삭제
    @jwt_required
    @route('/me', methods=['DELETE'])
    def delete_me(self):
        User.objects.get_or_404(id=get_jwt_identity()).delete()
        return {}, 204

    # 내가 작성한 글 보기
    @jwt_required
    @route('/me/posts')
    def my_posts(self):
        user = User.objects.get_or_404(id=get_jwt_identity())
        posts = Post.objects(user=user)
        return jsonify(get_paginated_list(
            model='posts', results=posts, schema=PostSchema(only=("id", "title", "content")),
            url='/users/me/posts', params='',
            start=int(request.args.get('start', 1)), limit=15
        )), 200

    # 내가 작성한 댓글 보기
    @jwt_required
    @route('/me/comments')
    def my_comments(self):
        user = User.objects.get_or_404(id=get_jwt_identity())
        comments = Comment.objects(user=user)
        return jsonify(get_paginated_list(
            model='comments', results=comments, schema=CommentSchema(only=("id", "content")),
            url='/users/me/comments', params='',
            start=int(request.args.get('start', 1)), limit=15
        )), 200

    # 내가 작성한 대댓글 보기
    @jwt_required
    @route('/me/recomments')
    def my_recomment(self):
        user = User.objects.get_or_404(id=get_jwt_identity())
        recomments = Recomment.objects(user=user)
        return jsonify(get_paginated_list(
            model='recomments', results=recomments, schema=RecommentSchema(only=("id", "content")),
            url='/users/me/recomments', params='',
            start=int(request.args.get('start', 1)), limit=15
        )), 200

    # 좋아요 한 게시글 보기
    @jwt_required
    @route('/me/liked-posts')
    def my_liked_posts(self):
        user = User.objects.get_or_404(id=get_jwt_identity())
        boards = Post.objects(likes__in=[user])
        return jsonify(get_paginated_list(
            model='posts', results=boards, schema=PostSchema(only=("id", "title", "content")),
            url='/users/me/liked-posts', params='',
            start=int(request.args.get('start', 1)), limit=15
        )), 200
