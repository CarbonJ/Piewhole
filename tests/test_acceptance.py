import os
import unittest
import multiprocessing
import time
import urllib.parse as urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser


# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "piewhole.config.TestingConfig"

from piewhole import piewhole
from piewhole import models
from piewhole.database import Base, engine, session

print("START TESTING")

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test Setup """
        print("IN SETUP")
        self.browser = Browser("phantomjs")
        Base.metadata.create_all(engine)

        self.process = multiprocessing.Process(target=piewhole.run(debug=True))
        self.process.start()
        time.sleep(1)

    def testLogin(self):
        print("IN TEST")
        pass

    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        print("IN TEARDOWN")
        self.process.terminate()
        session.close()
        engine.dispose()
        self.browser.quit()
        Base.metadata.drop_all(engine)


if __name__ == "__main__":
    unittest.main()