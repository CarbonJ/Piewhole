import os

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://justin:justin@localhost:5432/piewhole'
    DEBUG = False
    SECRET_KEY = os.environ.get("PIEWHOLEKEY", "")

class HerokuConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgres://gtqwxmqbjngadn:__ZudovRFB3HxFUT4EKt09jsHd@ec2-54-83-10-210.compute-1.amazonaws.com:5432/d5272decs0ohn9'
    DEBUG = False
    SECRET_KEY = 'couchheadphoneshorsemodel'

class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://justin:justin@localhost:5432/piewhole_test'
    DEBUG = True
    SECRET_KEY = 'piewholetesting'

class TravisConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/piewhole_test'
    DEBUG = True
    SECRET_KEY = 'This is not really a secret'