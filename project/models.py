from application import db,login_manager,bcrypt,application
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class RecommendLog(db.Model):
    __tablename__ = "recommend_log"

    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,ForeignKey('users.id'))
    ad_id=db.Column(db.Integer,ForeignKey('recommendation.id'))

    def __repr__(self):
        return 'user click {}th item'.format(self.ad_id)

class Recommendation(db.Model):
    __tablename__ = "recommendation"

    id=db.Column(db.Integer, primary_key=True)
    address=db.Column(db.String(), nullable=False)
    source=db.Column(db.String(), nullable=False)
    text=db.Column(db.String())
    style=db.Column(db.String(), nullable=False)
    gender=db.Column(db.String())

    recommends=relationship("RecommendLog",lazy='dynamic',cascade="all,delete",backref="recommendation")

    def __repr__(self):
        return 'Recommendation info {}'.format(self.id)

class Scrap(db.Model):
    __tablename__ = "scrap"

    id = db.Column(db.Integer, primary_key=True)
    scrapped=db.Column(db.Integer,ForeignKey('fashion.id'))
    scrapper=db.Column(db.Integer,ForeignKey('users.id'))
    scrapped_airank=db.Column(db.Integer,ForeignKey('fashionscore.id'))

    # def __init__(self, pub_date,img_url):
    #     self.pub_date = pub_date
    #     self.img_url=img_url

    def __repr__(self):
        return 'scrapper {}'.format(self.scrapper)



class Calendar(db.Model):

    __tablename__ = "calendar"

    id = db.Column(db.Integer, primary_key=True)
    #img=db.Column(db.Integer,ForeignKey('fashion.id'))
    img_url=db.Column(db.String,nullable=False)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))
    date = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return '<comment {}>'.format(self.date)


class Fashion(db.Model):

    __tablename__ = "fashion"

    id = db.Column(db.Integer, primary_key=True)
    pub_date = db.Column(db.DateTime)
    fashion_text=db.Column(db.String,nullable=True)

    upper=db.Column(db.String,nullable=True)
    lower=db.Column(db.String,nullable=True)
    etc=db.Column(db.String,nullable=True)


    img_url=db.Column(db.String,nullable=False)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))
    scraps=relationship("Scrap",lazy='dynamic',cascade="all,delete",backref="fashion")
    #calendar=relationship("Calendar",lazy='dynamic',cascade="all,delete",backref="fashion")


    # def __init__(self, pub_date,img_url):
    #     self.pub_date = pub_date
    #     self.img_url=img_url

    def __repr__(self):
        return '<comment {}>'.format(self.fashion_text)

class FashionScore(db.Model):
    
    __tablename__ = "fashionscore"

    id = db.Column(db.Integer, primary_key=True)
    img_url=db.Column(db.String,nullable=False)
    style = db.Column(db.String,nullable=True)
    ai_style= db.Column(db.String,nullable=True)
    score = db.Column(db.Float,nullable=True)
    gender = db.Column(db.String,nullable=True)
    sharing = db.Column(db.Integer,nullable=True,default=1)
    pub_date = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))
    scraps=relationship("Scrap",lazy='dynamic',cascade="all,delete",backref="fashionscore")

    def __repr__(self):
        return '<comment {}>'.format(self.img_url)

class User(db.Model,UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=True)
    instagram = db.Column(db.String, nullable=True)
    seo = db.Column(db.String,nullable=True)
    gender = db.Column(db.String,nullable=True)
    profile_img = db.Column(db.String(50),nullable=False,default='default.png')
    pictures=relationship("Fashion",cascade="all,delete",lazy=True,backref="author")
    scraps=relationship("Scrap",cascade="all,delete",lazy='dynamic',backref="author")
    calendar=relationship("Calendar",lazy='dynamic',cascade="all,delete",backref="author")
    fashioscore=relationship("FashionScore",lazy='dynamic',cascade="all,delete",backref="author")
    recommends=relationship("RecommendLog", lazy='dynamic', cascade="all,delete", backref="author")
    #,secondary=fashion_scrap,

    def __init__(self, name, email,seo,instagram,password,gender):
        self.name = name
        self.email = email
        self.seo=seo
        self.instagram=instagram
        self.gender = gender
        #seo 때문에 분기 처리
        if password!='':
            self.password = bcrypt.generate_password_hash(password)
        else:
            self.password=''

    def scrap_fashion(self,fashion):
        if not self.has_scrapped_fashion(fashion):
            scrap=Scrap(scrapper=self.id,scrapped_airank=fashion.id)
            db.session.add(scrap)
            return True
        else:
            return False

    def has_scrapped_fashion(self,fashion):
        return Scrap.query.filter_by(scrapper=self.id,scrapped_airank=fashion.id).count()>0

    def delete_scrap(self, fashion):
        if self.has_scrapped_fashion(fashion):
            Scrap.query.filter_by(
                scrapper=self.id,
                scrapped_airank=fashion.id).delete()

    def get_reset_token(self,expire_sec=1800):

        s=Serializer(application.config['SECRET_KEY'],expire_sec)
        print('here')
        db.session.commit()

        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s=Serializer(application.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
            print(user_id)
        except:
            return None
        try:
            user = User.query.get(user_id)
            db.session.rollback()
            return user
        except:
            db.session.rollback()



    def __repr__(self):
        return '<name - {}>'.format(self.name)
