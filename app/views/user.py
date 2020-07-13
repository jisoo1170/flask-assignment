from flask_classful import FlaskView, route
from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

from app.models.user import User
from app.models.board import Board, Comment
from app.serailziers.user import UserSchema
from app.serailziers.board import BoardSchema, CommentSchema


class UserView(FlaskView):
    # 회원가입
    @route('/signup', methods=['POST'])
    def signup(self):
        username = request.values.get('username')
        password1 = request.values.get('password1')
        password2 = request.values.get('password2')

        # 유효성 검사
        if User.objects(username=username):
            return {'message': '존재하는 닉네임입니다.'}, 400
        if password1 != password2:
            return {'message': '패스워드가 일치하지않습니다.'}, 400

        # 비밀번호 암호화
        # password = generate_password_hash('password1')

        # 사용자 저장
        user = User(username=username, password=password1)
        user.save()
        return {'message': '회원가입 완료!'}, 201

    # 로그인
    @route('/login', methods=['POST'])
    def login(self):
        username = request.values.get('username')
        password = request.values.get('password')

        # 유효성 검사
        user = User.objects(username=username)
        if not user:
            return {'message': '회원가입을 먼저 해주세요'}, 400
        # if not check_password_hash(user[0].password, password):
        if password != user[0].password:
            return {'message': '패스워드가 일치하지않습니다.'}, 400

        # 토큰 발급
        token = {
            'access_token': create_access_token(identity=str(user[0].id)),
            'refresh_token': create_refresh_token(identity=str(user[0].id))
        }
        return jsonify(token), 200

    # 사용자 정보 보기 (마이페이지)
    @jwt_required
    def get(self):
        user = User.objects.get(id=get_jwt_identity())
        return UserSchema().dumps(user)

    # 내가 작성한 글 보기
    @jwt_required
    @route('/board')
    def board(self):
        user = User.objects.get(id=get_jwt_identity())
        board = Board.objects(user=user)

        schema = BoardSchema(only=("id", "title", "content"))
        return schema.dumps(board, many=True), 200

    # 내가 작성한 댓글 보기
    @jwt_required
    @route('/comment')
    def comment(self):
        user = User.objects.get(id=get_jwt_identity())
        board = Board.objects.filter(comments__user=user)
        comment = []
        for b in board:
            comment += b.comments.filter(user=user)

        schema = CommentSchema(only=("id", "content"))
        return schema.dumps(comment, many=True), 200

    # 정보 수정
    @jwt_required
    def patch(self):
        user = User.objects.get(id=get_jwt_identity())
        username = request.values.get('username')
        password = request.values.get('password')

        if username:
            user.modify(username=username)
        if password:
            user.modify(password=password)
        return UserSchema().dumps(user)

    # 사용자 삭제
    @jwt_required
    def delete(self):
        User.objects.get(id=get_jwt_identity())
        return {'message': '삭제 완료!'}, 200
