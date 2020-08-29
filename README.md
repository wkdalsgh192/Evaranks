# evaranks.com
> A web application where a CNN-based AI classifies your fashion style

## Demo
Eva, fashion-classifier AI, is able to analyze your picture to figure out what your fashion is and classify it into 7~8 classes with a fine-tuend VGG-16 model. You can  also share the result with others on leaderboard. The service process:

<p align="center">
    <img width="700" align="center" src="https://user-images.githubusercontent.com/50606172/91626435-f7aa3400-e9e9-11ea-8f9e-d38d480debb9.gif" alt="demo"/>
 </p>


## AI Stack
Eva was created based on a nice paper regarding vision AI : **M. Takagi, E. Simo-Serra, S. Iizuka, and H. Ishikawa. WhatMakes a Style: Experimental Analysis of Fashion Prediction.InProceedings of the International Conference on ComputerVision Workshops (ICCVW), 2017.**

Among several models, we chose to use `VGG-16 model` after examining the validation result, which was a little bit higher than other candidates such as ResNet or VGG-50.

// training dataset picture

## Front-end Stack
### Vanila JS & CSS3(HTML5)
We tried to use as many as up-to-date ES6 grammers and implement visual effects using them.

### Interactive interface
How to design the whole layout for better UI/UX was a core issue in this project. Through several arguments and research, we were agreed to make **interactive interface using typing effect and speech bubbles**.


Here's the sample code : 
```javascript=
let typing =  setInterval(function(){
  content_element.innerHTML += content[text_idx]
  text_idx += 1
  if(text_idx===content_length&&content_idx<num_contents-1)
  {
    content_element.classList.remove('typing-on')
    content_idx += 1
    text_idx = 0
    content = texts_arrs[content_idx]
    content_length = content.length
    content_element = elements[content_idx]
    content_element.classList.add('typing-on')

  }
  else if(text_idx===content_length&&content_idx===num_contents-1){
    content_element.classList.remove('typing-on')
    clearInterval(typing)
  }
},100)
}
```


## Back-end Stack
### Flask
Flask is python based micro-framework. It gives a lot of flexibility to developers compared to other framework like django or spring. Since we needed to deploy AI model in our service, we needed flexibity in our backend server, and therefore, we chose to use flask

### Some Issues

1. Importing Tensorflow

    Importing tensorflow takes time when server is initialized. While developing, when we change and test the code, the server restarts and imports the library again. This takes quite a lot of time and lowers the productivity. To solve this problem, we set a flag variable named **USE_TF** in the config file and didn't import tensorlflow while development.

```python
#config.py
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    USE_TF = False
```

```python
#ranks.py
if USE_TF:
    from tensorflow.keras import applications, optimizers
    from tensorflow.keras.utils import to_categorical
    from tensorflow.keras.models import Sequential, Model, load_model
    from tensorflow.keras.layers import Dropout, Flatten, Dense
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.callbacks import ModelCheckpoint

def predict():
		if USE_TF:
		```...```
		else:
			result = np.random.randn(1,len(style_name))
      pred_class=np.argmax(result)
      ai_style =style_name[pred_class] #Street
      img_str = request.json['image']
    return pil_random_img
```
```

### PostgreSQL
Storing analyzed fashion style and features like following or scraping required many joining operations. Therefore we used RDBMS instead of NoSQL services

## Deploy
We used AWS Elastic Beanstalk and RDS to deploy our application. There are pros and cons you should check out before you enter into the AWS World!

### AWS
**Pros:**
1. Easy to deploy through CLI.
2. Easy to roll back a deployment with checking S3 logs and app version.
3. Able to do both direct control and auto-deployment
4. Able to automate load-balancing and capacity-provision

**Cons:**
1. Temporary server error occurs in updating app version.
2. A bit complicate for beginners to figure out settings and configuration like ebextensions.


### RDS
**Pros**
1. Handy to use since it isn't necessary to do OS and DB setting directly.
2. Easy scaling and auto-scaling for storage.

**Cons**
Nothing!! at least while we have used it.


## UI/UX

1. Facebook Login
2.Sharing Results in KakKoTalk

