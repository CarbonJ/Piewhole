import os

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://justin:justin@localhost:5432/piewhole'
    DEBUG = True

class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://justin:justin@localhost:5432/piewhole_test'
    DEBUG = True
    SECRET_KEY = 'piewholetesting'

class TravisConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/piewhole_test'
    debug = True
    SECRET_KEY = 'This is not really a secret'