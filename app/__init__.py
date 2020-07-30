# flask 모듈에서 Flask 클래스를 가져옴
import os

from flask import Flask
from flask_jwt_extended import JWTManager
from .config import config_by_name

from app.views import post, comment, user


def create_app():
    app = Flask(__name__)
    # app.config.from_object('app.config.DevelopmentConfig')
    config_name = os.getenv('APP_ENV') or 'local'
    app.config.from_object(config_by_name[config_name])

    # 디비 연결
    from flask_mongoengine import MongoEngine
    db = MongoEngine(app)

    # api 등록
    from app.views import post, comment, user
    user.UserView.register(app, route_base='users')
    post.PostView.register(app, route_base='posts')
    comment.CommentView.register(app, route_base='posts/<post_id>/comments')
    comment.RecommentView.register(app, route_base='posts/<post_id>/comments/<comment_id>/recomments')

    # jwt
    jwt = JWTManager(app)
    # print(app.url_map)
    # error
    from app.errors import page_not_found
    app.register_error_handler(404, page_not_found)

    return app
