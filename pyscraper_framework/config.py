import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'supersecret'
    BASE_DIR = basedir
    SCRAPERS_PKG = 'scrapers'
    SCRAPERS_DIR = os.path.join(basedir, SCRAPERS_PKG)
    JOBS_PKG = 'jobs'
    JOBS_DIR = os.path.join(basedir, JOBS_PKG)

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
