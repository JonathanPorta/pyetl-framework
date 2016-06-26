import os
from pyetl_framework import App

hostname = os.getenv('FLASK_HOSTNAME', '127.0.0.1')
port = int(os.getenv('FLASK_PORT', '5000'))

print('Starting pyetl flask server with hostname: {}, port: {}'.format(hostname, port))
print('Change hostname and port by setting env vars: FLASK_HOSTNAME and FLASK_PORT')

App.run(hostname, port)
