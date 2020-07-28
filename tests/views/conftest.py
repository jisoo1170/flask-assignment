import pytest
from flask_jwt_extended import create_access_token

from tests.factories.user import UserFactory


@pytest.fixture
def logged_in_user():
    return UserFactory.create()


@pytest.fixture
def auth_token(logged_in_user):
    return create_access_token(identity=str(logged_in_user.id))


@pytest.fixture
def headers(auth_token):
    return {'Authorization': f'Bearer {auth_token}'}


