import datetime


class Config(object):
    DEBUG = True
    JSON_AS_ASCII = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=20)
