import pytest
import json

from factory.fuzzy import FuzzyText
from flask import url_for
from flask_jwt_extended import create_access_token

from tests.factories.user import UserFactory
from app.serailziers.user import UserCreateFormSchema


class Describe_Userview:
    class Describe_signup:
        @pytest.fixture
        def form(self):
            user = UserFactory.build()
            return user

        @pytest.fixture
        def subject(self, client, form):
            url = url_for('UserView:signup')
            response = client.post(url, json=UserCreateFormSchema().dump(form))
            return response

        class Context_정상_요청:
            def test_회원가입이_된다_201(self, subject):
                assert subject.status_code == 201

        class Context_이름이_없는_경우:
            @pytest.fixture
            def form(self, form):
                form.username = None
                return form

            def test_400을_반환한다(self, subject):
                assert subject.status_code == 400

        class Context_비밀번호가_없는_경우:
            @pytest.fixture()
            def form(self, form):
                form.password = None
                return form

            def test_400을_반환한다(self, subject):
                assert subject.status_code == 400

        class Context_이름_중복:
            @pytest.fixture()
            def form(self):
                exist_user = UserFactory.create()
                user = UserFactory.build(username=exist_user.username)
                return user

            def test_409를_반환한다(self, subject):
                assert subject.status_code == 409

    class Describe_login:
        @pytest.fixture
        def subject(self, client, user):
            url = url_for('UserView:login')
            response = client.post(url, json=UserCreateFormSchema().dump(user))
            return response

        class Context_정상_요청:
            def test_로그인이_된다_200(self, subject):
                assert subject.status_code == 200
                assert subject.json['access_token']

        class Context_존재하지_않는_사용자:
            @pytest.fixture
            def user(self):
                user = UserFactory.build()
                return user

            def test_404를_반환한다(self, subject):
                assert subject.status_code == 404

        class Context_비밀번호_불일치:
            @pytest.fixture
            def user(self, user):
                user.password = 'wrong_password'
                return user

            def test_400을_반환한다(self, subject):
                assert subject.status_code == 400

    class Describe_get_me:
        @pytest.fixture
        def subject(self, client, headers):
            url = url_for('UserView:get_me')
            response = client.get(url, headers=headers)
            return response

        class Context_정상_요청:
            def test_유저_정보를_반환한다(self, subject, logged_in_user):
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

            def test_404를_반환한다(self, subject):
                assert subject.status_code == 401

    # 비밀번호 수정
    class Describe_patch:
        @pytest.fixture
        def logged_in_user(self, logged_in_user):
            logged_in_user.username = 'change username'
            return logged_in_user

        @pytest.fixture()
        def subject(self, client, headers, logged_in_user):
            url = url_for('UserView:patch')
            response = client.patch(url, headers=headers, json=UserCreateFormSchema().dump(logged_in_user))
            return response

        class Context_정상_요청:
            def test_유저_정보를_수정한다(self, subject):
                assert subject.status_code == 200
                assert subject.json['username'] == 'change username'

        class Context_이름이_중복되는_경우:
            @pytest.fixture
            def exist_user(self, user):
                exist_user = UserFactory.create()
                user.username = exist_user.username
                return user

            def test_409를_반환한다(self, subject):
                return subject.status_code == 409

        class Context_토큰이_없는_경우:
            @pytest.fixture
            def subject(self, client):
                url = url_for('UserView:patch')
                response = client.patch(url)
                return response

            def test_401을_반환한다(self, subject):
                assert subject.status_code == 401

        class Context_토큰에_해당하는_유저가_없는_경우:
            @pytest.fixture
            def auth_token(self):
                return create_access_token(identity=0)

            def test_404를_반환한다(self, subject):
                assert subject.status_code == 404

    class Describe_get_posts:
        @pytest.fixture()
        def subject(self, client, headers):
            url = url_for('UserView:post')
            response = client.get(url, headers=headers)
            return response

        class Context_정상_요청:
            def test_작성한_게시글을_반환한다(self, subject):
                assert subject.status_code == 200
                assert 'posts' in subject.json

        class Context_토큰이_없는_경우:
            @pytest.fixture
            def subject(self, client):
                url = url_for('UserView:post')
                response = client.get(url)
                return response

            def test_401을_반환한다(self, subject):
                assert subject.status_code == 401

        class Context_토큰에_해당하는_유저가_없는_경우:
            @pytest.fixture
            def auth_token(self):
                return create_access_token(identity=0)

            def test_404를_반환한다(self, subject):
                assert subject.status_code == 404


    class Describe_get_comments:
        @pytest.fixture()
        def subject(self, client, headers):
            url = url_for('UserView:comment')
            response = client.get(url, headers=headers)
            return response

        class Context_정상_요청:
            def test_작성한_댓글을_반환한다(self, subject):
                assert subject.status_code == 200
                assert 'comments' in subject.json

        class Context_토큰이_없는_경우:
            @pytest.fixture
            def subject(self, client):
                url = url_for('UserView:comment')
                response = client.get(url)
                return response

            def test_401을_반환한다(self, subject):
                assert subject.status_code == 401

        class Context_토큰에_해당하는_유저가_없는_경우:
            @pytest.fixture
            def auth_token(self):
                return create_access_token(identity=0)

            def test_404를_반환한다(self, subject):
                assert subject.status_code == 404

    class Describe_get_recomments:
        @pytest.fixture()
        def subject(self, client, headers):
            url = url_for('UserView:recomment')
            response = client.get(url, headers=headers)
            return response

        class Context_정상_요청:
            def test_작성한_게시글을_반환한다(self, subject):
                assert subject.status_code == 200
                assert 'recomments' in subject.json

        class Context_토큰이_없는_경우:
            @pytest.fixture
            def subject(self, client):
                url = url_for('UserView:recomment')
                response = client.get(url)
                return response

            def test_401을_반환한다(self, subject):
                assert subject.status_code == 401

        class Context_토큰에_해당하는_유저가_없는_경우:
            @pytest.fixture
            def auth_token(self):
                return create_access_token(identity=0)

            def test_404를_반환한다(self, subject):
                assert subject.status_code == 404

    class Describe_get_liked_posts:
        @pytest.fixture()
        def subject(self, client, headers):
            url = url_for('UserView:like')
            response = client.get(url, headers=headers)
            return response

        class Context_정상_요청:
            def test_작성한_게시글을_반환한다(self, subject):
                assert subject.status_code == 200
                assert 'posts' in subject.json

        class Context_토큰이_없는_경우:
            @pytest.fixture
            def subject(self, client):
                url = url_for('UserView:like')
                response = client.get(url)
                return response

            def test_401을_반환한다(self, subject):
                assert subject.status_code == 401

        class Context_토큰에_해당하는_유저가_없는_경우:
            @pytest.fixture
            def auth_token(self):
                return create_access_token(identity=0)

            def test_404를_반환한다(self, subject):
                assert subject.status_code == 404