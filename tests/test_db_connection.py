import os
import unittest
import piewhole

#Configuration to use  testing config

if not 'CONFIG_PATH' in os.environ:
    os.environ['CONFIG_PATH'] = 'piewhole.config.TestingConfig'

class DatabaseConnectionTest(unittest.TestCase):
    print('DatabaseConnectionTest')
    pass

if __name__ == '__main__':
    unittest.main()