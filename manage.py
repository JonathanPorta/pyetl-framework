import os
from flask.ext.script import Manager

from app import app as MyApp

MyApp.config.from_object(os.environ['APP_SETTINGS'])

manager = Manager(MyApp)

if __name__ == '__main__':
    manager.run()
