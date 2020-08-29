import os
from application import db
from flask import flash, redirect, session, url_for, render_template, Blueprint
from functools import wraps
from flask_login import current_user

################
#### config ####
################

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates',
)

@home_blueprint.route('/home')
def home():
    return render_template('socks_club.html')  # render a template
