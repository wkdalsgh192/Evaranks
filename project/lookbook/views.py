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

lookbook_blueprint = Blueprint(
    'lookbook', __name__,
    template_folder='templates'
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


@lookbook_blueprint.route('/new_post',methods=['GET','POST'])
@login_required
def new_post():

    unique_id=datetime.now().strftime('%Y%m%d%H%M%S')
    error=None


    if request.method=='POST':
        imagefile = request.files['imagefile']
        comment=request.form['comment']

        upper=request.form['upper']
        lower=request.form['lower']
        etc=request.form['etc']

        if allowed_image(imagefile.filename):
            _,f_ext=os.path.splitext(imagefile.filename)

            picture_name=str(current_user.id)+'_'+unique_id+f_ext
            picture_path=os.path.join(file_url,picture_name)
            upload_fn(imagefile,'socksclub',picture_name)


            fashion_post=Fashion(pub_date=datetime.now(),img_url=picture_path,author=current_user,fashion_text=comment,upper=upper,lower=lower,etc=etc)
            db.session.add(fashion_post)
            db.session.commit()


            return redirect(url_for('lookbook.main'))
        else:
            error='jpg or png file required'
            flash(error,'warning')
    return redirect(request.referrer)


@lookbook_blueprint.route('/main')
def main():
    page=request.args.get('page',1,type=int)
    queries = FashionScore.query.filter(FashionScore.sharing==1)
    # db.session.commit()
    queries_male=queries.filter(FashionScore.gender=='M').order_by(FashionScore.score.desc()).all()
    queries_female = queries.filter(FashionScore.gender=='F').order_by(FashionScore.score.desc()).all()
    total_queries = queries_male+queries_female
    nums = len(queries_male) + len(queries_female)

    first_male = queries_male[0]
    first_female = queries_female[0]

    else_male = queries_male[1:]
    else_female = queries_female[1:]

    return render_template('lookbook.html',first_male=first_male,first_female=first_female,male_imgs = else_male,female_imgs =else_female,total_queries=total_queries,nums=nums)



@lookbook_blueprint.route('/post/<int:fashion_id>/update_post', methods=['GET', 'POST'])
@login_required
def update_post(fashion_id):
    fashion=Fashion.query.get_or_404(fashion_id)
    error=None
    if fashion.author_id!=current_user.id:
        abort(403)

    if request.method=='POST':
        comment=request.form['comment']
        fashion.fashion_text=comment
        db.session.commit()
        return redirect(request.referrer)

    return render_template('update_image.html',fashion=fashion,error=None)

@lookbook_blueprint.route('/post/<int:fashion_id>/delete_post', methods=['GET', 'POST'])
@login_required
def delete_post(fashion_id):
    fashion=FashionScore.query.get_or_404(fashion_id)
    error=None
    print('here')
    if fashion.author_id!=current_user.id:
        abort(403)
    db.session.delete(fashion)
    db.session.commit()
    flash('Your post has been deleted!', 'success')

    return redirect(request.referrer)
