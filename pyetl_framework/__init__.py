import os
from .app import App as App
from .worker import Worker as Worker

from .lib import ETLJob as ETLJob
from .lib import Pipeline as Pipeline

from .lib import Extractor as Extractor
from .lib import Transformer as Transformer
from .lib import Loader as Loader

def run_flask():
    hostname = os.getenv('FLASK_HOSTNAME', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', '5000'))

    print('Starting pyetl flask server with hostname: {}, port: {}'.format(hostname, port))
    print('Change hostname and port by setting env vars: FLASK_HOSTNAME and FLASK_PORT')

    App.run(hostname, port)

def run_worker():
    Worker.run()
