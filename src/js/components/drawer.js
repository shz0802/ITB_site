import setting from "./setting"

const toggleDrawer = (flg)=>{
    document.getElementById('header__menu-trigger').classList.toggle('is-active');
    document.getElementById('page-cover').classList.toggle('is-open');
    document.getElementById('container').classList.toggle('is-open');
    document.getElementById('header').classList.toggle('is-open');
    document.getElementById('header-menu').classList.toggle('is-open');
    if(flg){
        document.body.style.overflowX = 'hidden';
        document.body.style.overflowY = 'scroll';
        document.getElementById('header-menu').style.overflowY = 'hidden';
    }else{
        document.body.style.overflow = 'hidden';
        document.getElementById('header-menu').style.overflowY = 'scroll';
    }
    return !flg
}

export default ()=>{    
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