import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from piewhole import piewhole
from piewhole.database import Base

manager = Manager(piewhole)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    piewhole.run(host='locke.local', port=port, debug=True)

class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata
migrate = Migrate(piewhole, DB(Base.metadata))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
