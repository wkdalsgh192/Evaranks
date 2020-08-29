const sectionInfo= [
  {
    // section 0
    sectionNum:0,
    heightNum:1,
    scrollHeight:0,
    objs: {
      container:document.querySelector('#click-section-0'),
      doubleClickFlag: false
    },
    contents:{
      animation:true,
      header:"Hello Stranger",
      main:["I'm your personal stylist AI, Eva.","First, upload your picture in the box."]
    },
  },
  {
    // section 1
    sectionNum:1,
    heightNum: 1,
    scrollHeight: 0,
    objs: {
      container: document.querySelector("#click-section-1"),
      doubleClickFlag: false
    },
    contents:{
      animation:true,
      header:"Please Select Your Gender",
      main:[" "," "]
    }
  },
  {
    // section 2
    sectionNum:2,
    heightNum: 1,
    scrollHeight: 0,
    objs: {
      container: document.querySelector("#click-section-2"),
      doubleClickFlag: false
    },
    contents:{
      animation:true,
      header:"Great!",
      main:["Next, select one of the pictures"," similar to your fashion."]
    }
  },
  {
    // section 3
    sectionNum:3,
    heightNum: 1,
    scrollHeight: 0,
    objs: {
      container: document.querySelector("#click-section-3"),
      doubleClickFlag: false
    },
    contents:{
      animation:false,
      header:"Please Select Your Gender",
      main:[" "," "]
    }
  },
  {
    // section 4
    sectionNum:4,
    heightNum: 1,
    scrollHeight: 0,
    objs: {
      container: document.querySelector("#click-section-4"),
      doubleClickFlag: false
    },
    contents:{
      animation:true,
      header:"Wait!",
      main:["Share your pic on our Leaderboard.","Join a competition for a free drink!"]
    }
  },
  {
    // section 5
    sectionNum:5,
    heightNum: 1,
    scrollHeight: 0,
    objs: {
      container: document.querySelector("#click-section-5"),
      doubleClickFlag: false
    },
    contents:{
      animation:true,
      header:"패션에 맞는 옷 추천",
      main:["옷을 추천해드립니다","이 옷을 구매해 보세요"]
    }
  },
  
];

function setLayout() {
  for (let i=0;i < sectionInfo.length;i++) {
    sectionInfo[i].scrollHeight=window.innerHeight*sectionInfo[i].heightNum;
    sectionInfo[i].objs.container.style.height=`${sectionInfo[i].scrollHeight}px`;
  }

  typing(0);
};

window.addEventListener('resize', setLayout);
setLayout();

//========================================================================
// Initial Animation events
//========================================================================

function typing(currentScene){

let nextScrollSection = document.querySelectorAll('section')[currentScene];

//title과 main html 가져오기
let headr_element = nextScrollSection.querySelector('.section-title');
let main_element = nextScrollSection.querySelectorAll('.line-1');
let elements = [headr_element,...main_element]
//비워주기
elements.map((e)=>{e.innerHTML=''})
//title과 main text정보
let header_text = sectionInfo[currentScene].contents.header
let main_text= sectionInfo[currentScene].contents.main

//text split해서 배열로 만들고 합치기
let header_arr = header_text.split('')
let main_arr_container = main_text.map((e=>{return e.split('')}))
let texts_arrs = [header_arr,...main_arr_container]
//initialize
let content_idx= 0
let num_contents = texts_arrs.length
let text_idx = 0
let content = texts_arrs[content_idx]
let content_length = content.length
let content_element = elements[content_idx]
content_element.classList.add('typing-on')

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

//Prevent Scrolling
function stopScroll (e) {
  e.preventDefault();
  //e.stopPropagation();
}
document.addEventListener("wheel", stopScroll, {passive: false});
document.addEventListener("touchmove", stopScroll, {passive: false});



var fileDrag = document.getElementById("file-drag");
var fileSelect = document.getElementById("file-upload");
var imageClass = document.querySelectorAll('.class-box');
var imageCheck = document.querySelectorAll('i');
var classChoice = document.getElementById('class-choice');

let coupang_container = document.body.querySelector('.coupang-item-container')

// Add event listeners
fileDrag.addEventListener("dragover", fileDragHover, false);
fileDrag.addEventListener("dragleave", fileDragHover, false);
fileDrag.addEventListener("drop", fileSelectHandler, false);
fileSelect.addEventListener("change", fileSelectHandler, false);
for (var i=imageClass.length-1;i>-1;i--) {
imageClass[i].querySelector('img').addEventListener("click", imageSelectHandler, false);
}

function fileDragHover(e) {
// prevent default behaviour
e.preventDefault();
e.stopPropagation();

fileDrag.className = e.type === "dragover" ? "upload-box dragover" : "upload-box";
}

function fileSelectHandler(e) {
// handle file selecting
var files = e.target.files || e.dataTransfer.files;
fileDragHover(e);
for (var i = 0, f; (f = files[i]); i++) {
  previewFile(f);
}
}

function fileDragHover(e) {
  // prevent default behaviour
  e.preventDefault();
  e.stopPropagation();

  fileDrag.className = e.type === "dragover" ? "upload-box dragover" : "upload-box";
}

function fileSelectHandler(e) {
  // handle file selecting
  var files = e.target.files || e.dataTransfer.files;
  fileDragHover(e);
  for (var i = 0, f; (f = files[i]); i++) {
    previewFile(f);
  }
}

function imageSelectHandler(e) {
  var nothidden = Array.from(document.body.querySelectorAll("div#class-table svg")).filter(function(a){return !a.classList.contains('hidden')})
  var selectClass=e.currentTarget.parentNode.childNodes[1];
  var classArray = Array.from(selectClass.classList);

  if(nothidden.length>0)
  {
    nothidden.map(function(e){hide(e)})
  }
  
  if (classArray.includes('hidden')) {
    show(selectClass)
  } else {
    hide(selectClass)
  }
  classChoice.textContent=e.currentTarget.parentNode.childNodes[6].textContent;
}

//========================================================================
// Web page elements for functions to use
//========================================================================

var evaIntro = document.getElementById('modal');
var secondTitle = document.getElementById('second-title');
var imagePreview = document.getElementById("image-preview");
var imageResult = document.getElementById("image-result");
var imageDisplay = document.getElementById("image-display");
var uploadCaption = document.getElementById("upload-caption");
var loader = document.getElementById("loader");
let currentScene = 0;
let gender;
let compressed_base64;

//========================================================================
// Main button events
//========================================================================

function changeSection() {
  // currentSection을 자동으로 탐지해서 붙여주기 
  currentScene += 1;
  let nextScrollSection = document.querySelectorAll('section')[currentScene];
  let scrollLocation= nextScrollSection.offsetTop;

  //일단 section1만 처리
    if (!imagePreview.src || !imagePreview.src.startsWith("data")) {
      window.alert("Please select an image for a next step");
      return;
    }

    
    if (currentScene === 2) {
      imageClassDisplay();
    }
  
  
  setTimeout(function(){
    
    window.scroll({top:scrollLocation, behavior:'smooth'})
    
    if(sectionInfo[currentScene].contents.animation) //section 3은 애니메이션 안걸림
    { 
      typing(currentScene);
    }

},900);
  // 중복 클릭 방지
  document.querySelectorAll('section')[currentScene-1].querySelector('#next-btn').classList.add('disabled')
};

function submitImage() {

  // action for the submit button
  if (classChoice.textContent === '') {
    window.alert("Please select your style.");
    return;
  } else {
    changeSection();
  }

  loader.classList.remove("hidden");
  imagePreview.classList.add("loading");

  //성별 체크
  gender = document.body.querySelector('#male').checked?'M':'F';
  var srcclass = {'image':compressed_base64,'class': classChoice.textContent,'gender':gender};
  // call the predict function of the backend
  hide(secondTitle);
  predictImage(srcclass);
  sketchImage(compressed_base64)
  // loadDescription();
}

function clearImage() {
  // reset selected files
  fileSelect.value = "";

  // remove image sources and hide them
  imagePreview.src = "";
  imageDisplay.src = "";


  hide(imagePreview);
  hide(imageDisplay);
  hide(loader);

  show(uploadCaption);
  hide(secondTitle);

  kakaodefault();
}


function imageToDataUri() {
  // create an off-screen canvas
  var canvas = document.createElement('canvas'),
      ctx = canvas.getContext('2d');

  width = 256
  height = 256

  // set its dimension to target size
  canvas.width = width;
  canvas.height = height;
  // draw source image into the off-screen canvas:
  ctx.drawImage(this, 0, 0, width, height);

  // encode image to data-uri with base64 version of compressed image
  compressed_base64 = canvas.toDataURL();

  return compressed_base64
}

function previewFile(file) {
  // show the preview of the image
  var fileName = encodeURI(file.name);

  var reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onloadend = () => {

    imagePreview.onload = imageToDataUri
    imagePreview.src = reader.result
    //let trial = imageToDataUri(imagePreview,1024,1024) //URL.createObjectURL(file);
    //console.log('after',trial)
    //magePreview.src = trial
    show(imagePreview);
    hide(uploadCaption);
    show(secondTitle);
  };
}

//========================================================================
// Helper functions
//========================================================================

function imageClassDisplay () {
  let classArray;
  let fileName;
  let className = document.querySelectorAll('.class-box p.class-text');
  let classNum = document.querySelectorAll('.class-box img');
  gender = document.body.querySelector('#male').checked?'M':'F';
  if (gender === 'F') {
    fileName = ['business_casual', 'street', 'casual', 'mod', 'girlish', 'retro', 'feminine', 'traditional'];
    classArray = ['Business Casual', 'Street', 'Casual', 'British Mod', 'Girlish', '80s Retro', 'Feminine', 'Traditional'];
    for (var i=0; i < classNum.length; i++) {
      classNum[i].src=`/static/image/gender/female/${fileName[i]}.jpg`;
      console.log('classNum[i].src',classNum[i].src)
      className[i].innerHTML = classArray[i];
    }    
  } else {
    fileName = ['business_casual', 'street', 'casual', 'mod', 'classic', 'retro', 'traditional'];
    classArray = ['Business Casual', 'Street', 'Casual', 'British Mod', 'Classic', '80s Retro', 'Traditional'];
    for (var i=0; i < classNum.length-1; i++) {
      classNum[i].src=`/static/image/gender/male/${fileName[i]}.jpg`;
      className[i].innerHTML = classArray[i];
    }
  }
}

// function loadDescription() {
//   fetch("/describe", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json"
//     }
//     // body : JSON.stringify()
//   })
//     .then(resp => {
//       if (resp.ok)
//         resp.json().then(data => {
//           explainText(data.text, '.style-description')
//         })
//     })
//     .catch(err => {
//       console.log("Wrong loaded", err.message)
//     });
// }

function sketchImage(image) {
  fetch("/sketch", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(image)
  })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
          displayImage(data.sketch, 'image-result');
        })
    })
    .catch(err => {
      console.log("Error occured", err.message)
    });
}

function predictImage(image) {
  fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(image)
  })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {          
          let imageResultBtn = document.getElementById("click-section-3").querySelector('.global-buttons');
          let resultStatus = document.querySelector('.result-status');
          show(resultStatus);
          show(imageResultBtn);

          displayText(data.top1_class, data.top1_value, 'pred-result1');
          hide(loader);
          
          imagePreview.classList.remove("loading");

          // 설명 삽입
          explainText(data.text, '.style-description');

          //쿠팡광고삽입
          coupang_container.innerHTML=''
          data.recommendation.forEach((e)=>{
            createAd(e)
          })


          Kakao.Link.createDefaultButton({
            container: '#kakao-link-btn',
            objectType: 'feed',
            content: {
              title: '오늘 나의 룩은?!',
              description: data.top1_class,
              imageUrl: data.picture_path,
              link: {
                webUrl: document.location.href,
                mobileWebUrl: document.location.href
              }
            },
            social: {
              likeCount: 100,
              commentCount: 100,
              sharedCount: 100
            },
            buttons: [
              {
                title: 'Open!',
                link: {
                  mobileWebUrl: document.location.href,
                  webUrl: document.location.href
                }
              }  
            ]
          });

        });
    })
    .catch(err => {
      console.log("An error occured", err.message);
      window.alert("Oops! Something went wrong.");
    });
}

function createAd(e)
{
  let coupang_item = document.createElement('div')
  coupang_item.classList.add('coupang-item')

  let address = document.createElement('a')
  address.href = e.address

  let img = document.createElement('img')
  img.src = e.source
  img.alt = e.text

  coupang_item.appendChild(address)
  address.appendChild(img)
  coupang_container.appendChild(coupang_item)

  let ad_id = e.id
  let data = {'id':ad_id}

  coupang_item.addEventListener('click',function(event)
  {
    ClickAdEvent(event,data);
  })

}

//db에 user 정보추가
function ClickAdEvent(event,data)
{
  fetch("/AddRecommendation", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
    .then(resp => {
      if (resp.result)
        resp.json().then(data => {
          console.log('success')
        //CODE
        });
    })
    .catch(err => {
      console.log("An error occured", err.message);
      window.alert("Oops! Something went wrong.");
    });
}
function displayImage(image, id) {
  // display image on given id <img> element
  let display = document.getElementById(id);
  display.src = image;
  show(display);
  hide(loader);

}

function displayText(pnt1, pnt2, id) {
    // display image on given id <img> element    
    let display = document.getElementById(id);    
    display.children[0].innerHTML = pnt1;
    display.children[1].innerHTML = `${pnt2}%`;
}

function explainText(text, className) {
  let explain = document.querySelector(className);
  explain.innerHTML = text;
}

function disable(el) {
  el.classList.add("disabled")
}

function hide(el) 
{ 
  // hide an element
  if (el === loader) {
    el.style.display = "none";
  } else {
    el.classList.add("hidden");
  }
}

function show(el)
{
  // show an element
  el.classList.remove("hidden");
}

//========================================================================
// Social Sharing Functions
//========================================================================

var kakaobutton=document.body.querySelector('#kakao-link-btn');

Kakao.init('447851f891152a700eb8aa1e85b28bdf');
kakaodefault();

function kakaodefault()
{
  Kakao.Link.createDefaultButton({
    container: '#kakao-link-btn',
    objectType: 'feed',
    content: {
      title: '오늘 나의 룩은?!',
      description: '오늘 나의 패션을 분석해보세요!',
      imageUrl: 'https://source.unsplash.com/random/1',
      link: {
        webUrl: document.location.href,
        mobileWebUrl: document.location.href
      }
    }  
  });
};
