!function(){"use strict";var t={bindTouchStart:null===window.ontouchstart?"touchstart":"click",bindTouchMove:null===window.ontouchmove?"touchmove":"mousewheel",bindTouchEnd:null===window.ontouchend?"touchend":"click",newsLabel:{management:"運営",benron:"弁論",debate:"ディベート",event:"企画",welcome:"新歓",others:"その他"},isSmph:function(){return window.innerWidth<1024},createNewsId:function(t){return String(t.year)+"-"+String(t.month)+"-"+String(t.day)+"_"+t.name}},e=function(t){var e=t.value;if(e.match(/[^\s　]/))switch(t.nextElementSibling.style.display="none",t.getAttribute("name")){case"name":case"content":t.classList.remove("has-error");break;case"mail":e.match(/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/)?(t.classList.remove("has-error"),t.nextElementSibling.nextElementSibling.style.display="none"):(t.classList.add("has-error"),t.nextElementSibling.nextElementSibling.style.display="block");break;case"mail-confirm":e!==document.getElementById("contact-form-input__mail").value?(t.classList.add("has-error"),t.nextElementSibling.nextElementSibling.style.display="block"):(t.classList.remove("has-error"),t.nextElementSibling.nextElementSibling.style.display="none")}else t.classList.add("has-error"),t.nextElementSibling.style.display="block"},n=Array.from(document.getElementsByClassName("input")),o=document.getElementById("contact-form__confirm");n.map((function(t){t.classList.add("untouched"),t.addEventListener("blur",(function(){t.classList.remove("untouched"),e(t),0==n.filter((function(t){return t.classList.contains("has-error")||t.classList.contains("untouched")})).length?o.classList.add("enabled"):o.classList.remove("enabled")}))})),o.addEventListener(t.bindTouchStart,(function(){o.classList.contains("enabled")&&(n.map((function(t){return e(t)})),0!=n.filter((function(t){return t.classList.contains("has-error")})).length&&o.classList.remove("enabled"))})),o.addEventListener(t.bindTouchEnd,(function(){if(o.classList.contains("enabled")){document.getElementById("contact-form-input").classList.add("confirm"),document.getElementById("contact-form-confirmation").classList.add("confirm"),document.getElementById("contact-form-confirmation__name").textContent=document.getElementById("contact-form-input__name").value,document.getElementById("contact-form-confirmation__mail").textContent=document.getElementById("contact-form-input__mail").value;for(var t="",e=document.getElementById("contact-form-input__content").value.replace(/\r\n|\r/g,"\n").split("\n"),n=0;n<e.length;n++)t=t+e[n]+"<br>";document.getElementById("contact-form-confirmation__content").innerHTML=t}})),document.getElementById("contact-form__back").addEventListener(t.bindTouchStart,(function(){document.getElementById("contact-form-input").classList.remove("confirm"),document.getElementById("contact-form-confirmation").classList.remove("confirm")})),document.getElementById("contact-form__submit").addEventListener(t.bindTouchEnd,(function(t){t.preventDefault();for(var e=new Date,o="",c=document.getElementById("contact-form-input__content").value.replace(/\r\n|\r/g,"\n").split("\n"),a=0;a<c.length;a++)o=o+c[a]+"<br>";var i='<html><head><meta charset="utf-8"></head><body><p>公式サイトのお問い合わせフォームから、新規のお問い合わせを受信しました。</p><hr><p>[送信日時] '+String(e.getFullYear())+"/"+("0"+String(e.getMonth()+1)).slice(-2)+"/"+("0"+String(e.getDay())).slice(-2)+" "+("0"+e.getHours()).slice(-2)+":"+("0"+e.getMinutes()).slice(-2)+"</p><p>[お名前] "+document.getElementById("contact-form-input__name").value+"</p><p>[メールアドレス] "+document.getElementById("contact-form-input__mail").value+"</p><p>[お問い合わせ内容]<br>"+o+"</p></body></html>",r=new FormData;r.set("text",i),fetch("mail.php",{method:"POST",body:r}).then((function(t){return t.text()})).then((function(t){"succeed"==t?(alert("お問い合わせフォームからメールを送信しました。"),document.getElementById("contact-form-input").classList.remove("confirm"),document.getElementById("contact-form-confirmation").classList.remove("confirm"),n.map((function(t){return t.value=""}))):(alert("送信エラー"),console.error(t))})).catch((function(t){alert("送信エラー"),console.error(t)}))}))}();