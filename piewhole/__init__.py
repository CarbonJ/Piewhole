import os
from flask import Flask

piewhole = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "piewhole.config.DevelopmentConfig")
piewhole.config.from_object(config_path)


from . import views
# assumes filters used
#from . import filters