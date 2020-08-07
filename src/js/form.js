import setting from './components/setting';
import $ from 'jquery';

const validate = (obj)=>{
    let input = obj.val();
    if(!input.match(/[^\s　]/)){
        obj.addClass("has-error");
        obj.siblings(".error-empty").show();
    }else{
        obj.siblings(".error-empty").hide();

        switch (obj.attr("name")){
            case "name":
            case "content":
                obj.removeClass("has-error");
                break;
            case "mail":
                if(!input.match(/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/)){
                    obj.siblings(".error-invalid-mail").show();
                }else{
                    obj.removeClass("has-error");
                    obj.siblings(".error-invalid-mail").hide();
                }
                break;
            case "mail-confirm":
                if(input !== $("#mail").val()){
                    obj.siblings(".error-invalid-confirmation").show();
                }else{
                    obj.removeClass("has-error");
                    obj.siblings(".error-invalid-confirmation").hide();
                }
                break;
        }
    }
}

$(".input").addClass("not-selected");
$(".input").on('blur', function(e) {
    e.preventDefault();
    $(this).removeClass("not-selected");
    validate($(this));

    if($("#contact-form-input").find(".has-error").length==0&&$("#contact-form-input").find(".not-selected").length==0){
        $("#contact-form__confirm").addClass("enabled");
    }else{
        $("#contact-form__confirm").removeClass("enabled");
    }
});


$(document).on(setting.bindTouchStart,"#contact-form__confirm.enabled",(e)=>{
    $(".input").each((_,element) => {
        validate($(element));
    });
    if($("#contact-form-input").find(".has-error").length!==0){
        $("#contact-form__confirm").removeClass("enabled");
    }
});
$(document).on(setting.bindTouchEnd,"#contact-form__confirm.enabled",(e)=>{
    $("#contact-form-input,#contact-form-confirmation").addClass("confirm");
    $("#contact-form-confirmation__name").html($(".input[name='name']").val());
    $("#contact-form-confirmation__mail").html($(".input[name='mail']").val());
    $("#contact-form-confirmation__content").html($(".input[name='content']").val());
});

$("#contact-form__back").on(setting.bindTouchStart, (e)=>{
    $("#contact-form-input,#contact-form-confirmation").removeClass("confirm");
});

$("#contact-form__submit").on(setting.bindTouchEnd, function(e){
    e.preventDefault();
    let now = new Date();
    let mailText = "<html>"
                    +"<head><meta charset='utf-8'></head>"
                    +"<body>"
                    +"<p>公式サイトのお問い合わせフォームから、新規のお問い合わせを受信しました。</p>"
                    +"<hr>"
                    +"<p>送信："+ String(now.getFullYear()) + "/" + String(now.getMonth()+1) + "/" + String(now.getDay()) +"</p>"
                    +"<p>氏名："+ $(".input[name='name']").val() +"</p>"
                    +"<p>連絡先："+ $(".input[name='mail']").val() +"</p>"
                    +"<p>本文：<br>"+ $(".input[name='content']").val() +"</p>"
                    +"</body></html>";
    console.log(mailText);
    $.ajax({
        type: "post",
        url: "mail.php",
        data: {
            text:mailText
        },
        crossDomain: false,
        dataType : "text",
        scriptCharset: 'utf-8'
    }).done(function(data){
        if(data=="succeed"){
            alert("お問い合わせフォームからメールを送信しました。");
            $("#contact-form-input,#contact-form-confirmation").removeClass("confirm");
            $(".input").val("");
        }else{
            alert("送信エラー");
        }
    }).fail(function(XMLHttpRequest, textStatus, errorThrown){
        console.log(errorThrown);
    });
});