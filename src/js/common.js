import setting from './components/setting';
import setDrawer from './components/drawer';

window.onload = ()=>{
    /*--- setting for custom vh ---*/
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);

    /*--- set drawer for smartphone ---*/
    setDrawer();

    document.getElementById('subpage-top__title').classList.add('is-called');
    document.getElementById('subpage-top__title-text').classList.add('is-called');
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