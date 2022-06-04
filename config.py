import os

TOP_LEVEL_DIR = os.path.dirname(os.path.abspath('__file__'))

SECRET_KEY = os.environ.get('SECRET_KEY') or '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

FLASKY_MAIL_SUBJECT_PREFIX = '[Gomes]'
FLASKY_MAIL_SENDER = 'GOMES ADMIN <eliaspbareia@gmail.com>'
FLASKY_ADMIN = os.environ.get('ADMIN')
CSRF_ENABLED = True

SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_DATABASE_URI ='sqlite:///database/app.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///../finance.db'

SQLALCHEMY_ECHO = True

POSTS_PER_PAGE = 3

# Uploads
UPLOADS_DEFAULT_DEST = TOP_LEVEL_DIR + '/application/static/uploads/'
UPLOADS_DEFAULT_URL = 'http://localhost:5000/uploads/'

UPLOADED_IMAGES_DEST = TOP_LEVEL_DIR + '/application/static/uploads/'
UPLOADED_IMAGES_URL = 'http://localhost:5000/uploads/'