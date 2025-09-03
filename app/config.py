import os
from dotenv import load_dotenv
load_dotenv()
import datetime

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    # Set JWT access token expiration using timedelta
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
    # Set JWT refresh token expiration using timedelta (7 days, as mentioned)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 7)))
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_TOKEN_LOCATION='cookies'
    JWT_COOKIE_CSRF_PROTECT=False

    # Flask-Mail Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 465))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'False') == 'True'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_SUPPRESS_SEND = os.getenv('MAIL_SUPPRESS_SEND', 'False') == 'True'
    MAIL_DEBUG = os.getenv('MAIL_DEBUG', 'False') == 'True'

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEVELOPMENT_DATABASE_URL")

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("PRODUCTION_DATABASE_URL")
    JWT_COOKIE_SECURE = os.getenv('JWT_COOKIE_SECURE', 'True') == 'True'
    JWT_COOKIE_SAMESITE = os.getenv('JWT_COOKIE_SAMESITE', 'Lax')

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
