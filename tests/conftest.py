import pytest


@pytest.fixture(scope="session")
def app():
    from app import create_app
    app = create_app()
    return app


@pytest.fixture(scope="session", autouse=True)
def app_context(app):
    # GET, POST 처리하기 위해서 app_context 필요
    ctx = app.app_context()
    ctx.push()
    yield
    # 테스트 환경 정리
    ctx.pop()


@pytest.fixture(scope='function', autouse=True)
def db(app):
    import mongoengine
    mongoengine.connect(host=app.config['MONGODB_HOST'])
    yield
    mongoengine.disconnect()
