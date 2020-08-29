from application import db,application,s3,file_url,upload_fn
from flask import flash, redirect, session, url_for, render_template, Blueprint,request,abort
from project.models import Fashion,User,Calendar
from functools import wraps
import os
from flask_login import current_user, login_user,logout_user,login_required
from datetime import datetime

################
#### config ####
################

calendar_blueprint = Blueprint(
    'calendar', __name__,
    template_folder='templates',
)

allowed_img_file = ["JPEG", "JPG", "PNG", "GIF"]


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in allowed_img_file:
        return True
    else:
        return False



@calendar_blueprint.route('/calendar')
@login_required
def calendar():

    queries = Calendar.query.filter_by(author_id=current_user.id).with_entities(Calendar.date,Calendar.img_url).all()
    queries=dict(queries)

    return render_template('calendar.html',queries=queries)  # render a template


@calendar_blueprint.route('/calendar_submit',methods=['GET','POST'])
@login_required
def calendar_submit():

    unique_id=datetime.now().strftime('%Y%m%d%H%M%S')
    error=None

    if request.method == 'POST':
        imagefile = request.files['imagefile']
        date=request.form['date']

        _,f_ext=os.path.splitext(imagefile.filename)

        picture_name='calendar_'+str(current_user.id)+'_'+unique_id+f_ext
        picture_path=os.path.join(file_url,picture_name)
        upload_fn(imagefile,'socksclub',picture_name)

        print('upload_fn',upload_fn)


        if allowed_image(imagefile.filename):

            calendar_post=Calendar(date=date,img_url=picture_path,author=current_user)
            db.session.add(calendar_post)
            db.session.commit()


            return redirect(url_for('calendar.calendar'))
        else:
            error='jpg or png file required'
            flash(error,'warning')
    return redirect(request.referrer)

@calendar_blueprint.route('/calendar/<int:date>/calendar_delete', methods=['GET', 'POST'])
@login_required
def calendar_delete(date):
    calendar=Calendar.query.filter_by(author_id=current_user.id,date=date).first()
    error=None

    if calendar.author_id!=current_user.id:
        abort(403)

    db.session.delete(calendar)
    db.session.commit()
    flash('Your post has been deleted!', 'success')

    return redirect(request.referrer)
