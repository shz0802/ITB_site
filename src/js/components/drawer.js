import setting from "./setting"

let drawerElements = ['header__menu-trigger', 'page-cover', 'container', 'header', 'header-menu'];

const toggleDrawer = flg => {
    drawerElements.map(id => document.getElementById(id).classList.toggle('is-open'));
    if(flg){
        document.body.style.overflowY = 'scroll';
        document.getElementById('header-menu').style.overflowY = 'hidden';
    }else{
        let scrollOffsetY = window.pageYOffset;
        window.scrollTo(0, scrollOffsetY);
        document.body.style.overflowY = 'hidden';
        document.getElementById('header-menu').style.overflowY = 'scroll';
    }
    return !flg
}

export default ()=>{
    window.addEventListener("pageshow", event => {
        if(event.persisted){
            drawerElements.map(id => {
                let obj = document.getElementById(id);
                obj.classList.add('transition-disabled');
            });
            setTimeout(()=> drawerElements.map(id => {
                document.getElementById(id).classList.remove('transition-disabled');
            }),100);
        }
    });

    let openFlg = false;
    document.getElementById('header__menu-trigger').addEventListener(setting.bindTouchEnd,()=>{
        if(setting.isSmph()){openFlg = toggleDrawer(openFlg);}
    });
    document.getElementById('header-menu').querySelector('.is-current').addEventListener(setting.bindTouchEnd,()=>{
        if(setting.isSmph()){openFlg = toggleDrawer(openFlg);}
    });
    document.getElementById('page-cover').addEventListener(setting.bindTouchStart, ()=> {
        if(openFlg == true){
            openFlg = toggleDrawer(openFlg);
        }
    });
}