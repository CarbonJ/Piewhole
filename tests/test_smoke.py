import os
import unittest
import urllib.parse as urlparse
from werkzeug.security import generate_password_hash

#Configuration to use testing config
if not 'CONFIG_PATH' in os.environ:
    os.environ['CONFIG_PATH'] = 'piewhole.config.TestingConfig'

#from piewhole import piewhole
from piewhole import models
from piewhole.database import Base, engine, session

print("CONFIG_PATH: {}".format(os.environ['CONFIG_PATH']))
print()

class testDatabase(unittest.TestCase):
    def setUp(self):
        '''Database setUp'''
        Base.metadata.create_all(engine)

    def testRank(self):
        '''Create ranks'''
        try:
            self.rank1 = models.Ranks(rank=1, rankdesc='good')
            self.rank2 = models.Ranks(rank=2, rankdesc='ok')
            self.rank3 = models.Ranks(rank=3, rankdesc='bad')

            session.add_all([self.rank1, self.rank2, self.rank3])
            session.commit()
            # How to catch error when rank='Todd'
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def testUserCreation(self):
        '''Create user'''
        self.user = models.User(username='todd', email='todd.hanssen@gmail.com', password=generate_password_hash('welcome1'))

        session.add(self.user)
        session.commit()

    def testGoal(self):
        '''Create food entries'''
        pass

    def tearDown(self):
        '''Database tearDown'''
        session.close()
        Base.metadata.drop_all(engine)
if __name__ == '__main__':
    Base.metadata.drop_all(engine)
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