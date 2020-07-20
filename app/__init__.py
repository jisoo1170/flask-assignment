# flask 모듈에서 Flask 클래스를 가져옴
from flask import Flask
from flask_restplus import Api
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # 디비 연결
    from flask_mongoengine import MongoEngine
    db = MongoEngine(app)

    # api 등록
    from app.views import board, comment, search, user
    user.UserView.register(app)
    board.BoardView.register(app)
    comment.CommentView.register(app)
    comment.RecommentView.register(app)
    search.SearchView.register(app)

    # swagger
    api = Api(app, version='1.0', title='게시판', description='게시 등록,수정,삭제,조회 API입니다')

    # jwt
    jwt = JWTManager(app)
    print(app.url_map)

    # error
    from app.error import page_not_found
    app.register_error_handler(404, page_not_found)

    return app
