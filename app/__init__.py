# flask 모듈에서 Flask 클래스를 가져옴
from flask import Flask
from flask_restplus import Api


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # 디비 연결
    from mongoengine import connect
    connect('tutorial')

    # api 등록
    from app.views import register_api
    register_api(app)

    # swagger
    api = Api(app, version='1.0', title='게시판', description='게시 등록,수정,삭제,조회 API입니다')

    return app
