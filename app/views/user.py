from flask_classful import FlaskView, route
from flask import request, session, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

from app.models.user import User


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
        return user.to_json()

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
            'access_token': create_access_token(identity=username),
            'refresh_token': create_refresh_token(identity=username)
        }
        return jsonify(token), 200

    def get(self):
        user = User.objects()
        return user.to_json()