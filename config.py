from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    """
    La config de base du serveur FLASK
    """
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'change-me'
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RECAPTCHA_PUBLIC_KEY = "change-me"
    RECAPTCHA_PRIVATE_KEY = "change-me"


class ProductionConfig(Config):
    """
    La config de production (!HAZARD!)
    """
    ENV= "production"
    DEBUG = False
    DEVELOPMENT = False


class DevelopmentConfig(Config):
    """
    La config de développement/Sandbox.
    Go and have fun!
    """
    ENV = "development"
    DEVELOPMENT = True
    DEBUG = True
