import os



# default config
class BaseConfig:
    DEBUG = False
    SECRET_KEY =os.environ['SECRET_KEY']
    S3_KEY=os.environ['S3_KEY']
    S3_SECRET=os.environ['S3_SECRET']
    MAIL_SERVER =os.environ['MAIL_SERVER']
    MAIL_PORT= 587
    MAIL_USE_TLS= True
    MAIL_USERNAME= os.environ.get('EMAIL_USER')
    MAIL_PASSWORD= os.environ.get('EMAIL_PASS')

    if 'RDS_HOSTNAME' in os.environ:
        DATABASE = {
    'NAME': os.environ['RDS_DB_NAME'],
    'USER': os.environ['RDS_USERNAME'],
    'PASSWORD': os.environ['RDS_PASSWORD'],
    'HOST': os.environ['RDS_HOSTNAME'],
    'PORT': os.environ['RDS_PORT'],
    }
        SQLALCHEMY_DATABASE_URI = 'postgresql://%(USER)s:%(PASSWORD)s@%(HOST)s:%(PORT)s/%(NAME)s' % DATABASE
        FILE_URL= os.environ['FILE_URL'],
        USE_TF = True
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
        FILE_URL="./static/image/"
        USE_TF = False
        
class TestConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    FILE_URL="./static/image/"

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    USE_TF = False


class ProductionConfig(BaseConfig):
    DEBUG = False
