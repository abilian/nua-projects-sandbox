from app.main import create_app

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_USERNAME = "test"
    MAIL_PASSWORD = "test"
    MAIL_FROM = "test@example.com"
    MAIL_SERVER = "localhost"


def test_smoke():
    app = create_app(TestConfig)
    assert app
