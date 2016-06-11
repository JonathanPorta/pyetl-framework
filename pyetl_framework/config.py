import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'supersecret'
    BASE_DIR = basedir

    PIPELINES_PKG = 'pipelines'
    PIPELINES_DIR = os.path.join(basedir, PIPELINES_PKG)

    EXTRACTORS_PKG = 'extractors'
    EXTRACTORS_DIR = os.path.join(basedir, EXTRACTORS_PKG)

    TRANSFORMERS_PKG = 'transformers'
    TRANSFORMERS_DIR = os.path.join(basedir, TRANSFORMERS_PKG)

    LOADERS_PKG = 'loaders'
    LOADERS_DIR = os.path.join(basedir, LOADERS_PKG)

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
