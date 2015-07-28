import os

class DevelopmentConfig(object):
    SQL_ALCHEMY_DATABASE_URI = 'postgresql://justin:justin@localhost:5432/piewhole'
    DEBUG = True

class TestingConfig(object):
    SQL_ALCHEMY_DATABASE_URI = 'postgresql://justin:justin@localhost:5432/piewhole_test'
    DEBUG = True
    SECRET_KEY = 'piewholetesting'