import factory
from factory.mongoengine import MongoEngineFactory

from app.models.user import User


class UserFactory(MongoEngineFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.Sequence(lambda n: f'password{n}')
