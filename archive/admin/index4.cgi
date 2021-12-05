#!/usr/bin/perl

use Jcode;
use CGI qw(:standard);

# パラメータ処理
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
# ファイル名格納変数
$header_file = './files/header.dat';
$sidebar_file = './files/sidebar.dat';
$footer_file = './files/footer.dat';

# 時間処理
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
$year += 1900;
$mon += 1;

# モード処理
if ($mode eq 'edit_html'){
	&VIEW_HEADER("ページの編集");
	&VIEW_SIDEBAR($dir_pass);
	&EDIT_HTML($dir_pass, $file_name);
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'edit_hsf'){
	&VIEW_HEADER("ヘッダー・サイドバー・フッターの編集");
	&VIEW_SIDEBAR($dir_pass);
	&EDIT_HSF($type);
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'new_html'){
	&VIEW_HEADER("新規HTMLファイル作成");
	&VIEW_SIDEBAR($dir_pass);
	&NEW_HTML($file_name,$dir_pass,$new_title,$encode,"");
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'new_dir'){
	&VIEW_HEADER("新規フォルダ作成");
	&VIEW_SIDEBAR($dir_pass);
	&NEW_DIR($dir_pass,$dir_name);
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'upload'){
	&VIEW_HEADER("ファイルのアップロード");
	&VIEW_SIDEBAR($dir_pass);
	&UPLOAD($dir_pass,$file_name);
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'write_news'){
	&VIEW_HEADER("新着情報更新");
	&VIEW_SIDEBAR($dir_pass);
	&WRITE_NEWS($title,$text,$category,$encode);
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'del_html'){
	&VIEW_HEADER("ファイル削除");
	&VIEW_SIDEBAR($dir_pass);
	&DEL_HTML($dir_pass,$file_name);
	&VIEW_FOOTER();
	exit;
}else{
	&VIEW_HEADER("メインページ");
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
	if (window.confirm('処理を実行してもよろしいですか？')){
		location.href = url;
	}
	else{
		window.alert('処理を中止しました');
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
<li><a href="?mode=edit_hsf&type=header">ヘッダー編集</a></li>
<li><a href="?mode=edit_hsf&type=sidebar">サイドバー編集</a></li>
<li><a href="?mode=edit_hsf&type=footer">フッター編集</a></li>
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
<p>第一高等学校・東京大学弁論部<br>Ichiko Todai Benronbu</p>
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
	print "<h2>下層フォルダ</h2>";
	print "<div class=\"dirlist\">";
	print "<ul>";
	foreach (@all_dirs){
		print "<li><a href=\"?mode=&dir_pass=$dir_pass/$_\">$_</a></li>";
	}
	print "</ul>";
	print "</div>";
	print "<h2>HTMLファイル</h2>";
	print "<ul>";
	foreach (@all_html_files){
		print "<li>$_<br>[<a href=\"$dir_pass/$_\" target=\"_top\">表示</a>] [<a href=\"?mode=edit_html&dir_pass=$dir_pass&file_name=$_\">編集</a>] [<a href=\"#\" onClick=\"del(\'?mode=del_html&dir_pass=$dir_pass&file_name=$file_name$_\'); return false;\">削除</a>]</li>";
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
	open(FH, "$file_pass") or ERROR("$file_passの読み込みに失敗しました。");
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
<h3>新着情報を更新する</h3>
<form method="POST">
<p>タイトル： <input type="text" name="title" value=""></p>
<p>ジャンル：
<select name="category">
<option value="0" selected>運営</option>
<option value="1">弁論</option>
<option value="2">ディベート</option>
</select>
</p>
<p>内容：
<TEXTAREA name="text" rows="10" cols="50"></TEXTAREA>
</p>
<p>文字コード：
<select name="encode">
<option value="sjis" selected>Shift-JIS</option>
<option value="euc">EUC-JP</option>
<option value="utf8">UTF-8</option>
</select>
</p>
<p>
<input type="hidden" name="mode" value="write_news">
<input type="submit" value="更新">
</p>
</form>
<h3>このフォルダ内に新規HTMLファイルを作成する</h3>
<ul>
<li>最上層（../）フォルダでの新規作成を除き、相対パスが全て../基準から変更されません（特にスタイルシートの問題）</li>
<li>新規作成ファイルの殻となるのはindex.htmlです。index.htmlのtitleタグが1行で記述されていない場合、正常に動作しません。</li>
</ul>
<form method="POST">
<p>タイトル： <input type="text" name="new_title" value=""></p>
<p>ファイル名（.html以前）： <input type="text" name="file_name" value=""></p>
<p>文字コード：
<select name="encode">
<option value="sjis" selected>Shift-JIS</option>
<option value="euc">EUC-JP</option>
<option value="utf8">UTF-8</option>
</select>
</p>
<p>
<input type="hidden" name="mode" value="new_html">
<input type="hidden" name="dir_pass" value="$dir_pass">
<input type="submit" value="作成">
</p>
</form>
<h3>このフォルダの下に新規フォルダを作成する</h3>
<form method="POST">
<p>
フォルダ名： <input type="text" name="dir_name" value="">
<input type="hidden" name="mode" value="new_dir">
<input type="hidden" name="dir_pass" value="$dir_pass">
<input type="submit" value="作成">
</p>
</form>
<h3>このフォルダ内にファイルをアップロードする</h3>
<form method="POST" enctype="multipart/form-data">
<p> <input type="file" name="file_name" size="60"></p>
<p>
<input type="hidden" name="dir_pass" value="$dir_pass">
<input type="hidden" name="mode" value="upload">
<input type="submit" value="アップロード">
</p>
</form>
END
}

sub EDIT_HTML{
	local ($dir_pass, $file_name) = @_;
	unless ($file_name){
		&ERROR("file_nameの指定が不正です。");
	}
	my $file_pass = "$dir_pass/" . "$file_name";
	if ($text){
		&WRITE_DIV($dir_pass,$file_name,'content',$text,$encode);
		print "<font color=\"red\">編集が完了しました。</font>";
	}
	my $data = EXTRACT_DIV($file_pass, 'div', 'content', 'content');
	print "<h2>$file_passを編集中</h2>";
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
<input type="submit" value="書き換え">
</form>
END
}

sub WRITE_DIV{
	local ($dir_pass, $file_name, $id, $write_text, $encode) = @_;
	unless ($file_name){
		&ERROR("file_nameの指定が不正です。");
	}
	my $file_pass = "$dir_pass/" . "$file_name";
	unless ($write_text) {return;}
	my $before_div = EXTRACT_DIV($file_pass, 'div', $id, 'before');
	my $after_div = EXTRACT_DIV($file_pass, 'div', $id, 'after');
	my $content_attribute = EXTRACT_DIV($file_pass, 'div', $id, 'atr');
	open(FH, "> $file_pass") or ERROR("$file_passへの書き込みに失敗しました。");
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
		$data .= "<img src=\"../images/benron-ss.png\" alt=\"弁論\">";
	}elsif ($category == 2){
		$data .= "<img src=\"../images/debate-ss.png\" alt=\"ディベート\">";
	}else{
		$data .= "<img src=\"../images/unei-ss.png\" alt=\"運営\">";
	}
	$data .= " $title</h3>";
	$data .= " $text";
	my $data_news = EXTRACT_DIV('../index.html','div','news','content');
	my $write_text_index = "<ul>\n<li>$year.$mon.$mday \n";
	if ($category == 1){
		$write_text_index .= "<img src=\"../images/benron-ss.png\" alt=\"弁論\">";
	}elsif ($category == 2){
		$write_text_index .= "<img src=\"../images/debate-ss.png\" alt=\"ディベート\">";
	}else{
		$write_text_index .= "<img src=\"../images/unei-ss.png\" alt=\"運営\">";
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
	print "<li>index.htmlへの書き込みが完了しました。</li>";
	&NEW_HTML($file_name, '../news', $title, $encode, $data);
}

sub NEW_HTML{
	local ($file_name, $dir_pass, $title, $encode, $text) = @_;
	unless ($file_name){
		&ERROR("ファイル名を入力してください。");
	}
	unless ($title){
		&ERROR("タイトルを入力してください。");
	}
	my $file_pass = "$dir_pass/" . "$file_name" . ".html";
	if (-f $file_pass){
		ERROR("$file_passは既に存在しています。（上書き防止）");
	}
	my $model_pass = '../index.html';
	$new_title = jcode($new_title)->euc;
	my $before_div = EXTRACT_DIV($model_pass, 'div', 'content', 'before');
	my $after_div = EXTRACT_DIV($model_pass, 'div', 'content', 'after');
	my $content_attribute = EXTRACT_DIV($model_pass, 'div', 'content', 'atr');
	open(FH, "> $file_pass") or ERROR("$file_passへの書き込みに失敗しました（content）。");
	my $data = "$before_div<div $content_attribute>$text\n</div>\n$after_div";
	$data = jcode($data)->$encode;
	print FH $data;
	close(FH);
	my $before_title = EXTRACT_DIV($file_pass, 'title', '', 'before');
	my $after_title = EXTRACT_DIV($file_pass, 'title', '', 'after');
	my $title_attribute = EXTRACT_DIV($file_pass, '', 'title', 'atr');
	open(FH, "> $file_pass") or ERROR("$file_passへの書き込みに失敗しました（title）。");
	if ($title_attribute){
		$data = "$before_title<title $title_attribute>$new_title</title>\n$after_title";
	}else{
		$data = "$before_title<title>$new_title</title>\n$after_title";
	}
	$data = jcode($data)->$encode;
	print FH $data;
	close(FH);
	print "<li><font color=\"red\">$file_passを作成しました（戻るボタンは使用せず、上記メニューから選択してください。）</font></li>";
}

sub DEL_HTML{
	local ($dir_pass, $file_name) = @_;
	unless ($file_name){
		&ERROR("file_nameの指定が不正です。");
	}
	my $file_pass = "$dir_pass/" . "$file_name";
	if (unlink $file_pass) {
		print "<li><font color=\"red\">$file_passを削除しました</li></font>";
	}
	else{
		ERROR("$file_passを削除できませんでした。");
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
	else {&ERROR("コマンドが不正です");}
	if ($text){
		open(FH, "> $open_file") or ERROR("$open_fileが見つかりません。");
		print FH $text;
		close(FH);
		&OPEN_DIR("..",$type,$text,$encode);
		print "<font color=\"red\">編集が完了しました。</font>";
	}
	print "<h2>$typeを編集中</h2>";
	print "<form method=\"POST\">";
	print "<TEXTAREA name=\"text\" rows=\"20\" cols=\"100\">";
	open(FH, "$open_file") or ERROR("指定されたファイルが見つかりません。");
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
<input type="submit" value="書き換え">
</form>
END

}

sub UPLOAD{
	local ($dir_pass,$file_name) = @_;
	unless ($file_name){
		&ERROR("アップロードするファイルを選択してください。");
	}
	my $write_file = "$dir_pass". "/" . "$file_name";
	open(OUT, ">$write_file");
	binmode(OUT);
	while (read($file_name,$buffer,1024)){
		print OUT $buffer;
	}
	close(OUT);
	close($file_name);
	print "<font color=\"red\">$write_fileを作成しました（戻るボタンは使用せず、上記メニューから選択してください。）</font>";
}

sub NEW_DIR{
	local ($dir_pass,$dir_name) = @_;
	unless ($dir_name){
		&ERROR("フォルダ名を入力してください。");
	}
	my $write_dir = "$dir_pass". "/" . "$dir_name";
	if (-d "$write_dir"){
		ERROR("$wite_dirは既に存在しています。（上書き防止）");
	}
	mkdir "$write_dir";
	print "<font color=\"red\">$write_dirを作成しました（戻るボタンは使用せず、上記メニューから選択してください。）</font>";
}


sub ERROR{
	local ($text) = @_;
	print "<h2>$text</h2>";
	print "<ul><li>システム管理者に問い合わせてください。</li></ul>";
	&VIEW_FOOTER();
	exit;
}

exit;