import os
import unittest
import urllib.parse as urlparse
from werkzeug.security import generate_password_hash

from piewhole import piewhole
from piewhole import models
from piewhole.database import Base, engine, session

#Configuration to use testing config
if not 'CONFIG_PATH' in os.environ:
    os.environ['CONFIG_PATH'] = 'piewhole.config.TestingConfig'

print("CONFIG_PATH: {}".format(os.environ['CONFIG_PATH']))
print()

class testDatabase(unittest.TestCase):
    def testDatabaseSetup(self):
        '''Database connection, setup, and single user'''
        self.client = piewhole.test_client()
        Base.metadata.create_all(engine)

        self.user = models.User(username='justin', email='justin.hanssen@gmail.com', password=generate_password_hash('welcome1'))

        session.add(self.user)
        session.commit()

    def testUser(self):
        '''Create user and entries directly into database'''
        self.client = piewhole.test_client()
        self.user = models.User(username='todd', email='todd.hanssen@gmail.com', password=generate_password_hash('welcome1'))

        session.add(self.user)
        session.commit()

    def testDatabaseTearDown(self):
        '''Tear down of database'''
        session.close()
        Base.metadata.drop_all(engine)
if __name__ == '__main__':
    unittest.main()



# class Weight(Base):
#     __tablename__ = 'Weight'
#     id = Column(Integer, primary_key=True, unique=True)
#     weight = Column(Float)
#     weight_date = Column(Date)
#     weight_delta = Column(Float)
#     user_id = Column(Integer, ForeignKey('User.id'))


# class Food(Base):
#     __tablename__ = 'Food'
#     id = Column(Integer, primary_key=True, unique=True)
#     food = Column(String)
#     food_date = Column(Date)
#     rank_id = Column(Integer, ForeignKey('Ranks.id'))
#     user_id = Column(Integer, ForeignKey('User.id'))


# class User(Base):
#     __tablename__ = 'User'
#     id = Column(Integer, primary_key=True, unique=True)
#     username = Column(String)
#     email = Column(String, unique=True)
#     password = Column(String)


# class Goals(Base):
#     __tablename__ = 'Goals'
#     id = Column(Integer, primary_key=True, unique=True)
#     user_id = Column(Integer, ForeignKey('User.id'))
#     weight_goal = Column(String)
#     health_goal = Column(Float)