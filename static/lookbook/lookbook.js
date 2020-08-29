//gender box 누르면 토글 효과
let GenderButton = document.body.querySelectorAll('.gender-header div')
let MaleImgContainer = document.body.querySelector('#male-container')
let FemaleImgContainer = document.body.querySelector('#female-container')

GenderButton.forEach((e) => {
    e.addEventListener('click',function(){ToggleGender()})
})
function ToggleGender()
{
    let text_styles = {'init_hide': 'init-out', 'init_show': 'init-in','hide':'fade-out','show':'fade-in'}
    GenderButton.forEach((e)=>{

        ToggleAnimation(e,text_styles)
        //ToggleText(e)
    })


    let img_styles =  {'init_hide': 'init-img-hide', 'init_show': 'init-img-show','hide':'hide-male-container','show':'show-male-container'}
    ToggleAnimation(MaleImgContainer,img_styles)
    //male animation female animation으로 바꾸어줌
    for (let [key, value] of Object.entries(img_styles)) {
            if(value.includes('male'))
            {
                img_styles[key]=value.replace('male','female')
            }
          }
    ToggleAnimation(FemaleImgContainer,img_styles)

}

function ToggleAnimation(container,styles)
{
    let init_hide = styles['init_hide']
    let init_show = styles['init_show']

    let hide = styles['hide']
    let show = styles['show']
    //초기세팅
    if(container.classList.contains(init_hide))
    {
        container.classList.remove(init_hide)
        container.classList.toggle(show)
    }
    else if(container.classList.contains(init_show))
    {
        container.classList.remove(init_show)
        container.classList.toggle(hide)
    }
    else{

        container.classList.toggle(show)
        container.classList.toggle(hide)
    }
}

//참가한 인원 숫자 증가
let nums = document.body.querySelector('.count-header strong')
let total_people =document.body.querySelector('#total-people')
let people_num = parseInt(total_people.innerHTML)
for(let i=0;i<people_num;i++)
{

    setTimeout(function(){
        nums.innerHTML=String(i+1)
    },1000*Math.log2(i+1))
}

//text 타이핑
let main_text = 'Join Our Fashion Challenge!!!'
let text_arr = main_text.split('')
let text_element = document.body.querySelector('.count-footer a')
text_element.classList.add('typing-on')
for(let i=0;i<text_arr.length;i++)
{
    setTimeout(function(){
        text_element.innerHTML = text_element.innerHTML + text_arr[i]
    },200*i)
    //blinking 효과 제거
    if(i==text_arr.length-1)
    {
        setTimeout(function(){
            text_element.classList.remove('typing-on')
        },200*i)
    }
}