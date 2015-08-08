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

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        # Wipe any residual db items
        Base.metadata.drop_all(engine)

        port = int(os.environ.get('PORT', 8080))

        self.browser = Browser("phantomjs")

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = models.User(username="Alice", email="alice@example.com",
                                password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

        self.process = multiprocessing.Process(target=piewhole.run(host='127.0.0.1', port=port))
        self.process.start()
        time.sleep(1)

    def testLoginCorrect(self):
        self.browser.visit("http://127.0.0.1:8080/login")
        self.browser.fill("email", "alice@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/")

    # def testLoginIncorrect(self):
    #     self.browser.visit("http://0.0.0.0:8080/login")
    #     self.browser.fill("email", "bob@example.com")
    #     self.browser.fill("password", "test")
    #     button = self.browser.find_by_css("button[type=submit]")
    #     button.click()
    #     self.assertEqual(self.browser.url, "http://0.0.0.0:8080/login")

    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)
        self.process.terminate()
        session.close()
        engine.dispose()
        self.browser.quit()

if __name__ == "__main__":
    unittest.main()