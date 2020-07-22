from flask_classful import FlaskView, route
from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from marshmallow import ValidationError

from app.models.user import User
from app.models.board import Board
from app.models.comment import Comment, Recomment
from app.serailziers.user import UserSchema
from app.serailziers.board import BoardSchema
from app.serailziers.comment import CommentSchema, RecommentSchema

from app.views import get_paginated_list


class UserView(FlaskView):
    # 회원가입
    @route('/signup', methods=['POST'])
    def signup(self):
        try:
            data = UserSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400

        if User.objects(username=data['username']):
            return {'message': '존재하는 닉네임입니다.'}, 400

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

        user = User.objects.get(username=data['username'])
        if not user:
            return {'message': '회원가입을 먼저 해주세요'}, 404
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
    def get(self):
        user = User.objects.get(id=get_jwt_identity())
        return UserSchema().dump(user)

    # 정보 수정
    @jwt_required
    def patch(self):
        user = User.objects.get(id=get_jwt_identity())
        try:
            data = UserSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400
        if User.objects(username=data['username']):
            return {'message': '존재하는 닉네임입니다.'}, 400
        user.modify(**data)
        return UserSchema().dump(user)

    # 사용자 삭제
    @jwt_required
    def delete(self):
        User.objects.get(id=get_jwt_identity()).delete()
        return {}, 204

    # 내가 작성한 글 보기
    @jwt_required
    @route('/board')
    def board(self):
        boards = Board.objects(user=get_jwt_identity())
        return jsonify(get_paginated_list(
            model='boards', results=boards, schema=BoardSchema(only=("id", "title", "content")),
            url='/user/board', params='',
            start=int(request.args.get('start', 1)), limit=15
        )), 200

    # 내가 작성한 댓글 보기
    @jwt_required
    @route('/comment')
    def comment(self):
        comments = Comment.objects(user=get_jwt_identity())
        return jsonify(get_paginated_list(
            model='comments', results=comments, schema=CommentSchema(only=("id", "content")),
            url='/user/comment', params='',
            start=int(request.args.get('start', 1)), limit=15
        )), 200

    # 내가 작성한 대댓글 보기
    @jwt_required
    @route('/recomment')
    def recomment(self):
        recomments = Recomment.objects(user=get_jwt_identity())
        return jsonify(get_paginated_list(
            model='recomments', results=recomments, schema=RecommentSchema(only=("id", "content")),
            url='/user/recomment', params='',
            start=int(request.args.get('start', 1)), limit=15
        )), 200

    # 좋아요 한 게시글 보기
    @jwt_required
    @route('/like')
    def like(self):
        boards = Board.objects(likes__in=[get_jwt_identity()])
        return jsonify(get_paginated_list(
            model='boards', results=boards, schema=BoardSchema(only=("id", "title", "content")),
            url='/user/like', params='',
            start=int(request.args.get('start', 1)), limit=15
        )), 200
