import os
import datetime
import unittest
import urllib.parse as urlparse
from werkzeug.security import generate_password_hash
import sqlalchemy.exc

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

            r1test = session.query(models.Ranks).filter_by(rank=1).first()
            r2test = session.query(models.Ranks).filter_by(rank=2).first()
            r3test = session.query(models.Ranks).filter_by(rank=3).first()
            self.assertEqual(r1test.rankdesc, 'good')
            self.assertEqual(r2test.rankdesc, 'ok')
            self.assertEqual(r3test.rankdesc, 'bad')
        except sqlalchemy.exc.DataError as error:
            print(error)

    def testUserCreation(self):
        '''Create user'''
        self.user = models.Users(username='todd', email='todd.hanssen@gmail.com', password=generate_password_hash('welcome1'))

        session.add(self.user)
        session.commit()

        utest = session.query(models.Users).filter_by(email='todd.hanssen@gmail.com').first()

        self.assertEqual(utest.username, 'todd')

    def testGoal(self):
        '''Create goal entries'''
        self.user = models.Users(username='todd', email='todd.hanssen@gmail.com', password=generate_password_hash('welcome1'))

        session.add(self.user)
        session.commit()

        goal = models.Goals(user_id=self.user.id, weight_goal=150, health_goal=.5)

        session.add(goal)
        session.commit()

        gtest = session.query(models.Goals) \
            .filter_by(user_id=self.user.id) \
            .first()

        self.assertEqual(gtest.weight_goal, 150)

    def testFoodDiary(self):
        '''Create food entries'''
        now = datetime.datetime.now().strftime("%Y-%m-%d")

        self.user = models.Users(username='todd', email='todd.hanssen@gmail.com', password=generate_password_hash('welcome1'))

        session.add(self.user)
        session.commit()

        rank1 = models.Ranks(rank=1, rankdesc='Good')
        rank2 = models.Ranks(rank=2, rankdesc='Ok')
        rank3 = models.Ranks(rank=3, rankdesc='Bad')
        session.add_all([rank1, rank2, rank3])
        session.commit()

        food1 = models.Food(food='TEST FOOD 1', food_date=now, rank_id=1, user_id=self.user.id)
        food2 = models.Food(food='TEST FOOD 1', food_date=now, rank_id=2, user_id=self.user.id)
        food3 = models.Food(food='TEST FOOD 1', food_date=now, rank_id=3, user_id=self.user.id)

        session.add_all([food1, food2, food3])
        session.commit()

        foodcount = session.query(models.Food).count()

        self.assertEqual(foodcount, 3)

    def testWeightEntries(self):
        '''Create weight entries'''
        now = datetime.datetime.now().strftime("%Y-%m-%d")

        self.user = models.Users(username='todd', email='todd.hanssen@gmail.com', password=generate_password_hash('welcome1'))

        session.add(self.user)
        session.commit()

        weight = models.Weight(weight=200, weight_date=now, user_id=self.user.id)
        session.add(weight)
        session.commit()

        testweight = session.query(models.Weight) \
            .filter_by(user_id = self.user.id) \
            .filter_by(weight=200) \
            .first()

        self.assertEqual(testweight.weight, 200)

    def tearDown(self):
        '''Database tearDown'''
        session.close()
        Base.metadata.drop_all(engine)
if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    unittest.main()
