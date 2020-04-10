import os
from datetime import timedelta

ROOT_PATH = os.path.split(os.path.abspath(__name__))[0]

DEBUG = True
JWT_SECRET_KEY = 'shop'
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(
   os.path.join(ROOT_PATH, 's_shop_flask.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
user = 'shop'
passwd = 'shopadmin'
db = 'shopdb'

# SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{passwd}@10.10.10.105:6606/{db}'

JWT_AUTH_USERNAME_KEY = 'username'
JWT_AUTH_PASSWORD_KEY = 'password'
JWT_AUTH_HEADER_PREFIX = 'JWT'
JWT_EXPIRATION_DELTA = timedelta(days=30)
JWT_ALGORITHM = 'HS256'
JWT_REQUIRED_CLAIMS =  ['exp', 'iat', 'nbf']
