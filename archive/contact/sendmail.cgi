#!/usr/bin/perl

# MODULES
use Jcode;
use CGI qw(:standard);

$mode = param('mode');
$name = param('name');
$mail = param('mail');
$syozoku = param('syozoku');
$subject = param('subject');
$body = param('body');

if ($mode eq 'send'){
   &SEND();
}

print "Location: http://utbenron.com/contact/thanks.html\n";
print "\n";

sub SEND{
   &SEND_MAIL($name, $mail, $syozoku, $subject, $body);
}

sub SEND_MAIL{
    local($name, $mail, $syozoku, $subject, $body) = @_;
    my $sendmail;
    my $from;
    my $to;

    $sendmail = '/usr/lib/sendmail';
    $to = 'info@utbenron.com';
    $from = 'info@utbenron.com';

    &Jcode::convert(\$subject,'jis');
    $subject = jcode($subject)->mime_encode;

    $mail_body = "お名前：$name\n";
    $mail_body .= "メールアドレス：$mail\n";
    $mail_body .= "所属：$syozoku\n";
    $mail_body .= "内容：$body\n";
    &Jcode::convert(\$mail_body,'jis');

    open(MAIL,"| $sendmail -t");
    print MAIL "To: $to\n";
    print MAIL "From: $from\n";
    print MAIL "Subject: $subject\n";
    print MAIL "\n";
    print MAIL "$mail_body\n";
    close(MAIL);
}


exit;
