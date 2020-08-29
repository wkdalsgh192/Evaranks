from flask import flash, redirect, render_template, request, \
    session, url_for, Blueprint,abort
from project.models import User, bcrypt
from functools import wraps
from flask_login import current_user, login_user,logout_user,login_required
from application import db,application,s3,file_url,upload_fn
from PIL import Image
from project.models import Fashion,User,FashionScore
from werkzeug import secure_filename

from datetime import datetime
import os
import secrets

################
#### config ####
################

language_blueprint = Blueprint(
    'language', __name__,
    template_folder = 'templates'
)

@language_blueprint.route('/language')
def language():
    
    return render_template('language.html')
