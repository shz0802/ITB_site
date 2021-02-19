import setting from './components/setting';
import setDrawer from './components/drawer';

document.addEventListener('DOMContentLoaded', ()=>{
    /*--- setting for custom vh ---*/
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);

    /*--- set drawer for smartphone ---*/
    setDrawer();

    if(document.getElementById('subpage-top__title')){
        document.getElementById('subpage-top__title').classList.add('is-called');
        document.getElementById('subpage-top__title-text').classList.add('is-called');
        document.getElementById('subpage-top__down').classList.add('is-called');
        document.getElementById('subpage-top__down').addEventListener(setting.bindTouchStart, ()=>{
            let rectTop = document.getElementById('subpage-top').getBoundingClientRect().bottom;
            let offsetTop = window.pageYOffset;
            // let buffer = window.innerWidth*0.15 - 10;
            let top = rectTop + offsetTop;
            window.scrollTo({
                top,
                behavior: 'smooth'
            });
        });
    }

    let externalLinks = document.getElementById('main').querySelectorAll('[data-external]');
    for(let i=0; i<externalLinks.length; i++){
        let link = externalLinks[i];
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
    }
});