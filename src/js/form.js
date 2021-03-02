import setting from './components/setting';

const validate = (obj)=>{
    let input = obj.value;
    if(!input.match(/[^\s　]/)){
        obj.classList.add('has-error');
        // obj.siblings(".error-empty").show();
    }else{
        // obj.siblings(".error-empty").hide();

        switch (obj.getAttribute('name')){
            case 'name':
            case 'content':
                obj.classList.remove('has-error');
                break;
            case 'mail':
                if(!input.match(/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/)){
                    obj.classList.add('has-error');
                    // obj.siblings(".error-invalid-mail").show();
                }else{
                    obj.classList.remove('has-error');
                    // obj.siblings(".error-invalid-mail").hide();
                }
                break;
            case 'mail-confirm':
                if(input !== document.getElementById('contact-form-input__mail').value){
                    obj.classList.add('has-error');
                    // obj.siblings(".error-invalid-confirmation").show();
                }else{
                    obj.classList.remove("has-error");
                    // obj.siblings(".error-invalid-confirmation").hide();
                }
                break;
        }
    }
}

let inputElements = Array.from(document.getElementsByClassName('input'));
let confirmButton = document.getElementById('contact-form__confirm');
inputElements.map(input => {
    input.classList.add('untouched');
    input.addEventListener('blur', (e)=>{
        e.preventDefault();
        input.classList.remove('untouched');
        validate(input);
        
        if(inputElements.filter(input => input.classList.contains('has-error') || input.classList.contains('untouched')).length == 0){
            confirmButton.classList.add('enabled');
        }else{
            confirmButton.classList.remove('enabled');
        }
    });
});

confirmButton.addEventListener(setting.bindTouchStart, ()=>{
    if(confirmButton.classList.contains('enabled')){
        inputElements.map(input => validate(input));
        if(inputElements.filter(input => input.classList.contains('has-error')).length != 0){
            confirmButton.classList.remove('enabled');
        }
    }
});

confirmButton.addEventListener(setting.bindTouchEnd, ()=>{
    if(confirmButton.classList.contains('enabled')){
        document.getElementById('contact-form-input').classList.add('confirm');
        document.getElementById('contact-form-confirmation').classList.add('confirm');
        document.getElementById('contact-form-confirmation__name').textContent = document.getElementById('contact-form-input__name').value;
        document.getElementById('contact-form-confirmation__mail').textContent = document.getElementById('contact-form-input__mail').value;
        let contentWithEOL = '';
        let lines = document.getElementById('contact-form-input__content').value.replace(/\r\n|\r/g, '\n').split('\n');
        for(let i=0; i<lines.length; i++){
            contentWithEOL = contentWithEOL + lines[i] + '<br>';
        }
        document.getElementById('contact-form-confirmation__content').innerHTML = contentWithEOL;
    }
});

document.getElementById('contact-form__back').addEventListener(setting.bindTouchStart, ()=>{
    document.getElementById('contact-form-input').classList.remove('confirm');
    document.getElementById('contact-form-confirmation').classList.remove('confirm');
});

document.getElementById('contact-form__submit').addEventListener(setting.bindTouchEnd, (e)=>{
    e.preventDefault();
    let now = new Date();
    let contentWithEOL = '';
    let lines = document.getElementById('contact-form-input__content').value.replace(/\r\n|\r/g, '\n').split('\n');
    for(let i=0; i<lines.length; i++){
        contentWithEOL = contentWithEOL + lines[i] + '<br>';
    }
    let mailText = '<html>'
                    +'<head><meta charset="utf-8"></head>'
                    +'<body>'
                    +'<p>公式サイトのお問い合わせフォームから、新規のお問い合わせを受信しました。</p>'
                    +'<hr>'
                    +'<p>[送信日時] ' + String(now.getFullYear()) + '/' + ('0' + String(now.getMonth()+1)).slice(-2) + '/' + ('0' + String(now.getDay())).slice(-2) + ' ' + ('0' + now.getHours()).slice(-2) + ':' + ('0' + now.getMinutes()).slice(-2) + '</p>'
                    +'<p>[お名前] ' + document.getElementById('contact-form-input__name').value +'</p>'
                    +'<p>[メールアドレス] ' + document.getElementById('contact-form-input__mail').value +'</p>'
                    +'<p>[お問い合わせ内容]<br>' + contentWithEOL + '</p>'
                    +'</body></html>';
    let postData = new FormData;
    postData.set('text', mailText);
    
    fetch('mail.php', {
        method: 'POST',
        body: postData
    })
    .then(res => {return res.text()})
    .then(text => {
        if(text == 'succeed'){
            alert("お問い合わせフォームからメールを送信しました。");
            document.getElementById('contact-form-input').classList.remove('confirm');
            document.getElementById('contact-form-confirmation').classList.remove('confirm');
            inputElements.map(input => input.value = '');
        }else{
            alert("送信エラー");
            console.error(text);
        }
    })
    .catch(error => {
        alert("送信エラー");
        console.error(error);
    });
});