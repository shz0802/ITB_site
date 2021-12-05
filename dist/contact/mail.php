<?php
    mb_language("ja");
    mb_internal_encoding("UTF-8");

    $to = "ichiko.todai.benronbu@gmail.com";
    $subject = mb_encode_mimeheader("【新規お問い合わせ】");
    $text = $_POST["text"];
    $from = mb_encode_mimeheader("公式サイトお問い合わせフォーム");
    $from_mail = "info@utbenron.com";
    $from_name = mb_encode_mimeheader("公式サイトお問い合わせフォーム");

    // 送信者情報の設定
    $header = "";
    $header .= "Content-Type: text/html; charset=UTF-8 \r\n";
    $header .= "MIME-Version: 1.0 \r\n";
    $header .= "Return-Path: " . $from_mail . " \r\n";
    $header .= "From: " . $from ." \r\n";
    $header .= "Sender: " . $from ." \r\n";
    $header .= "Reply-To: " . $from_mail . " \r\n";
    $header .= "Organization: " . $from_name . " \r\n";

    
    $return = mail($to, $subject, $text, $header);
    if($return){
        echo "succeed";
        exit;
    }else{
        echo $return;
    }
    
?>