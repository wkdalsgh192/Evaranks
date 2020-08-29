from flask import flash, redirect, render_template, request, \
    session, url_for, Blueprint
from project.models import User, bcrypt,Fashion,Scrap,FashionScore
from functools import wraps
from .forms import LoginForm,RegistrationForm,UpdateAccountForm,PostForm,RequestResetForm, ResetPasswordForm
from flask_login import current_user, login_user,logout_user,login_required
from flask_mail import Message
from application import db,application,mail,s3,file_url,upload_fn
from PIL import Image

import os
import secrets

users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)


# route for handling the login page logic
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated():
        return redirect(url_for('rank.rank'))
    error = None
    form=LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user=User.query.filter_by(name=request.form['username']).first()
            if user is not None and bcrypt.check_password_hash(user.password,request.form['password']):
                #session['logged_in'] = True
                login_user(user, remember=form.remember.data)
                print('login')
                #flash('You were logged in.')
                return redirect(url_for('rank.rank'))

            else:
                error = 'Invalid username or password.'

    return render_template('login.html',form=form,error=error)


@users_blueprint.route('/naver_login/<email>/<username>', methods=['GET', 'POST'])
def naver_login(email,username):
    #중복 이메일 어떻게 처리하지???
    user=User.query.filter_by(email=email).first()
    if user is None:
        user = User(
            name=username,
            email=email,
            seo='naver',
            password=''
        )

        db.session.add(user)
        db.session.commit()
        login_user(user)
    else:
        print('I am already registered')
        login_user(user)
        #flash('You were logged in.')
    return redirect(url_for('rank.rank'))    
   


@users_blueprint.route('/naver_callback', methods=['GET', 'POST'])
def naver_callback():

    return render_template('login_callback.html')

@users_blueprint.route('/facebook_callback/<username>', methods=['GET', 'POST'])
def facebook_login(username):
    #중복 이메일 어떻게 처리하지???
    user=User.query.filter_by(name=username).filter_by(seo="facebook").first()
    if user is None:
        user = User(
            name=username,
            email='facebook@facebook.com',
            seo='facebook',
            instagram='',
            password=''
        )

        db.session.add(user)
        db.session.commit()
        login_user(user)
    else:
        print('I am already registered')
        login_user(user)
        #flash('You were logged in.')
    return redirect(url_for('rank.rank'))    



@users_blueprint.route('/logout')
def logout():
    #session.pop('logged_in', None)
    logout_user()
 #   flash('You were logged out.')
    return redirect(url_for('home.home'))


@users_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated():
        return redirect(url_for('home.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data,
            instagram=form.instagram.data,
            gender=form.gender.data,
            seo=''
        )


        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('rank.rank'))
    return render_template('register.html', form=form)

@users_blueprint.route('/personal_info')
def personal_info():
    return render_template('personal_info.html')


def save_picture(form_picture):
    ''''resize img to 125 125 and save pic and return file path'''

    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex+f_ext

    picture_path=os.path.join(application.root_path,'static/image/profile',picture_fn)

    output_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@users_blueprint.route('/account/<int:user_id>',methods=['GET','POST'])
@login_required
def account(user_id):
    '''todo : sharing한거 분기 처리해줘야됨'''

    queries = FashionScore.query.order_by(FashionScore.pub_date.desc()).filter_by(author_id=user_id)
    #다른 유저면 public한거만 공개
    if user_id!=current_user.id:

        queries= queries.filter_by(sharing=1)

    queries_scrap=Scrap.query.filter_by(scrapper=user_id).join(FashionScore).order_by(FashionScore.pub_date.desc())
    query_user=User.query.filter_by(id=user_id).first()

    pictures=queries.all()
    pictures_scrap=queries_scrap.all()

    image_cnt=queries.count()
    scarp_cnt=queries_scrap.count()
    profile_image = os.path.join(file_url,query_user.profile_img)

    return render_template('account.html',profile_image=profile_image,user=query_user,user_img=pictures,scrap_img=pictures_scrap,image_cnt=image_cnt,scrap_cnt=scarp_cnt)

@users_blueprint.route('/edit_account',methods=['GET','POST'])
@login_required
def edit_account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            random_hex=secrets.token_hex(8)
            _,f_ext=os.path.splitext(form.picture.data.filename)
            picture_fn=random_hex+f_ext

            picture_name='profile_'+str(current_user.id)+'_'+picture_fn
    
            upload_fn(form.picture.data,'socksclub',picture_name)

            current_user.profile_img = picture_name
        if current_user.seo!='facebook':
            current_user.name = form.username.data
            current_user.email = form.email.data
        #facebook으로 가입하면 이름이랑 이메일 바꾸면안딤
        if current_user.seo=='facebook' and (current_user.name != form.username.data or current_user.email != form.email.data):
            flash("You can't update since you are facebook user", 'success')
            return redirect(url_for('users.edit_account'))
        current_user.instagram = form.instagram.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.edit_account'))
    elif request.method == 'GET':
        form.username.data = current_user.name
        form.email.data = current_user.email
        form.instagram.data = current_user.instagram


    profile_image = os.path.join(file_url,current_user.profile_img)

    return render_template('edit_account.html',form=form,profile_image=profile_image)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@users_blueprint.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        flash('Your post has been created','success')
        return redirect(url_for('users.account'))

    return render_template('create_post.html',title='New Post',form=form)

@users_blueprint.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated():
        print('here')
        return redirect(url_for('home.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)



@users_blueprint.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated():
        return redirect(url_for('home.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
