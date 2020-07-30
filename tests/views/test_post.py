from random import randrange

import pytest
from bson import ObjectId
from factory.fuzzy import FuzzyText
from flask import url_for
from flask_jwt_extended import create_access_token
from funcy import pairwise

from tests.factories.post import PostFactory
from tests.factories.user import UserFactory


class Describe_PostView:
    class Describe_index:
        @pytest.fixture
        def subject(self, client):
            url = url_for('PostView:index')
            response = client.get(url)
            return response

        class Context_정상_요청:
            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200
                assert 'items' in subject.json

        class Context_좋아요_정렬하는_경우:
            @pytest.fixture(autouse=True)
            def posts(self):
                PostFactory.create(num_of_likes=randrange(50))
                PostFactory.create(num_of_likes=randrange(50))
                PostFactory.create(num_of_likes=randrange(50))
                PostFactory.create(num_of_likes=randrange(50))
                PostFactory.create(num_of_likes=randrange(50))

            @pytest.fixture
            def subject(self, client):
                url = url_for('PostView:index')
                params = {'order': 'num_of_likes'}
                response = client.get(url, query_string=params)
                return response

            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200
                assert 'items' in subject.json
                posts = subject.json['items']
                for post1, post2 in pairwise(posts):
                    assert post1['num_of_likes'] >= post2['num_of_likes']

        class Context_조회수_정렬하는_경우:
            @pytest.fixture(autouse=True)
            def posts(self):
                PostFactory.create(num_of_views=randrange(50))
                PostFactory.create(num_of_views=randrange(50))
                PostFactory.create(num_of_views=randrange(50))
                PostFactory.create(num_of_views=randrange(50))
                PostFactory.create(num_of_views=randrange(50))

            @pytest.fixture
            def subject(self, client):
                url = url_for('PostView:index')
                params = {'order': 'num_of_views'}
                response = client.get(url, query_string=params)
                return response

            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200
                assert 'items' in subject.json
                posts = subject.json['items']
                for post1, post2 in pairwise(posts):
                    assert post1['num_of_views'] >= post2['num_of_views']

        class Context_태그_검색을_하는_경우:
            @pytest.fixture(autouse=True)
            def posts(self):
                PostFactory.create(tags=['1', '2'])
                PostFactory.create(tags=['1', '3'])
                PostFactory.create(tags=['1'])
                PostFactory.create(tags=['2'])
                PostFactory.create(tags=['3'])

            @pytest.fixture
            def subject(self, client):
                url = url_for('PostView:index')
                params = {'tag': '1'}
                response = client.get(url, query_string=params)
                print(response)
                return response

            def test_200이_반환된다(self, subject):
                assert subject.status_code == 200
                assert 'items' in subject.json
                posts = subject.json['items']
                for post in posts:
                    assert '1' in post['tags']

    class Describe_post:
        @pytest.fixture()
        def form(self):
            return {'title': 'test title', 'content': 'test content'}

        @pytest.fixture
        def subject(self, client, headers, form):
            url = url_for('PostView:post')
            response = client.post(url, headers=headers, json=form)
            return response

        class Context_정상_요청:
            def test_게시글이_작성된다_201(self, subject):
                assert subject.status_code == 201
                assert subject.json['title'] == 'test title'

        class Context_제목이_없는_경우:
            @pytest.fixture()
            def form(self):
                return {'content': 'test content'}

            def test_400이_반환된다(self, subject):
                assert subject.status_code == 400

        class Context_내용이_없는_경우:
            @pytest.fixture()
            def form(self):
                return {'title': 'test title'}

            def test_400이_반환된다(self, subject):
                assert subject.status_code == 400

    class Describe_get:
        @pytest.fixture
        def created_post(self, logged_in_user):
            return PostFactory.create(user=logged_in_user)

        @pytest.fixture
        def post_id_to_get(self, created_post):
            return created_post.id

        @pytest.fixture
        def subject(self, client, headers, post_id_to_get):
            url = url_for('PostView:get', post_id=post_id_to_get)
            response = client.get(url, headers=headers)
            return response

        class Context_존재하는_게시글_조회:
            def test_200이_반환된다(self, subject, created_post):
                assert subject.status_code == 200
                assert subject.json['title'] == created_post.title
                assert subject.json['content'] == created_post.content
                assert subject.json['num_of_views'] == created_post.num_of_views + 1

        class Context_게시글이_없는_경우:
            @pytest.fixture
            def post_id_to_get(self):
                return ObjectId()

            def test_404가_반환된다(self, subject):
                assert subject.status_code == 404

    class Describe_patch:
        @pytest.fixture
        def created_post(self, logged_in_user):
            return PostFactory.create(user=logged_in_user)

        @pytest.fixture
        def post_id_to_patch(self, created_post):
            return created_post.id

        @pytest.fixture()
        def form(self):
            return {'title': FuzzyText(length=20).fuzz(), 'content': FuzzyText(length=100).fuzz()}

        @pytest.fixture
        def subject(self, client, headers, form, created_post, post_id_to_patch):
            url = url_for('PostView:patch', post_id=post_id_to_patch)
            response = client.patch(url, headers=headers, json=form)
            return response

        class Context_정상_요청:
            def test_200이_반환된다(self, subject, form):
                assert subject.status_code == 200
                assert subject.json['title'] == form['title']
                assert subject.json['content'] == form['content']

        class Context_작성한_사용자가_아닌_경우:
            @pytest.fixture
            def created_post(self):
                return PostFactory.create()

            def test_403을_반환한다(self, subject):
                assert subject.status_code == 403

        class Context_게시글이_없는_경우:
            @pytest.fixture
            def post_id_to_patch(self):
                return ObjectId()

            def test_404를_반환한다(self, subject):
                assert subject.status_code == 404

        class Context_빈_값을_넣는_경우:
            @pytest.fixture()
            def form(self):
                return {'title': '', 'content': ''}

            def test_400를_반환한다(self, subject):
                assert subject.status_code == 400

    class Describe_delete:
        @pytest.fixture
        def created_post(self, logged_in_user):
            return PostFactory.create(user=logged_in_user)

        @pytest.fixture
        def subject(self, client, headers, created_post):
            url = url_for('PostView:delete', id=created_post.id)
            response = client.delete(url, headers=headers)
            return response

        class Context_정상_요청:
            def test_204가_반환된다(self, subject):
                assert subject.status_code == 204

        class Context_작성한_사용자가_아닌_경우:
            @pytest.fixture
            def auth_token(self):
                logged_in_another_user = UserFactory.create()
                return create_access_token(identity=str(logged_in_another_user.id))

            @pytest.fixture
            def subject(self, client, headers, created_post):
                url = url_for('PostView:delete', id=created_post.id)
                response = client.delete(url, headers=headers)
                return response

            def test_403을_반환한다(self, subject):
                assert subject.status_code == 403

    class Describe_like:
        @pytest.fixture
        def created_post(self, logged_in_user):
            return PostFactory.create(user=logged_in_user)

        @pytest.fixture
        def subject(self, client, headers, created_post, logged_in_user):
            url = url_for('PostView:like', id=created_post.id)
            response = client.post(url, headers=headers)
            return response

        class Context_정상_요청:
            def test_200이_반환된다(self, subject, created_post):
                assert subject.status_code == 200
                assert subject.json['num_of_likes'] == created_post.num_of_likes + 1

        class Context_이미_누른_경우:
            @pytest.fixture
            def logged_in_user(self):
                return UserFactory.create()

            @pytest.fixture
            def created_post(self, created_post, logged_in_user):
                created_post.likes.append(logged_in_user)
                created_post.save()
                return created_post

            def test_409가_반환된다(self, subject):
                assert subject.status_code == 409
