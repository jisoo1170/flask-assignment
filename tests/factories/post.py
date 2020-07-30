import factory
from factory import fuzzy
from factory.mongoengine import MongoEngineFactory
from random import randrange

from tests.factories.user import UserFactory
from app.models.post import Post


class PostFactory(MongoEngineFactory):
    class Meta:
        model = Post

    user = factory.SubFactory(UserFactory)
    title = fuzzy.FuzzyText(length=10)
    content = factory.Faker('text')
    tags = factory.List(['tag1', 'tag2', 'tag3'])
    likes = factory.List([factory.SubFactory(UserFactory)])
    num_of_likes = factory.LazyAttribute(lambda p: len(p.likes))
    num_of_views = randrange(50)
