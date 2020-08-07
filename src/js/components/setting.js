export default  {
    bindTouchStart: window.ontouchstart===null?"touchstart":"click",
    bindTouchMove: window.ontouchmove===null?"touchmove":"mousewheel",
    bindTouchEnd: window.ontouchend===null?"touchend":"click",
    newsLabel: {"management":"運営", "benron": "弁論", "debate": "ディベート", "event": "企画", "others": "その他"},
    isSmph: ()=>{
        return window.innerWidth < 1024
    },
    createNewsId: (data)=>{
        return String(data.year) + "-" + String(data.month) + "-" + String(data.day) + "_" + data.name
    }
}