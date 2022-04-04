import setting from './components/setting';
import Swiper from 'swiper/bundle';
import 'style-loader!css-loader!swiper/css/bundle';
import setDrawer from './components/drawer';
import lozad from 'lozad';

document.addEventListener('DOMContentLoaded', ()=>{
    /*--- lazyload setting ---*/
    const observer = lozad();
    observer.observe();

    new Swiper('#top-slider__list', {
        loop: true,
        effect: 'fade',
        fadeEffect: {
            crossFade: true
        },
        speed: 1500,
        autoplay: {
            delay: 2500,
            disableOnInteraction: false
        },
        preloadImages: false,
        lazy: {
            loadPrevNext: true,
        }
    });
    document.querySelectorAll(['.top-slider__list-item']).forEach(s=>{s.style.visibility = "visible";});
    
    /*--- setting for custom vh ---*/
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);

    /*--- set drawer for smartphone ---*/
    setDrawer();

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

    setTimeout(()=>{
        let twitterscript = document.createElement('script');
        twitterscript.src = 'https://platform.twitter.com/widgets.js';
        twitterscript.async = 'true';
        document.head.appendChild(twitterscript);

        /*--- twitter ---*/
        document.getElementById('top-twitter__content').style.display = 'none';
        const mutationObserver = new MutationObserver(records => {
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
        mutationObserver.observe(document.getElementById('top-twitter__content'), {
            attributes: true,
            attributeFilter: ['style'],
            childList: true
        });
    },2000);
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