from flask_classful import FlaskView, route
from flask import request, session, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

from app.models.user import User
from app.serailziers.user import UserSchema


class UserView(FlaskView):
    def __init__(self):
        self.schema = UserSchema()

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
        print(user[0].pk, username)

        # 토큰 발급
        token = {
            'access_token': create_access_token(identity=str(user[0].pk)),
            'refresh_token': create_refresh_token(identity=str(user[0].pk))
        }
        return jsonify(token), 200

    # 사용자 정보 보기 (마이페이지)
    @jwt_required
    def get(self):
        user = User.objects.get(pk=get_jwt_identity())
        return self.schema.dumps(user)

    # 정보 수정
    @jwt_required
    def patch(self):
        user = User.objects.get(pk=get_jwt_identity())
        username = request.values.get('username')
        password = request.values.get('password')
        if username:
            user.modify(username=username)
        if password:
            user.modify(password=password)
        return self.schema.dumps(user)

    # 사용자 삭제
    @jwt_required
    def delete(self):
        User.objects.get(pk=get_jwt_identity())
        return {'message': '삭제 완료!'}, 200
