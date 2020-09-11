import setting from './components/setting';
import setDrawer from './components/drawer';
import 'babel-polyfill';

/*--- the very first action ---*/
const pageId = document.getElementById('loading-screen')?document.getElementById('loading-screen').dataset.pageId:null;
if(sessionStorage.getItem('utbenron-'+pageId)!='visited'&&pageId){
    document.getElementById('loading-screen').style.display = 'block';
}
if(pageId){
    Array.prototype.forEach.call(document.getElementsByClassName('main-lev1'), element=>element.classList.add('is-waiting'));
}

/*--- delay function ---*/
const delay = t => {
    return new Promise(resolve=>setTimeout(resolve,t));
}

/*--- prevent scroll ---*/
function preventScroll(event) {
    event.preventDefault();
}

/*--- initializing animation/processing ---*/
const initializeSubPage = async ()=>{
    document.removeEventListener(setting.bindTouchMove, preventScroll, {passive: false});
    document.body.classList.remove('stopScroll');
    document.getElementById('subpage-top__title').classList.add('is-called');
    await delay(250);
    document.getElementById('subpage-top__title-text').classList.add('is-called');
    Array.prototype.forEach.call(document.getElementsByClassName('main-lev1'), element=>element.classList.remove('is-waiting'));
    await delay(400);
    document.getElementById('loading-screen').style.display = 'none';
    document.getElementById('subpage-top__down').classList.add('is-called');
    document.getElementById('subpage-top__down').addEventListener(setting.bindTouchStart, ()=>{
        let rectTop = document.getElementById('subpage-top').getBoundingClientRect().bottom;
        let offsetTop = window.pageYOffset;
        let buffer = window.innerWidth*0.15 - 10;
        let top = rectTop + offsetTop;
        window.scrollTo({
            top,
            behavior: 'smooth'
        });
    });
}

/*--- after contents are loaded ---*/
document.addEventListener('DOMContentLoaded', ()=>{

    window.onload = ()=>{
        /*--- setting for custom vh ---*/
        let vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }

    /*--- set drawer for smartphone ---*/
    setDrawer();

    /*--- animation for sub page ---*/
    //exclude chrome on iOS
    let ua = window.navigator.userAgent.toLowerCase();
    let animationExcludeFlag = false;
    if(ua.indexOf('chrome')!==-1&&ua.indexOf('ios')!==-1){
        animationExcludeFlag = true;
    }
    if(!pageId){
        animationExcludeFlag = true;
    }

    if(!animationExcludeFlag){
        //already visited?
        if(sessionStorage.getItem('utbenron-'+pageId)==='visited'){
            initializeSubPage();
        }else{
            sessionStorage.setItem('utbenron-'+pageId,'visited');
            document.body.scrollIntoView();
            document.addEventListener(setting.bindTouchMove, preventScroll, {passive:false});
            document.body.classList.add('stopScroll');

            Promise.resolve()
            .then(()=>{
                return delay(500);
            })
            .then(()=>{
                document.getElementById('loading-icon').classList.add('is-hidden');
                return delay(250);
            })
            .then(()=>{
                document.getElementById('loading-screen').classList.add('is-hidden');
                return delay(500);
            })
            .then(initializeSubPage);
        }
    }
});
