#!/usr/bin/perl

use Jcode;
use CGI qw(:standard);

# �ѥ�᡼������
$mode = param('mode');
$file_pass = param('file_pass');
$dir_pass = param('dir_pass');
unless ($dir_pass){$dir_pass = ".."};
$file_name = param('file_name');
$dir_name = param('dir_name');
$new_title = param('new_title');
$type = param('type');
$text = param('text');
$title = param('title');
$category = param('category');
$encode = param('encode');
if (param('encode') eq 'sjis'){
	$encode = 'sjis';
}elsif (param('encode') eq 'euc'){
	$encode = 'euc';
}elsif (param('encode') eq 'utf8'){
	$encode = 'utf8';
}else{
	$encode = 'sjis';
}
# �ե�����̾��Ǽ�ѿ�
$header_file = './files/header.dat';
$sidebar_file = './files/sidebar.dat';
$footer_file = './files/footer.dat';

# ���ֽ���
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
$year += 1900;
$mon += 1;

# �⡼�ɽ���
if ($mode eq 'edit_html'){
	&VIEW_HEADER("�ڡ������Խ�");
	&VIEW_SIDEBAR($dir_pass);
	&EDIT_HTML($dir_pass, $file_name);
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'edit_hsf'){
	&VIEW_HEADER("�إå����������ɥС����եå������Խ�");
	&VIEW_SIDEBAR($dir_pass);
	&EDIT_HSF($type);
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'new_html'){
	&VIEW_HEADER("����HTML�ե��������");
	&VIEW_SIDEBAR($dir_pass);
	&NEW_HTML($file_name,$dir_pass,$new_title,$encode,"");
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'new_dir'){
	&VIEW_HEADER("�����ե��������");
	&VIEW_SIDEBAR($dir_pass);
	&NEW_DIR($dir_pass,$dir_name);
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'upload'){
	&VIEW_HEADER("�ե�����Υ��åץ���");
	&VIEW_SIDEBAR($dir_pass);
	&UPLOAD($dir_pass,$file_name);
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'write_news'){
	&VIEW_HEADER("������󹹿�");
	&VIEW_SIDEBAR($dir_pass);
	&WRITE_NEWS($title,$text,$category,$encode);
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'del_html'){
	&VIEW_HEADER("�ե�������");
	&VIEW_SIDEBAR($dir_pass);
	&DEL_HTML($dir_pass,$file_name);
	&VIEW_FOOTER();
	exit;
}else{
	&VIEW_HEADER("�ᥤ��ڡ���");
	&VIEW_SIDEBAR($dir_pass);
	&VIEW_MAIN($dir_pass);
	&VIEW_FOOTER();
	exit;
}

sub VIEW_HEADER{
	local ($title) = @_;
	print "Content-type: text/html\n\n";
	print <<END;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=euc-jp" />
<link href="style.css" rel="stylesheet" type="text/css">
<title>$title - sms (ver.2.04)</title>
<script type="text/javascript">
<!--
function del(url){
	if (window.confirm('������¹Ԥ��Ƥ������Ǥ�����')){
		location.href = url;
	}
	else{
		window.alert('��������ߤ��ޤ���');
	}
}
// -->
</script>
<script type="text/javascript" src="../js/tinymce/tinymce.min.js"></script>
<script type="text/javascript">
tinymce.init({
    selector: "textarea",
    language : 'ja',
    plugins: "code link image",
    toolbar: "code | undo redo | styleselect | bold italic | fontsizeselect | alignleft aligncenter alignright | bullist numlist | link image",
    menubar : "edit format view insert"
 });
</script>
</head>
<body>
<hr><hr><hr>
<div id="top">
<div id="top2">
<div id="logo">&nbsp;</div>
<div id="header">
<ul>
<li><a href="?mode=">sms</a></li>
<li><a href="?mode=edit_hsf&type=header">�إå����Խ�</a></li>
<li><a href="?mode=edit_hsf&type=sidebar">�����ɥС��Խ�</a></li>
<li><a href="?mode=edit_hsf&type=footer">�եå����Խ�</a></li>
</ul>
</div>
</div>
</div>
<div style="clear:both;"></div>
<div id="main">
END
}

sub VIEW_FOOTER{
	print <<END;
</div>
</div>
<div id="footer">
<div id="footer2">
<p>�������ع���������������<br>Ichiko Todai Benronbu</p>
<p>Copyright(C)2014 Koki Ishii. All rights reserved.</p>
</div>
</div>
</body>
</html>
END
}

sub VIEW_SIDEBAR{
	local ($dir_pass) = @_;
	print "<div id=\"pankuzu\">";
	my @dirs = split(/\//,$dir_pass);
	my $n = 0;
	foreach (@dirs){
		my $pass_before_dir;
		for ($i = 0; $i < $n; $i++){
			$pass_before_dir .= "$dirs[$i]/";
		}
		print "<a href=\"?mode=&dir_pass=$pass_before_dir$_\">$_</a>/";
		$n++;
	}
	print "</div>";
	my @all_html_files;
	my @all_dirs;
	opendir (DIR, "$dir_pass");
	foreach (readdir(DIR)){
		next if /^\.{1,2}$/;
		if (-d "$dir_pass/$_"){
			push (@all_dirs,$_);
		}elsif ($_ =~ /\.html?$/){
			push (@all_html_files,$_);
		}
	}
	closedir (DIR);
	print "<div style=\"clear:both;\"></div>";
	print "<div id=\"sidebar\">";
	print "<div class=\"content\">";
	print "<h2>���إե����</h2>";
	print "<div class=\"dirlist\">";
	print "<ul>";
	foreach (@all_dirs){
		print "<li><a href=\"?mode=&dir_pass=$dir_pass/$_\">$_</a></li>";
	}
	print "</ul>";
	print "</div>";
	print "<h2>HTML�ե�����</h2>";
	print "<ul>";
	foreach (@all_html_files){
		print "<li>$_<br>[<a href=\"$dir_pass/$_\" target=\"_top\">ɽ��</a>] [<a href=\"?mode=edit_html&dir_pass=$dir_pass&file_name=$_\">�Խ�</a>] [<a href=\"#\" onClick=\"del(\'?mode=del_html&dir_pass=$dir_pass&file_name=$file_name$_\'); return false;\">���</a>]</li>";
	}
	print "</ul>";
	print "</div>";
	print "</div>";
	print "<div id=\"content\">";
}

sub EXTRACT_DIV{
	local ($file_pass, $tag, $id, $mode) = @_;
	my $before_div;
	my $content;
	my $after_div;
	my $content_counter;
	my $content_attribute;
	my $counter;
	my @flg;
	open(FH, "$file_pass") or ERROR("$file_pass���ɤ߹��ߤ˼��Ԥ��ޤ�����");
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		unless ($flg[$content_counter] == 2){
		while ($data =~ /^(<\s*$tag\s*((?:"[^"]*"|'[^']*'|[^"'>])*?)(?:\s*\/\s*)?>)/ig){
			my $html = $1;
			my $attribute = $2;
			my %attributes;
			while ($attribute =~ m/(\w+?)(?:\s*=\s*("[^"]*"|'[^']*'|[^"']*))?(?:\s+|$)/g){
				my $atr_name = $1;
				my $atr_value = $2;
				$atr_value =~ s/^(["'])(.*?)\1$/$2/;
				$attributes{$atr_name} = $atr_value;
			}
			$counter++;
			$flg[$counter] = 1;
			if ($attributes{"id"} eq $id){
				$data =~ s/$html//;
				$content_counter = $counter;
				$content_attribute = $attribute;
			}
		}
		if ($flg[$content_counter] == 1){
			$content .= "$data\n";
		}elsif ($flg[$content_counter] == 0){
			$before_div .= "$data\n";
		}
		while ($data =~ /<\s*\/\s*$tag\s*>/ig){
			my $html = $1;
			for ($i = $counter; $i > 0; $i--){
				if ($flg[$i] == 1){
					if ($i == $content_counter){
						$flg[$i] = 2;
					}else{
						$flg[$i] = 0;
					}
					last;
				}
			}
		}
		}else{
			$after_div .= "$data\n";
		}
	}
	chomp $after_div;
	if ($mode eq 'before'){
		return ($before_div);
	}elsif ($mode eq 'after'){
		return ($after_div);
	}elsif ($mode eq 'content'){
		return ($content);
	}elsif ($mode eq 'atr'){
		return ($content_attribute);
	}else{
		return;
	}
}

sub VIEW_MAIN{
	local ($dir_pass) = @_;
	my $poster_attribute = EXTRACT_DIV('../index.html', 'div', 'poster', 'atr');
	print "<TEXTAREA>$poster_attribute</TEXTAREA>";
	print <<END;
<h3>�������򹹿�����</h3>
<form method="POST">
<p>�����ȥ롧 <input type="text" name="title" value=""></p>
<p>�����롧
<select name="category">
<option value="0" selected>����</option>
<option value="1">����</option>
<option value="2">�ǥ��١���</option>
</select>
</p>
<p>���ơ�
<TEXTAREA name="text" rows="10" cols="50"></TEXTAREA>
</p>
<p>ʸ�������ɡ�
<select name="encode">
<option value="sjis" selected>Shift-JIS</option>
<option value="euc">EUC-JP</option>
<option value="utf8">UTF-8</option>
</select>
</p>
<p>
<input type="hidden" name="mode" value="write_news">
<input type="submit" value="����">
</p>
</form>
<h3>���Υե������˿���HTML�ե�������������</h3>
<ul>
<li>�Ǿ��ء�../�˥ե�����Ǥο�����������������Хѥ�������../��फ���ѹ�����ޤ�����ä˥������륷���Ȥ������</li>
<li>���������ե�����γ̤Ȥʤ�Τ�index.html�Ǥ���index.html��title������1�Ԥǵ��Ҥ���Ƥ��ʤ���硢�����ư��ޤ���</li>
</ul>
<form method="POST">
<p>�����ȥ롧 <input type="text" name="new_title" value=""></p>
<p>�ե�����̾��.html�����ˡ� <input type="text" name="file_name" value=""></p>
<p>ʸ�������ɡ�
<select name="encode">
<option value="sjis" selected>Shift-JIS</option>
<option value="euc">EUC-JP</option>
<option value="utf8">UTF-8</option>
</select>
</p>
<p>
<input type="hidden" name="mode" value="new_html">
<input type="hidden" name="dir_pass" value="$dir_pass">
<input type="submit" value="����">
</p>
</form>
<h3>���Υե�����β��˿����ե�������������</h3>
<form method="POST">
<p>
�ե����̾�� <input type="text" name="dir_name" value="">
<input type="hidden" name="mode" value="new_dir">
<input type="hidden" name="dir_pass" value="$dir_pass">
<input type="submit" value="����">
</p>
</form>
<h3>���Υե������˥ե�����򥢥åץ��ɤ���</h3>
<form method="POST" enctype="multipart/form-data">
<p> <input type="file" name="file_name" size="60"></p>
<p>
<input type="hidden" name="dir_pass" value="$dir_pass">
<input type="hidden" name="mode" value="upload">
<input type="submit" value="���åץ���">
</p>
</form>
END
}

sub EDIT_HTML{
	local ($dir_pass, $file_name) = @_;
	unless ($file_name){
		&ERROR("file_name�λ��꤬�����Ǥ���");
	}
	my $file_pass = "$dir_pass/" . "$file_name";
	if ($text){
		&WRITE_DIV($dir_pass,$file_name,'content',$text,$encode);
		print "<font color=\"red\">�Խ�����λ���ޤ�����</font>";
	}
	my $data = EXTRACT_DIV($file_pass, 'div', 'content', 'content');
	print "<h2>$file_pass���Խ���</h2>";
	print "<form method=\"POST\">";
	print "<TEXTAREA name=\"text\" rows=\"20\" cols=\"100\">";
	print "$data";
	print "</TEXTAREA>";
	print "<br>";
	print <<END;
<select name="encode">
<option value="sjis" selected>Shift-JIS</option>
<option value="euc">EUC-JP</option>
<option value="utf8">UTF-8</option>
</select>
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="file_name" value="$file_name">
<input type="hidden" name="dir_pass" value="$dir_pass">
<input type="submit" value="�񤭴���">
</form>
END
}

sub WRITE_DIV{
	local ($dir_pass, $file_name, $id, $write_text, $encode) = @_;
	unless ($file_name){
		&ERROR("file_name�λ��꤬�����Ǥ���");
	}
	my $file_pass = "$dir_pass/" . "$file_name";
	unless ($write_text) {return;}
	my $before_div = EXTRACT_DIV($file_pass, 'div', $id, 'before');
	my $after_div = EXTRACT_DIV($file_pass, 'div', $id, 'after');
	my $content_attribute = EXTRACT_DIV($file_pass, 'div', $id, 'atr');
	open(FH, "> $file_pass") or ERROR("$file_pass�ؤν񤭹��ߤ˼��Ԥ��ޤ�����");
	my $data = "$before_div<div $content_attribute>\n$write_text\n</div>\n$after_div";
	$data = jcode($data)->$encode;
	print FH $data;
	close(FH);
}

sub WRITE_NEWS{
	local ($title,$text,$category,$encode) = @_;
	chomp $text;
	my $mon = sprintf("%02d",$mon);
	my $mday = sprintf("%02d",$mday);
	my $sec = sprintf("%02d",$sec);
	my $min = sprintf("%02d",$min);
	my $data = "<h3>$year.$mon.$mday \n";
	my $file_name = "$year$mon$mday$hour$min$sec";
	if ($category == 1){
		$data .= "<img src=\"../images/benron-ss.png\" alt=\"����\">";
	}elsif ($category == 2){
		$data .= "<img src=\"../images/debate-ss.png\" alt=\"�ǥ��١���\">";
	}else{
		$data .= "<img src=\"../images/unei-ss.png\" alt=\"����\">";
	}
	$data .= " $title</h3>";
	$data .= " $text";
	my $data_news = EXTRACT_DIV('../index.html','div','news','content');
	my $write_text_index = "<ul>\n<li>$year.$mon.$mday \n";
	if ($category == 1){
		$write_text_index .= "<img src=\"../images/benron-ss.png\" alt=\"����\">";
	}elsif ($category == 2){
		$write_text_index .= "<img src=\"../images/debate-ss.png\" alt=\"�ǥ��١���\">";
	}else{
		$write_text_index .= "<img src=\"../images/unei-ss.png\" alt=\"����\">";
	}
	$write_text_index .= " <a href=\"../news/$file_name.html\">$title</a></li>\n";
	my @data_news_array = split(/\n/,$data_news);
	foreach (@data_news_array){
		$_ =~ s/<\s*\/?div[^>]*?>//igo;
		$_ =~ s/<\s*\/?ul[^>]*?>//igo;
		if ($_){
			$write_text_index .= $_;
		}
	}
	$write_text_index .= "</ul>";
	&WRITE_DIV('..','index.html','news',$write_text_index,$encode);
	print "<li>index.html�ؤν񤭹��ߤ���λ���ޤ�����</li>";
	&NEW_HTML($file_name, '../news', $title, $encode, $data);
}

sub NEW_HTML{
	local ($file_name, $dir_pass, $title, $encode, $text) = @_;
	unless ($file_name){
		&ERROR("�ե�����̾�����Ϥ��Ƥ���������");
	}
	unless ($title){
		&ERROR("�����ȥ�����Ϥ��Ƥ���������");
	}
	my $file_pass = "$dir_pass/" . "$file_name" . ".html";
	if (-f $file_pass){
		ERROR("$file_pass�ϴ���¸�ߤ��Ƥ��ޤ����ʾ���ɻߡ�");
	}
	my $model_pass = '../index.html';
	$new_title = jcode($new_title)->euc;
	my $before_div = EXTRACT_DIV($model_pass, 'div', 'content', 'before');
	my $after_div = EXTRACT_DIV($model_pass, 'div', 'content', 'after');
	my $content_attribute = EXTRACT_DIV($model_pass, 'div', 'content', 'atr');
	open(FH, "> $file_pass") or ERROR("$file_pass�ؤν񤭹��ߤ˼��Ԥ��ޤ�����content�ˡ�");
	my $data = "$before_div<div $content_attribute>$text\n</div>\n$after_div";
	$data = jcode($data)->$encode;
	print FH $data;
	close(FH);
	my $before_title = EXTRACT_DIV($file_pass, 'title', '', 'before');
	my $after_title = EXTRACT_DIV($file_pass, 'title', '', 'after');
	my $title_attribute = EXTRACT_DIV($file_pass, '', 'title', 'atr');
	open(FH, "> $file_pass") or ERROR("$file_pass�ؤν񤭹��ߤ˼��Ԥ��ޤ�����title�ˡ�");
	if ($title_attribute){
		$data = "$before_title<title $title_attribute>$new_title</title>\n$after_title";
	}else{
		$data = "$before_title<title>$new_title</title>\n$after_title";
	}
	$data = jcode($data)->$encode;
	print FH $data;
	close(FH);
	print "<li><font color=\"red\">$file_pass��������ޤ��������ܥ���ϻ��Ѥ������嵭��˥塼�������򤷤Ƥ�����������</font></li>";
}

sub DEL_HTML{
	local ($dir_pass, $file_name) = @_;
	unless ($file_name){
		&ERROR("file_name�λ��꤬�����Ǥ���");
	}
	my $file_pass = "$dir_pass/" . "$file_name";
	if (unlink $file_pass) {
		print "<li><font color=\"red\">$file_pass�������ޤ���</li></font>";
	}
	else{
		ERROR("$file_pass�����Ǥ��ޤ���Ǥ�����");
	}
}

sub OPEN_DIR{
	local ($dir_pass,$type,$text,$encode) = @_;
	opendir (DIR, "$dir_pass");
	foreach (readdir(DIR)){
		next if /^\.{1,2}$/;
		if (-d "$dir_pass/$_"){
			&OPEN_DIR("$dir_pass/$_",$type,$text,$encode);
		}elsif ($_ =~ /\.html?$/){
			&WRITE_DIV("$dir_pass","$_",$type,$text,$encode);
		}
	}
	closedir (DIR);
}

sub EDIT_HSF{
	local ($type) = @_;
	my $opne_file;
	if ($type eq 'header') {$open_file = $header_file;}
	elsif ($type eq 'sidebar') {$open_file = $sidebar_file;}
	elsif ($type eq 'footer') {$open_file = $footer_file;}
	else {&ERROR("���ޥ�ɤ������Ǥ�");}
	if ($text){
		open(FH, "> $open_file") or ERROR("$open_file�����Ĥ���ޤ���");
		print FH $text;
		close(FH);
		&OPEN_DIR("..",$type,$text,$encode);
		print "<font color=\"red\">�Խ�����λ���ޤ�����</font>";
	}
	print "<h2>$type���Խ���</h2>";
	print "<form method=\"POST\">";
	print "<TEXTAREA name=\"text\" rows=\"20\" cols=\"100\">";
	open(FH, "$open_file") or ERROR("���ꤵ�줿�ե����뤬���Ĥ���ޤ���");
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		print "$data\n";
	}
	close(FH);
	print "</TEXTAREA>";
	print "<br>";
	print <<END;
<select name="encode">
<option value="sjis" selected>Shift-JIS</option>
<option value="euc">EUC-JP</option>
<option value="utf8">UTF-8</option>
</select>
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="type" value="$type">
<input type="submit" value="�񤭴���">
</form>
END

}

sub UPLOAD{
	local ($dir_pass,$file_name) = @_;
	unless ($file_name){
		&ERROR("���åץ��ɤ���ե���������򤷤Ƥ���������");
	}
	my $write_file = "$dir_pass". "/" . "$file_name";
	open(OUT, ">$write_file");
	binmode(OUT);
	while (read($file_name,$buffer,1024)){
		print OUT $buffer;
	}
	close(OUT);
	close($file_name);
	print "<font color=\"red\">$write_file��������ޤ��������ܥ���ϻ��Ѥ������嵭��˥塼�������򤷤Ƥ�����������</font>";
}

sub NEW_DIR{
	local ($dir_pass,$dir_name) = @_;
	unless ($dir_name){
		&ERROR("�ե����̾�����Ϥ��Ƥ���������");
	}
	my $write_dir = "$dir_pass". "/" . "$dir_name";
	if (-d "$write_dir"){
		ERROR("$wite_dir�ϴ���¸�ߤ��Ƥ��ޤ����ʾ���ɻߡ�");
	}
	mkdir "$write_dir";
	print "<font color=\"red\">$write_dir��������ޤ��������ܥ���ϻ��Ѥ������嵭��˥塼�������򤷤Ƥ�����������</font>";
}


sub ERROR{
	local ($text) = @_;
	print "<h2>$text</h2>";
	print "<ul><li>�����ƥ�����Ԥ��䤤��碌�Ƥ���������</li></ul>";
	&VIEW_FOOTER();
	exit;
}

exit;