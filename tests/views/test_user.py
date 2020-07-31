import pytest

from flask import url_for
from flask_jwt_extended import create_access_token

from tests.factories.user import UserFactory
from app.serailziers.user import UserCreateSchema, UserPasswordChangeSchema, UserLoginSchema


class Describe_Userview:
    class Describe_signup:
        @pytest.fixture
        def user(self):
            return UserFactory.build()

        @pytest.fixture
        def subject(self, client, user):
            url = url_for('UserView:signup')
            response = client.post(url, json=UserCreateSchema().dump(user))
            return response

        class Context_정상_요청:
            def test_회원가입이_된다_201(self, subject):
                assert subject.status_code == 201

        class Context_이름이_없는_경우:
            @pytest.fixture
            def user(self, user):
                user.username = None
                return user

            def test_400을_반환한다(self, subject):
                assert subject.status_code == 400

        class Context_비밀번호가_없는_경우:
            @pytest.fixture()
            def user(self, user):
                user.password = None
                return user

            def test_400을_반환한다(self, subject):
                assert subject.status_code == 400

        class Context_이름_중복인_경우:
            @pytest.fixture()
            def user(self):
                exist_user = UserFactory.create()
                return UserFactory.build(username=exist_user.username)

            def test_409를_반환한다(self, subject):
                assert subject.status_code == 409

    class Describe_login:
        @pytest.fixture
        def request_user(self):
            return UserFactory.create()

        @pytest.fixture
        def subject(self, client, request_user):
            url = url_for('UserView:login')
            response = client.post(url, json=UserLoginSchema().dump(request_user))
            return response

        class Context_정상_요청:
            def test_로그인이_된다_200(self, subject):
                assert subject.status_code == 200
                assert subject.json['access_token']

        class Context_존재하지_않는_사용자:
            @pytest.fixture
            def request_user(self):
                return UserFactory.build()

            def test_404를_반환한다(self, subject):
                assert subject.status_code == 404

        class Context_비밀번호_불일치:
            @pytest.fixture
            def request_user(self, request_user):
                request_user.password = 'wrong_password'
                return request_user

            def test_400을_반환한다(self, subject):
                assert subject.status_code == 400

    class Describe_get_me:
        @pytest.fixture
        def subject(self, client, headers):
            url = url_for('UserView:get_me')
            response = client.get(url, headers=headers)
            return response

        class Context_정상_요청:
            def test_유저_정보를_반환한다(self, subject):
                assert subject.status_code == 200

        class Context_토큰이_없는_경우:
            @pytest.fixture
            def auth_token(self):
                return None

            def test_401을_반환한다(self, subject):
                assert subject.status_code == 401

        class Context_토큰에_해당하는_유저가_없는_경우:
            @pytest.fixture
            def auth_token(self):
                return create_access_token(identity=0)

            def test_401을_반환한다(self, subject):
                assert subject.status_code == 401

    # 비밀번호 수정
    class Describe_change_password:
        @pytest.fixture
        def logged_in_user(self, logged_in_user):
            logged_in_user.password = 'change password'
            return logged_in_user

        @pytest.fixture()
        def subject(self, client, headers, logged_in_user):
            url = url_for('UserView:change_my_password')
            response = client.patch(url, headers=headers, json=UserPasswordChangeSchema().dump(logged_in_user))
            return response

        class Context_정상_요청:
            def test_유저_비밀번호를_수정한다(self, subject):
                assert subject.status_code == 200

    class Describe_get_posts:
        @pytest.fixture()
        def subject(self, client, headers):
            url = url_for('UserView:my_posts')
            response = client.get(url, headers=headers)
            return response

        class Context_정상_요청:
            def test_작성한_게시글을_반환한다(self, subject):
                assert subject.status_code == 200
                assert 'items' in subject.json

    class Describe_get_comments:
        @pytest.fixture()
        def subject(self, client, headers):
            url = url_for('UserView:my_comments')
            response = client.get(url, headers=headers)
            return response

        class Context_정상_요청:
            def test_작성한_댓글을_반환한다(self, subject):
                assert subject.status_code == 200
                assert 'items' in subject.json

    class Describe_get_recomments:
        @pytest.fixture()
        def subject(self, client, headers):
            url = url_for('UserView:my_recomments')
            response = client.get(url, headers=headers)
            return response

        class Context_정상_요청:
            def test_작성한_게시글을_반환한다(self, subject):
                assert subject.status_code == 200
                assert 'items' in subject.json

    class Describe_get_liked_posts:
        @pytest.fixture()
        def subject(self, client, headers):
            url = url_for('UserView:my_liked_posts')
            response = client.get(url, headers=headers)
            return response

        class Context_정상_요청:
            def test_작성한_게시글을_반환한다(self, subject):
                assert subject.status_code == 200
                assert 'items' in subject.json
