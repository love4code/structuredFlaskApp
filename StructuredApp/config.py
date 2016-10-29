import os
# Application Configurations.
# Applications often need several configuration sets.
# The best example of this is the need to use different databases during
# development, testing, and production so that they don’t interfere
# with each other.

# The Config base class contains settings that are common to all
#  configurations;
# the different subclasses define settings that are specific to a
# configuration.
#
# Additional configurations can be added as needed.

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECTRET_KEY') or \
                 'xH30458JSu3el0rT374980j4K2'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@myapp.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'markagrover85@gmail.com'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smpt.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or \
                    'markagrover85@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'installs'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig
}
# The SQLALCHEMY_DATABASE_URI variable is assigned different values under
# each of the three configurations. This enables the application to run
# under different configurations, each using a different database.


