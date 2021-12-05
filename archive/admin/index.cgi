#!/usr/bin/perl

use Jcode;
use CGI qw(:standard);
use Image::Magick;

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
$url = param('url');
$no = param('no');
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
}elsif ($mode eq 'edit_news'){
	&VIEW_HEADER("������󹹿�");
	&VIEW_SIDEBAR($dir_pass);
	&EDIT_NEWS();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'edit_poster'){
	&VIEW_HEADER("�ݥ������Ǽ��Ĺ���");
	&VIEW_SIDEBAR($dir_pass);
	&EDIT_POSTER();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'write_news'){
	&VIEW_HEADER("������󹹿�");
	&VIEW_SIDEBAR($dir_pass);
	&WRITE_NEWS($title,$text,$category,$encode);
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'write_poster'){
	&VIEW_HEADER("�ݥ������Ǽ��Ĺ���");
	&VIEW_SIDEBAR($dir_pass);
	&WRITE_POSTER($file_name, $title, $encode, $url, $type, $no);
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
<title>$title - ichigochan (ver.2.05)</title>
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

<div id="top">
<b>ichigochan</b> - ITB�����֥ڡ������������ƥ�
</div>
<div id="header">
<ul>
<li><a href="?mode=">�ᥤ��ڡ���</a></li>
<li><a href="?mode=edit_news">�������</a></li>
<li><a href="?mode=edit_poster">�ݥ������Ǽ���</a></li>
<li><a href="?mode=edit_hsf&type=header">�إå���</a></li>
<li><a href="?mode=edit_hsf&type=sidebar">�����ɥС�</a></li>
<li><a href="?mode=edit_hsf&type=footer">�եå���</a></li>
</ul>
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
<p>�������ع���������������<br>Ichiko Todai Benronbu</p>
<p>Copyright(C)2015 Koki Ishii. All rights reserved.</p>
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
		print "<a href=\"?mode=&dir_pass=$pass_before_dir$_\">$_</a>&nbsp;<img src=\"./images/pankuzu.gif\">&nbsp;";
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
	if ($dir_pass eq '..'){
		print "<h2>�ᥤ��ڡ���</h2>";
		print "<p>�褦������<b>ichigochan</b>���������ع������������������������Ȥ�������뤿��Υ����ƥ�Ǥ���</p>";
		print "<p>�����ƥ�����Ԥ�<a href=\"mailto:daabubu@gmail.com\">�а�</a>��124���ˤǤ��������ƥ��ư��˴ؤ��뤪�䤤��碌�Ϥ�����ޤǡ�</p>";
		print "<ul><li>�ե�������ư������ϡ������ɥС��Ρֲ��إե�����פ����ư��Υե���������򤷤Ƥ���������</li><li>���ߤΥե������ˤ���HTML�ե�����ʥ����֥ڡ����ˤΰ����ϥ����ɥС��Ρ�HTML�ե�����פ��󵭤���Ƥ��ޤ����ڡ������Խ�������ϡ��ե�����̾�β��Ρ��Խ��פ򡢺��������ϡֺ���פ����򤷤Ƥ���������</li></ul>";
	}else{
		print "<h2>$dir_pass</h2>";
	}
	print <<END;
<h3>����HTML�ե��������</h3>
<p>���Υե�����������HTML�ե������������ޤ���</p>
<h4>���</h4>
<ol>
<li>�ʲ������������᤿��ǡֺ����פ����򤷤ޤ���</li>
<li>���Υե����뤬���������Τǡ����Υ����ɥС�������������ե������õ�������Խ��פ����򤷤��Խ����ޤ���</li>
</ol>
<form method="POST">
<fieldset><legend>������</legend>
<p>�����ȥ롧 <input type="text" name="new_title" value=""> ��ˡ�����̡�</p>
<p>�ե�����̾��.html������Ⱦ�ѱѿ����ˡ� <input type="text" name="file_name" value=""> ��ˡ�index��,��tatenokai��</p>
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
</fieldset>
</form>
<h4>���</h4>
<ul>
<li>���������ե�����γ̤Ȥʤ�Τ�index.html�Ǥ���index.html��title������1�Ԥǵ��Ҥ���Ƥ��ʤ���硢�����ư��ޤ���</li>
</ul>
<h3>�����ե��������</h3>
<p>���Υե�����β��ؤ˿������ե�����ʥ��֥ե�����ˤ�������ޤ���</p>
<h4>���</h4>
<ol>
<li>�ե����̾�����Ϥ����ֺ����פ����򤷤ޤ���</li>
</ol>
<form method="POST">
<fieldset><legend>������</legend>
<p>
�ե����̾��Ⱦ�ѱѿ����ˡ� <input type="text" name="dir_name" value=""> ��ˡ�event��
<input type="hidden" name="mode" value="new_dir">
<input type="hidden" name="dir_pass" value="$dir_pass">
</p>
<p><input type="submit" value="����"></p>
</fieldset>
</form>
<h3>�ե�����Υ��åץ���</h3>
<p>���Υե������˥ե�����򥢥åץ��ɤ��ޤ���HTML�ե���������Ǥʤ��������ե��������⥢�åץ��ɤ��뤳�Ȥ��Ǥ��ޤ���</p>
<h4>���</h4>
<ol>
<li>�ֻ��ȡס�Chrome�ϡ֥ե����������סˤ����򤷤ޤ���</li>
<li>�ֳ����ץ�����ɥ��������Τǡ����åץ��ɤ������ե���������򤷤Ʊ����Ρֳ���(O)�פ����򤷤ޤ���</li>
<li>�֥��åץ��ɡץܥ�������򤷤ޤ���</li>
</ol>
<form method="POST" enctype="multipart/form-data">
<fieldset><legend>������</legend>
<p> <input type="file" name="file_name"></p>
<p>
<input type="hidden" name="dir_pass" value="$dir_pass">
<input type="hidden" name="mode" value="upload">
<input type="submit" value="���åץ���">
</p>
</fieldset>
</form>
<h4>���</h4>
<ul>
<li>Ʊ��̾�Υե����뤬¸�ߤ����硢<u>��񤭤���ޤ�</u>��</li>
<li>�����򥢥åץ��ɤ��ƥ����֥ڡ�����˰��Ѥ�����ϡ������Υե�����̾��Ⱦ�ѱѿ����ʡܰ����ε���ˤΤߤǵ��Ҥ���ɬ�פ�����ޤ������åץ��ɤ���ե������̾����Ⱦ�ѱѿ������ǵ��Ҥ���Ƥ��뤫��ǧ���Ƥ���������</li>
</ul>
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
	print <<END;
<h2>$file_pass���Խ���</h2>
<p>HTML�ե�������Խ����ޤ���</p>
<h4>���</h4>
<ol>
<li>�����ơ���˵��������Ϥ��ޤ���HTML�������Ѥ��Ƶ��Ҥ�����ϡ���<>�ץܥ�������򤷤Ƥ���������</li>
<li>��ʸ�������ɡסʥǥե���Ȥϡ�Shift-JIS�סˤ����򤷤���ǡֽ񤭴����פ����򤷤ޤ���</li>
</ol>
<form method="POST">
<fieldset><legend>������</legend>
<p>���ơ�
<TEXTAREA name="text" rows="20">$data</TEXTAREA>
</p>
<p>ʸ�������ɡ�
<select name="encode">
<option value="sjis" selected>Shift-JIS</option>
<option value="euc">EUC-JP</option>
<option value="utf8">UTF-8</option>
</select>
</p>
<p>
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="file_name" value="$file_name">
<input type="hidden" name="dir_pass" value="$dir_pass">
<input type="submit" value="�񤭴���">
</p>
</fieldset>
</form>
END
}

sub EDIT_NEWS{
	print <<END;
<h2>������󹹿�</h2>
<p><img src="./images/screen2.png"></p>
<p>�����������ˡ����������������ɲä��ޤ���</p>
<h4>���</h4>
<ol>
<li>�֥����ȥ�פ˵����Υ����ȥ�����Ϥ��ޤ�������ϥȥåץڡ�����../index.html�ˤΡֿ������װ����˷Ǻܤ����ۤ��������ڡ����Υ����ȥ�ˤ�ʤ�ޤ���</li>
<li>�֥�����פ����򤷤ޤ���������Ϣ�ε����Ǥ���С������ס��ǥ��١��ȴ�Ϣ�Ǥ���С֥ǥ��١��ȡס�����ʳ��ϡֱ��ġפ����򤹤뤳�Ȥ����ꤵ��Ƥ��ޤ���</li>
<li>�����ơפ˵��������Ƥ����Ϥ��ޤ������������Ϥ�������ϥȥåץڡ����Ρֿ������װ��������󥯤��������ε����ڡ����˷Ǻܤ�����ΤǤ�����<>�ץܥ�������򤹤��HTML�������Ѥ����Խ����Ǥ��ޤ���</li>
<li>��ʸ�������ɡפ����򤷤ޤ����̾�ϡ�Shift-JIS�פΤޤޤˤ��Ƥ����ޤ���</li>
<li>���Ƥ��ǧ�����ֹ����פ����򤷤ޤ���</li>
</ol>
<form method="POST">
<fieldset><legend>������</legend>
<p>�����ȥ롧 <input type="text" name="title" value=""> ��ˡ���37����������������˽о줷�ޤ�������</p>
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
</fieldset>
</form>
END
}

sub EDIT_POSTER{
	print <<END;
<h2>�ݥ������Ǽ����Խ�</h2>
<p><img src="./images/screen1.png"></p>
<p>�ݥ������Ǽ��Ĥ˷Ǽ����줿�ݥ��������ɲá�������ֽ�λ���ޤ����ץХʡ����ղá�����ޤ���</p>
<h3>���ߤηǼ���</h3>
<ul>
<li>�����ν��֤˺�����Ǽ�����ޤ���</li>
<li>�ֽ�λ�ˤ���ס��ֽ�λ��Ϥ����פ����򤹤�ȡ��ֽ�λ���ޤ����ץХʡ����դ����곰�����ꤹ�뤳�Ȥ��Ǥ��ޤ���</li>
<li>�ֺ���פ����򤹤�ȡ����Υݥ�������Ǽ��Ĥ��������ޤ��������������ե�����ϥ����С��夫��Ϻ������ޤ���</li>
</ul>
END
	my $poster_content = EXTRACT_DIV('../index.html', 'div', 'poster', 'content');
	my @posters = split(/<img[^>]*?src\s*=\s*\"\.\.\/images\/space_poster\.png\"[^>]*?>/, $poster_content);
	print "<ol>";
	my $i = 0;
	foreach my $tag (@posters){
		my $end_flg;
		my $poster_image;
		my $poster_image_alt;
		my $eventpage;
		my $end_tag = '<img[^>]*?src\s*=\s*\"\.\.\/images\/end-l\.png\"[^>]*?>';
		if ($tag =~ m/$end_tag/){
			$tag =~ s/$end_tag//;
			$end_flg = 1;
		}
		if ($tag =~ /<img[^>]*?src\s*=\s*\"(.+?)\"\s*(alt\s*=\s*\"(.*?)\")?[^>]*?>/){
			$poster_image = $1;
			$poster_image_alt = $3;
		}
		if ($tag =~ /<a[^>]*?href\s*=\s*\"(.*?)\"[^>]*?>/){
			$eventpage = $1;
		}
		print "<li>$poster_image_alt<br>";
		print "[<a href=\"$poster_image\">������ɽ��</a>] ";
		if ($end_flg){
			print "[<a href=\"?mode=write_poster&type=end&no=$i\">��λ��Ϥ���</a>]";
		}else{
			print "[<a href=\"?mode=write_poster&type=end&no=$i\">��λ�ˤ���</a>]";
		}
		print " [<a href=\"?mode=write_poster&type=del&no=$i\">���</a>]";
		print "</li>";
		$i++;
	}
	print "</ol>";
	print <<END;
<h3>�������ݥ��������ɲä���</h3>
<h4>���</h4>
<ol>
<li>�ֲ�������Ρֻ��ȡס�Chrome�ϡ֥ե����������סˤ����򤷡��ֳ����ץ�����ɥ����������顢���åץ��ɤ������ե���������򤷤Ʊ����Ρֳ���(O)�פ����򤷤ޤ���</li>
<li>�֥����Υ��ɥ쥹�פ����Ϥ��ޤ�������ϡ��ݥ������򥯥�å���������־ܺ٤ʥ��٥�Ⱦ���Υڡ����Υ��ɥ쥹�����ꤵ��Ƥ��ޤ���<br>����Ū�˥��٥�ȥڡ����ϡ�event�ץե��������ǽ���Ū�˴�������Ƥ��ޤ����������ڡ���������ϡ����Υ����ɥС������event�ץե���������򤷤ơ��ֿ���HTML�ե�����κ����פ������Υڡ���������������ȡ������ɥС�������Խ��פ��ޤ������κݺ��������ڡ����Υ��ɥ쥹�򵭲����Ƥ������ݥ�������Ǽ�����ݤˤ��Ρ֥����Υ��ɥ쥹��������Ϥ��ޤ���</li>
<li>�֥��٥�ȤΥ����ȥ�פ����Ϥ�����ʸ�������ɡפ����򤷤���ǡ��ɲáפ����򤷤ޤ���</li>
</ol>
<form method="POST" enctype="multipart/form-data">
<fieldset><legend>������</legend>
<ul>
<p>������ <input type="file" name="file_name"></p>
<p>�����Υ��ɥ쥹�� <input type="text" name="url"> ��˸޷�פʤ��http://utbenron.com/event/mayfest.html��</li>
<p>���٥�ȤΥ����ȥ롧 <input type="text" name="title"> ��ˡ���10��޷�׵�ǰ��������</p>
<p>ʸ�������ɡ�
<select name="encode">
<option value="sjis" selected>Shift-JIS</option>
<option value="euc">EUC-JP</option>
<option value="utf8">UTF-8</option>
</select>
</p>
<p><input type="hidden" name="mode" value="write_poster"><input type="hidden" name="type" value="add"><input type="submit" value="�ɲ�"></p>
</fieldset>
<h4>���</h4>
<ul>
<li><u>���åץ��ɤ���ݥ����������Υե�����̾��Ⱦ�ѱѿ����Ǥ��뤳�Ȥ��ǧ���Ƥ���������</u></li>
<li>�ݥ������Υ������Ͻ�200px����141px���ǥե���ȤǤ����������礭���ե���������򤷤���硢��ưŪ�˹⤵��200px��·�����ޤ���</li>
<li>�ݥ������ν��֤������ؤ������Ȥ��ϡ��������ơֺ���פ�����ǡֿ������ݥ��������ɲä���פ������������֤��ɲä��ޤ���</li>
<li>�ݥ������ηǺܤ����Ǥʤ����ܺ٥ڡ������Խ���ԤäƤ���������</li>
<ul>
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

sub WRITE_POSTER {
	local ($file_name, $title, $encode, $url, $type, $no) = @_;
	my $data_poster = EXTRACT_DIV('../index.html','div','poster','content');
	my @posters = split(/<img[^>]*?src\s*=\s*\"\.\.\/images\/space_poster\.png\"[^>]*?>/, $data_poster);
	my $data_write;
	my $image_position = 0;
	my $i = 0;
	foreach my $tag (@posters){
		if ($type eq 'del' && $i == $no){
			$i++;
			next;
		}
		my $end_flg;
		my $poster_image;
		my $poster_image_alt;
		my $eventpage;
		my $end_tag = '<img[^>]*?src\s*=\s*\"\.\.\/images\/end-l\.png\"[^>]*?>';
		if ($tag =~ m/$end_tag/){
			$tag =~ s/$end_tag//;
			$end_flg = 1;
		}
		if ($tag =~ /<img[^>]*?src\s*=\s*\"(.+?)\"\s*(alt\s*=\s*\"(.*?)\")?[^>]*?>/){
			$poster_image = $1;
			$poster_image_alt = $3;
		}
		my $image = Image::Magick->new;
		my $status = $image->Read($poster_image);
		my ($width, $height) = $image->Get('width', 'height');
		if ($tag =~ /<a[^>]*?href\s*=\s*\"(.*?)\"[^>]*?>/){
			$eventpage = $1;
		}
		if ($i > 0){
			$data_write .= "<img src=\"../images/space_poster.png\" alt=\"\" height=\"200\" border=\"0\" />";
		}
		$data_write .= "<a href=\"$eventpage\">";
		$data_write .= "<img src=\"$poster_image\" alt=\"$poster_image_alt\" height=\"200\" border=\"0\" />";
		if ($end_flg){
			unless ($type eq 'end' && $i == $no){
				my $left = "$image_position" . "px";
				$data_write .= "<img style=\"position: absolute\; left: $left\; top: 0px\;\" src=\"../images/end-l.png\" alt=\"\" border=\"0\" />";
			}
		}else{
			if ($type eq 'end' && $i == $no){
				my $left = "$image_position" . "px";
				$data_write .= "<img style=\"position: absolute\; left: $left\; top: 0px\;\" src=\"../images/end-l.png\" alt=\"\" border=\"0\" />";
			}
		}
		$data_write .= "</a>";
		$image_position += ($width * (200 / $height)) + 5;
		$i++;
	}
	if ($type eq 'add'){
		unless ($file_name){
			&ERROR("���åץ��ɤ���ե���������򤷤Ƥ���������");
		}
		my $write_file = "../images/$file_name";
		open(OUT, ">$write_file");
		binmode(OUT);
		while (read($file_name,$buffer,1024)){
			print OUT $buffer;
		}
		close(OUT);
		close($write_file);
		$data_write .= "<img src=\"../images/space_poster.png\" alt=\"\" height=\"200\" border=\"0\" /><a href=\"$url\"><img src=\"$write_file\" alt=\"$title\" height=\"200\" border=\"0\" /></a>";
	}
	&WRITE_DIV('..','index.html','poster',$data_write,$encode);
	print "<li>index.html�ؤν񤭹��ߤ���λ���ޤ�����</li>";
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
	print <<END;
<h2>$type���Խ���</h2>
<p><b>���Ƥ�</b>�ڡ����Υإå����������ɥС����եå�����񤭴����ޤ���</p>
<p>div��������Ѥ������<b>���Ф�</b>�������������Ĥ��������θĿ���Ʊ��Ǥ��뤳�Ȥ��ǧ���Ƥ��������ʲ�ǽ�Ǥ����<u>div��������Ѥ��ʤ��Ǥ�������</u>�ˡ����켺�Ԥ���ȡ����Ƥ��Խ������ƥ�ε�ǽ�����ѤǤ��ʤ��ʤ�ޤ���</p>
<h4>���</h4>
<ol><li>����Ū�ˡ��Խ��פ�Ʊ���Ǥ���</li></ol>
<form method="POST">
<fieldset><legend>������</legend>
<p>���ơ�
<TEXTAREA name="text" rows="20">
END
	open(FH, "$open_file") or ERROR("���ꤵ�줿�ե����뤬���Ĥ���ޤ���");
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		print "$data\n";
	}
	close(FH);
	print <<END;
</TEXTAREA>
</p>
<p>ʸ�������ɡ�
<select name="encode">
<option value="sjis" selected>Shift-JIS</option>
<option value="euc">EUC-JP</option>
<option value="utf8">UTF-8</option>
</select>
</p>
<p>
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="type" value="$type">
<input type="submit" value="�񤭴���">
</p>
</fieldset>
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
	close($write_file);
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