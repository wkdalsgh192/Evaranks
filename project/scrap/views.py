from flask import flash, redirect, render_template, request, \
    session, url_for, Blueprint,abort
from project.models import User, bcrypt,Scrap
from functools import wraps
from flask_login import current_user, login_user,logout_user,login_required
from application import db,application
from PIL import Image
from project.models import Fashion,User,FashionScore
from werkzeug import secure_filename

from datetime import datetime
import os
import secrets


################
#### config ####
################

scrap_blueprint = Blueprint(
    'scrap', __name__,
    template_folder='templates'
)


@scrap_blueprint.route("/scrapping/<int:fashionid>")
@login_required
def scrap_post(fashionid):

    fashion=FashionScore.query.filter_by(id=fashionid).first()
    print('current_user',current_user.id)
    if current_user.scrap_fashion(fashion):
        db.session.commit()
        flash('내 룩북에 추가되었습니다!','success')
    else:
        flash('이미 내 룩북에 있어요!','warning')
    #return redirect(url_for('lookbook.main'))
    return redirect(request.referrer)


@scrap_blueprint.route("/remove_scrap/<int:fashionid>")
@login_required
def remove_scrap(fashionid):

    fashion=FashionScore.query.filter_by(id=fashionid).first()

    current_user.delete_scrap(fashion)
    db.session.commit()
    flash('Scrap 에서 제거완료!','success')
    return redirect(request.referrer)
