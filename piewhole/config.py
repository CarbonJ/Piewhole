import os

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://justin:justin@localhost:5432/piewhole'
    DEBUG = True
    SECRET_KEY = os.environ.get("PIEWHOLEKEY", "")

class HerokuConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://gtqwxmqbjngadn:gtqwxmqbjngadn@localhost:5432/d5272decs0ohn9'
    DEBUG = True
    SECRET_KEY = os.environ.get('JOLDERSHAMMER')

class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://justin:justin@localhost:5432/piewhole_test'
    DEBUG = True
    SECRET_KEY = 'piewholetesting'

class TravisConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/piewhole_test'
    DEBUG = True
    SECRET_KEY = 'This is not really a secret'