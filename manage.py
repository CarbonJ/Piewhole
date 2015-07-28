import os
from flask.ext.script import Manager


manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='10.0.10.21', port=port, debug=True)

if __name__ == '__main__':
    manager.run()
