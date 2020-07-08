# flask 모듈에서 Flask 클래스를 가져옴
from flask import Flask
from app.views import BoardView


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # 디비 연결
    from mongoengine import connect
    connect('tutorial')

    # api 등록
    BoardView.register(app)

    return app
