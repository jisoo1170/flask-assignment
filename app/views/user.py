from flask_classful import FlaskView, route
from flask import request, jsonify, g
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token
from marshmallow import ValidationError

from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment, Recomment
from app.serailziers.user import UserSchema, UserPasswordChangeSchema
from app.serailziers.post import PostSchema, PostPaginationSchema
from app.serailziers.comment import CommentSchema, RecommentSchema, CommentPaginationSchema, RecommentPaginationSchema

from app.views import get_paginated_list
from app.views.auth import login_required


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
    @login_required
    @route('/me')
    def get_me(self):
        return UserSchema().dump(g.user), 200

    # 정보 수정
    @jwt_required
    @login_required
    @route('/me/change-password', methods=['PATCH'])
    def change_my_password(self):
        try:
            data = UserPasswordChangeSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400
        g.user.modify(**data)
        return UserSchema().dump(g.user)

    # 사용자 삭제
    @jwt_required
    @login_required
    @route('/me', methods=['DELETE'])
    def delete_me(self):
        g.user.delete()
        return {}, 204

    # 내가 작성한 글 보기
    @jwt_required
    @login_required
    @route('/me/posts')
    def my_posts(self, per_page=10):
        posts = Post.objects(user=g.user)
        page = int(request.args.get('page', 1))
        paginated_posts = posts.paginate(page=page, per_page=per_page)
        return PostPaginationSchema().dump(paginated_posts)

    # 내가 작성한 댓글 보기
    @jwt_required
    @login_required
    @route('/me/comments')
    def my_comments(self, per_page=10):
        comments = Comment.objects(user=g.user)
        page = int(request.args.get('page', 1))
        paginated_comments = comments.paginate(page=page, per_page=per_page)
        return CommentPaginationSchema().dump(paginated_comments)

    # 내가 작성한 대댓글 보기
    @jwt_required
    @login_required
    @route('/me/recomments')
    def my_recomments(self, per_page=10):
        recomments = Recomment.objects(user=g.user)
        page = int(request.args.get('page', 1))
        paginated_recomments = recomments.paginate(page=page, per_page=per_page)
        return RecommentPaginationSchema().dump(paginated_recomments)

    # 좋아요 한 게시글 보기
    @jwt_required
    @login_required
    @route('/me/liked-posts')
    def my_liked_posts(self, per_page=10):
        posts = Post.objects(likes__in=[g.user])
        page = int(request.args.get('page', 1))
        paginated_posts = posts.paginate(page=page, per_page=per_page)
        return PostPaginationSchema().dump(paginated_posts)