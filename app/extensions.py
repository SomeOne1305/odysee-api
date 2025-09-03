from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import redis


db = SQLAlchemy()
CacheStorage = redis.Redis(
	host='127.0.0.1',
	port=6379,
)

mailer = Mail()
