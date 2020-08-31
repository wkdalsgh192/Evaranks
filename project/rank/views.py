import os
from application import db,new_model,extraction_model,application,s3,file_url,upload_fn,USE_TF
from flask import flash, redirect, session, url_for, render_template, Blueprint, request,jsonify
from sqlalchemy.sql.functions import func
from functools import wraps
from flask_login import current_user,login_required
from project.models import FashionScore,Recommendation,RecommendLog
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import re
import base64
from io import BytesIO

import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
import scipy
import scipy.ndimage
import time
from datetime import datetime
import random


if USE_TF:
    from tensorflow.keras import applications, optimizers
    from tensorflow.keras.utils import to_categorical
    from tensorflow.keras.models import Sequential, Model, load_model
    from tensorflow.keras.layers import Dropout, Flatten, Dense
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.callbacks import ModelCheckpoint


################
#### config ####
################

allowed_img_file = ["JPEG", "JPG", "PNG", "GIF"]
current_user = current_user


style2id = {'Business Casual':0}
id2url = {0:['<a href="https://coupa.ng/bENGHm" target="_blank"><img src="https://static.coupangcdn.com/image/affiliate/banner/ca9249b95047afbf3379add638f5fc8e@2x.jpg" alt="홀리버니 여성용 스퀘어팁 앤 스트랩 레더 블로퍼 CM1307" width="120" height="240"></a>',]}


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in allowed_img_file:
        return True
    else:
        return False

rank_blueprint = Blueprint(
    'rank', __name__,
    template_folder='templates',
)


def centering_img(img):
    size = [256, 256]
    img_size = img.size[:2]
    
    #centering
    row = (size[0] - img_size[0]) // 2
    col = (size[1] - img_size[1]) // 2
    resized = np.zeros(list(size) + [3], dtype=np.uint8)

    resized[col: (col + img.size[1]), row:(row + img.size[0])] = img
    
    return resized


def base64_to_pil(img_base64):
    """
    Convert base64 image data to PIL image
    """
    image_data = re.sub('^data:image/.+;base64,', '', img_base64)
    image_data = BytesIO(base64.b64decode(image_data))
    pil_image = Image.open(image_data)
    pil_image = pil_image.resize((256, 256))
    
    return pil_image

def Generate_RandomImage():
    '''dev'''
    rgb_array = np.random.rand(256, 256) * 255
    pil_random_img =  Image.fromarray(rgb_array.astype('uint8')).convert('RGB')

    return pil_random_img

def ndarray_to_pil(img_ndarray):
    """
    Convert ndarray image data to PIL image
    """
    ndarray_img = Image.fromarray(np.uint8(cm.jet(img_ndarray)*255))

    return ndarray_img

def grayscale(rgb):
        return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def dodge(front, back):
    result=front*255/(255-back)
    result[result>255]=255
    result[back==255]=255
    return result.astype('uint8')

@rank_blueprint.route('/describe', methods=['GET', 'POST'])
def describe():

    if request.method == 'POST':
        f = open('static/text/businessCasual.txt', 'r')
        text = "<\br>".join(f.readlines())
        
        return jsonify(text = text)


@rank_blueprint.route('/sketch', methods=['GET', 'POST'])
def sketch():
    global current_user

    if request.method == 'POST':
        f_ext='.jpeg'
        pub_time = time.time()
        try:
            picture_name=str(pub_time)+str(current_user.id)+f_ext
        except:
            picture_name=str(pub_time)+f_ext
        picture_path=os.path.join(file_url, picture_name)
        starting_img=np.array(base64_to_pil(request.json))
        
        gray_img = grayscale(starting_img)
        inverted_img= 255 - gray_img
        blur_img=scipy.ndimage.filters.gaussian_filter(inverted_img, sigma=5)
        final_img= dodge(blur_img, gray_img)

        new_buffer=BytesIO()
        fig, axes=plt.subplots(1, 1, figsize=(5, 5))
        axes.imshow(final_img, cmap="gray")
        extent = axes.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        fig.savefig(new_buffer, bbox_inches=extent, format='png')

        img_str = base64.b64encode(new_buffer.getvalue())
        # print(img_str)
        img_str = img_str.decode('utf-8')
        img_str = 'data:image/png;base64,'+img_str

        return jsonify(sketch=img_str)



@rank_blueprint.route('/AddRecommendation',methods=['GET', 'POST'])
def AddRecommendation():
    global current_user
    ad_id = request.json['id']
    if current_user.is_authenticated():
        recommend_log=RecommendLog(author=current_user,ad_id=ad_id)
    else:
        recommend_log=RecommendLog(author=None,ad_id=ad_id)
            
    db.session.add(recommend_log)
    db.session.commit()
    db.session.close()
    result='ok'

    return jsonify(result=result)

@rank_blueprint.route('/predict', methods=['GET', 'POST'])
def predict():

    #javasript post method랑 안맞음??
    global current_user

    style_name = ['Business Casual', 'Ethnic', 'Feminine', 'Girlish', '80s Retro', 'British Mode', 'Casual', 'Street']
    if request.method == 'POST':
        #jpeg으로 저장
        f_ext='.jpeg'
        pub_time = time.time()
        #파일이름 설정,current user가 undefined인 예외 처리(js 때문)
        try:
            picture_name=str(pub_time)+str(current_user.id)+f_ext
        except:
            picture_name=str(pub_time)+f_ext
        picture_path=os.path.join(file_url,picture_name)
        style = request.json['class'] #user가 선택한 스타일
        img_rows, img_cols, img_channel = 256, 256, 3
        img = base64_to_pil(request.json['image'])

        #s3에 머저장
        buffer = BytesIO()
        try:
            img.save(buffer, "JPEG")
        except:
            img = img.convert("RGB")  #JPG는 A(투명도)가 없음
            img.save(buffer,"JPEG")
        buffer.seek(0)
        upload_fn(buffer,'socksclub',picture_name)

        #그리고 db에 추가
        new_img=img.resize((img_rows,img_cols))
        new_img=np.array(new_img)[np.newaxis,...]

        if USE_TF:
            layer_output, result=extraction_model.predict(new_img)
            result=result.tolist()

            # mapping feature extraction  
            last_weight = new_model.weights[-2]
            layer_output = np.squeeze(layer_output)
            try:
                '''메모리 에러 발생?'''
                feature_map=scipy.ndimage.zoom(layer_output, (32, 32, 0.5), order=1)
            except Exception as e:
                '''에러 메세지 출력해줘야됨'''
                print('error occured',e)
                return jsonify(ok=False)

            
            pred_class=np.argmax(result)
            ai_style =style_name[pred_class] #Street
            pred_class_weight=last_weight[:, pred_class]
            final_output = np.dot(feature_map.reshape((256*256, 256)),pred_class_weight).reshape((256, 256))
            
            new_buffer = BytesIO()
            fig, axes = plt.subplots(1, 1, figsize= (5, 5))
            axes.imshow(np.asarray(img), alpha=0.5)
            axes.imshow(final_output, cmap='jet', alpha=0.5)
            extent = axes.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            fig.savefig(new_buffer, bbox_inches=extent, format='png')

            img_str = base64.b64encode(new_buffer.getvalue())
            img_str = img_str.decode('utf-8')
            img_str = 'data:image/png;base64,'+img_str
        else:
            result = np.random.randn(1,len(style_name))
            pred_class=np.argmax(result)
            ai_style =style_name[pred_class] #Street
            img_str = request.json['image']

        res={}
        for keys, values in zip(style_name, result[0]):
            values=round(values, 2)*100
            res[keys]=values
        else:
            res = dict(sorted(res.items(), key=(lambda x:x[1]), reverse=True))
            top3_keys, top3_values=list(res.keys())[:3], list(res.values())[:3]
            if top3_values[0] == 100:
                np.random.seed(0)
                randNum=np.random.rand(2).tolist()
                for i in range(1, len(top3_values)):
                    top3_values[i] += randNum[i-1]*10 + 10
                    top3_values[i] = round(top3_values[i],2)
                top3_values[0] = top3_values[0] - (top3_values[1] + top3_values[2])
            max_score =top3_values[0]  #db에 String으로 저장 => 나중에 혹시 모르니까?

        gender = request.json['gender']
        if current_user.is_authenticated():
            sharing = 1
            rank_post=FashionScore(score=max_score,ai_style=ai_style,pub_date=datetime.now(),img_url=picture_path,style=style,author=current_user,sharing=sharing,gender=gender)
        else:
            sharing = 0
            rank_post=FashionScore(score=max_score,ai_style=ai_style,pub_date=datetime.now(),img_url=picture_path,style=style,author=None,sharing=sharing,gender=gender)
        
        db.session.add(rank_post)
        db.session.commit()

    
        recommend_sbquery = db.session.query(RecommendLog.ad_id,func.count(RecommendLog.ad_id).label('count')).group_by(RecommendLog.ad_id).subquery()
        recommendation_queries = Recommendation.query.filter(Recommendation.gender==gender).join(recommend_sbquery,Recommendation.id==recommend_sbquery.c.ad_id,isouter=True).order_by(recommend_sbquery.c.count.desc().nullslast()).all()
        #2개는 클릭수 많은것, 2개는 random
        recommendation_choices = recommendation_queries[:2]
        random_recommendation = random.choices(population=recommendation_queries[2:], k=2)
        recommendation_choices.extend(random_recommendation)

        #sql object 딕셔너리 형태로 바꿔줘야됨
        recommedation_list = []
        for i in recommendation_choices:
            test = {c.name: getattr(i,c.name) for c in Recommendation.__table__.columns}
            recommedation_list.append(test)

        db.session.close()

        #Predict class에 맞는 설명 가져오기
        try: 
            text_dir = 'static/text/'+top3_keys[0]+'.txt'
            f = open(text_dir, 'r')
            text = "<\br>".join(f.readlines())
        except:
            text=""

        return jsonify(top1_class=top3_keys[0],top2_class=top3_keys[1],top3_class=top3_keys[2],
        top1_value=top3_values[0],top2_value=top3_values[1],top3_value=top3_values[2],
        feature=img_str,picture_path=picture_path,recommendation=recommedation_list, text=text)

        


    return None

@rank_blueprint.route('/')
def rank():



    return render_template('rank.html')  # render a template

@rank_blueprint.route('/rank_kr')
def rank_kr():

    return render_template('rank_kr.html') 