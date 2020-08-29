from flask import Flask,render_template,flash, redirect,url_for,session,logging,request,g
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from functools import wraps
import os
from flask_login import LoginManager
from flask_mail import Mail
import boto3
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
# from flask_talisman import Talisman




application = Flask(__name__)
application.config.from_object(os.environ['APP_SETTINGS'])
#db connection?
application.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True} 
#application.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
application.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# Talisman(application,content_security_policy=None)


login_manager = LoginManager()
login_manager.init_app(application)

bcrypt = Bcrypt(application)
db = SQLAlchemy(application)

mail=Mail(application)

file_url=application.config['FILE_URL']
USE_TF = application.config['USE_TF']

s3 = boto3.client(
   "s3",
   aws_access_key_id=application.config['S3_KEY'],
   aws_secret_access_key=application.config['S3_SECRET']
)

@application.teardown_request
def close_connection(r):
    try:
        db.session.close_all()
    except:
        print(';??')
        db.session.close()
    return r


def upload_file_to_s3(file, bucket_name, filename,acl="public-read"):
    
    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": "image/jpeg"
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return 'success'


def save_picture(file, bucket_name, filename,acl="public-read"):
    ''''resize img to 125 125 and save pic and return file path'''
    file_abs_path=file_url+filename
    i=Image.open(file)
    i.save(file_abs_path)

    return filename


if 'amazonaws' in file_url:
    upload_fn=upload_file_to_s3
else:
    upload_fn=save_picture

if USE_TF:
    from tensorflow.keras.models import load_model,Model
    '''load tensorflow model'''
    model_name='./project/rank/model/VGG16-transferlearning-10'
    new_model = load_model(model_name)
    extraction_model=Model(inputs=new_model.input, outputs=(new_model.layers[-2].output, new_model.output))
    # new_model = None
    # extraction_model=None
    print('model loaded')
else:
    new_model = None
    extraction_model=None
    

from project.home.views import home_blueprint
from project.users.views import users_blueprint
from project.lookbook.views import lookbook_blueprint
from project.scrap.views import scrap_blueprint
from project.calendar.views import calendar_blueprint
from project.rank.views import rank_blueprint
from project.language.views import language_blueprint

application.register_blueprint(users_blueprint)
application.register_blueprint(home_blueprint)
application.register_blueprint(lookbook_blueprint)
application.register_blueprint(scrap_blueprint)
application.register_blueprint(calendar_blueprint)
application.register_blueprint(rank_blueprint)
application.register_blueprint(language_blueprint)


from project.models import User


login_manager.login_view = "users.login"
login_manager.login_message_category = 'info'


#수상하다
@login_manager.user_loader
def load_user(user_id):
    try:
        user = User.query.get(int(user_id))
        db.session.remove()
        return user
    except:
        db.session.remove()
        return None


if __name__ == '__main__':
    application.run()