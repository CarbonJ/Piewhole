import os

class DevelopmentConfig(object):
    SQL_ALCHEMY_DATABASE_URI = "postgresql://justin:justin@localhost:5432/piewhole"
    DEBUG = True