from flask.ext.login import LoginManager

from piewhole import piewhole
from .database import session
from .models import User

login_manager = LoginManager()
login_manager.init_app(piewhole)

login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'

@login_manager.user_loader
def load_user(id):
    return session.query(User).get(int(id))