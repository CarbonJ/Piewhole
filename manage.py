import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from piewhole import piewhole
from piewhole.database import session
from piewhole.database import Base
from piewhole.models import User
from getpass import getpass
from werkzeug.security import generate_password_hash

manager = Manager(piewhole)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    piewhole.run(host='locke.local', port=port, debug=True)

@manager.command
def adduser():
    name = input("Name: ")
    email = input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print('User with that email address already exists')
        return

    password = ''
    password_2 = ''
    while not (password and password_2) or password != password_2:
        password = getpass('Password: ')
        password_2 = getpass('Re-enter password: ')
    user = User(username=name, email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()


class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata
migrate = Migrate(piewhole, DB(Base.metadata))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
