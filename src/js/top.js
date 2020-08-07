import setting from './components/setting';
import Swiper from 'swiper';
import ShuffleText from 'shuffle-text';
import setDrawer from './components/drawer';

/*--- the very first action ---*/
if(sessionStorage.getItem('utbenron-top')!='visited'){
    document.getElementById('enter-page').style.display = 'block';
    document.getElementById('loading-icon').classList.add('is-hidden');
}

/*--- delay function ---*/
const delay = t => {
    return new Promise(resolve=>setTimeout(resolve,t));
}

/*--- prevent scroll ---*/
function preventScroll(e) {
    e.preventDefault();
}

/*--- initializing animation/processing ---*/
const initializeTopPage = async ()=>{
    document.getElementById('top-slider').classList.add('is-called');
    let swiper = new Swiper('#top-slider__list', {
        loop: true,
        effect: 'fade',
        fadeEffect: {
            crossFade: true
        },
        speed: 1500,
        autoplay: {
            delay: 2500
        }
    });
    document.removeEventListener(setting.bindTouchMove, preventScroll, { passive: false });
    await delay(500);
    document.body.classList.remove('stopScroll');
    await delay(400);
    document.getElementById('top-slider__down').classList.add('is-called');
    document.getElementById('top-slider__down').addEventListener(setting.bindTouchStart, ()=>{
        let rectTop = document.getElementById('top-info').getBoundingClientRect().top;
        let buffer = window.innerWidth<1024?window.innerWidth*0.25:window.innerWidth*0.15 - 10;
        let diff = rectTop - buffer;
        let scrollNow = window.pageYOffset;
        let smoothScroll = (range)=>{
            let position = 0;
            let progress = 0;
            let easeOut = p=>{
                return p*(2-p);
            };
            let move = ()=>{
                progress++;
                position = range*easeOut(progress/60);
                window.scrollTo(0, scrollNow + position);
                if (position < range){
                    requestAnimationFrame(move);
                }
            };
            requestAnimationFrame(move);
        };
        smoothScroll(diff);
    });

    let twitterscript = document.createElement('script');
    twitterscript.src = 'https://platform.twitter.com/widgets.js';
    document.head.appendChild(twitterscript);
};


/*--- after contents are loaded ---*/
document.addEventListener('DOMContentLoaded', ()=>{
    /*--- setting for custom vh ---*/
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);

    /*--- set drawer for smartphone ---*/
    setDrawer();

    /*--- animation for top page ---*/
    //exclude chrome on iOS
    let ua = window.navigator.userAgent.toLowerCase();
    let animationExcludeFlag = false;
    if(ua.indexOf('chrome')!==-1&&ua.indexOf('ios')!==-1){
        animationExcludeFlag = true;
    }

    //already visited?
    if(animationExcludeFlag || sessionStorage.getItem('utbenron-top')=='visited'){
        initializeTopPage();
    }else{
        sessionStorage.setItem('utbenron-top','visited');
        document.body.scrollIntoView();
        document.addEventListener(setting.bindTouchMove, preventScroll, { passive: false });

        Promise.resolve()
        .then(()=>{
            document.body.classList.add('stopScroll');
            document.getElementById('top-slider').classList.add('is-called');
            return delay(100);
        })
        .then(()=>{
            var text = new ShuffleText(document.getElementById('enter-page__title'));
            text.duration = 1500;
            text.start();
            return delay(1750);
        })
        .then(()=>{
            document.getElementById('enter-button').classList.add('is-called');
            document.getElementById('enter-button').addEventListener(setting.bindTouchStart, async ()=>{
                document.getElementById('enter-page').classList.add('is-over');
                await delay(600);
                initializeTopPage();
                document.getElementById('enter-page').classList.add('is-hidden');
            });
        });
    }

    /*--- latest news list ---*/
    const displayNum = 3;
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = ()=>{
        if(xhr.readyState == 4){
            if(xhr.status == 200){
                let newsList = JSON.parse(xhr.responseText)['news-list'];
                for(let i=0;i<displayNum;i++){
                    let news = newsList[i];
                    let newsDOM = "<li class='top-news__list-item'>"
                                + "<div class='top-news__list-item__date'>" + String(news.year) + "/" + ("00"+String(news.month)).slice(-2) + "/" + ("00"+String(news.day)).slice(-2) + "</div>"
                                + "<div class='top-news__list-item__title'><a href='news/" + setting.createNewsId(news) + "'>" + news.title + "</a></div>"
                                + "<div class='top-news__list-item__label " + "label-" + news.label +"'>" + setting.newsLabel[news.label] + "</div>"
                                + "</li>"
                    document.getElementById('top-news__list').insertAdjacentHTML('beforeend',newsDOM);
                }
            }else{
                console.error(xhr.status+':'+xhr.statusText);
            }
        }
    }
    xhr.open('GET', './assets/json/news-list.json', true);
    xhr.send();

    /*--- twitter ---*/
    document.getElementById('top-twitter__content').style.display = 'none';
    const observer = new MutationObserver(records => {
        if(records[0]["removedNodes"].length!=0&&document.getElementById('twitter-widget-0')){
            let twitterWidget = document.getElementById('twitter-widget-0');
            twitterWidget.removeAttribute('style');
            twitterWidget.contentWindow.document.querySelector('.timeline-Body').style.border = 'none';
            twitterWidget.contentWindow.document.querySelector('.timeline-Widget').style.backgroundColor = '#fcfcfc';
            twitterWidget.contentWindow.document.querySelector('.timeline-Widget').style.fontFamily = 'Noto Sans JP';
            Array.prototype.forEach.call(twitterWidget.contentWindow.document.getElementsByClassName('timeline-Tweet-text'), element=>{
                element.style.fontSize = '15px';
                element.style.lineHeight = '1.5';
            });
            twitterWidget.contentWindow.document.querySelector('footer.timeline-Footer').style.display = 'none';
            twitterWidget.classList.add('enabled');
            let twitterWrapper = document.getElementById('top-twitter__content');
            twitterWrapper.style.opacity = 0;
            twitterWrapper.style.display = 'block';
            let start = performance.now();
            let duration = 500;
            requestAnimationFrame(function tick(timestamp) {
                var easing = (timestamp - start) / duration;
                twitterWrapper.style.opacity = Math.min(easing, 1);
                if(easing<1) {
                    requestAnimationFrame(tick);
                }else{
                    twitterWrapper.style.opacity = '';
                }
            });
        }
    })
    observer.observe(document.getElementById('top-twitter__content'), {
        attributes: true,
        attributeFilter: ['style'],
        childList: true
    });
});


/*--- on resize ---*/
let timeoutId;
let currentWidth = window.innerWidth;
window.addEventListener('resize', ()=>{
    if(currentWidth == window.innerWidth){return;}
    clearTimeout(timeoutId);
    timeoutId = setTimeout(()=>{
        let vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
        let swiper = new Swiper('#top-slider__list', {
            loop: true,
            effect: 'fade',
            fadeEffect: {
                crossFade: true
            },
            speed: 1500,
            autoplay: {
                delay: 2500
            }
        });        
    },500);
    currentWidth = window.innerWidth;
});