import datetime


class Config(object):
    JSON_AS_ASCII = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=20)
    SECRET_KEY = '@6f%$q&arc4cqnnw!q31@%#b6yly_v1pw6j6celpryeewio&@8'
    MONGODB_DB = 'tutorial'


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    MONGODB_HOST = 'mongomock://localhost'
    TESTING = True


config_by_name = dict(dev=DevelopmentConfig, test=TestConfig)
