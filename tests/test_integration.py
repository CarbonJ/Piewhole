import os
import unittest
import urllib.parse as urlparse
from werkzeug.security import generate_password_hash

from piewhole import app
from piewhole import models
from piewhole.database import Base, engine, session

#Configuration to use testing config
if not 'CONFIG_PATH' in os.environ:
    os.environ['CONFIG_PATH'] = 'piewhole.config.TestingConfig'

class testDatabase(unittest.TestCase):
    def testDatabaseSetup(self):
        '''Database connection, setup, and single user'''
        self.client = app.test_client()
        Base.metadata.create_all(engine)

        self.user = models.User(username='justin', email='justin.hanssen@gmail.com', password=generate_password_hash('welcome1'))

        session.add(self.user)
        session.commit()

    def testDatabaseTearDown(self):
        '''Tear down of database'''
        session.close()
        Base.metadata.drop_all(engine)
if __name__ == '__main__':
    unittest.main()