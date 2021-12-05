#!/usr/bin/perl

use Jcode;
use CGI qw(:standard);

# パラメータ処理
$mode = param('mode');
$file_pass = param('file_pass');
$dir_pass = param('dir_pass');
unless ($dir_pass){$dir_pass = ".."};
$type = param('type');
$text = param('text');
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


# モード処理
if ($mode eq 'edit_html'){
	&VIEW_HEADER("ページの編集");
	&EDIT_HTML($file_pass);
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'edit_hsf'){
	&VIEW_HEADER("ヘッダー・サイドバー・フッターの編集");
	&EDIT_HSF($type);
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'file_make'){
	&VIEW_HEADER("新規HTMLファイル作成");
	&VIEW_FOOTER();
	exit;
}else{
	&VIEW_HEADER("メインページ");
	&VIEW_ALL_FILES($dir_pass);
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
<title>$title - Franken (ver.2.01)</title>
</head>
<body>
<div id="top">
Franken
</div>
<div id="header">
<ul>
<li><a href="index.cgi?mode=">メイン</a></li>
<li><a href="index.cgi?mode=edit_hsf&type=header">ヘッダー編集</a></li>
<li><a href="index.cgi?mode=edit_hsf&type=sidebar">サイドバー編集</a></li>
<li><a href="index.cgi?mode=edit_hsf&type=footer">フッター編集</a></li>
</ul>
</div>
<div style="clear:both;"></div>
<div id="main">
<div id="sidebar">
</div>
<div id="content">
END
}

sub VIEW_FOOTER{
	print <<END;
</div>
<div id="footer">
<i>Copyright(C)2014 Koki Ishii. All rights reserved.</i>
</div>
</div>
</body>
</html>
END
}

sub VIEW_ALL_FILES(){
	local ($dir_pass) = @_;
	print "現在の位置：";
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
	print "<h3>フォルダ一覧</h3>";
	print "<ul>";
	foreach (@all_dirs){
		print "<li><a href=\"?mode=&dir_pass=$dir_pass/$_\">$_</a></li>";
	}
	print "</ul>";
	print "<h3>HTMLファイル一覧</h3>";
	print "<ul>";
	foreach (@all_html_files){
		print "<li>$_ - [<a href=\"$dir_pass/$_\">表示</a>] [<a href=\"?mode=edit_html&file_pass=$dir_pass/$_\">編集</a>]</li>";
	}
	print "</ul>";
	print <<END;
<h3>このフォルダ内に新規HTMLファイルを作成する（未対応）</h3>
<form method="POST">
ファイル名：<input type="text" name="file_name" value="">
<input type="hidden" name="mode" value="file_make">
<input type="hidden" name="dir_pass" value="$dir_pass">
<input type="submit" value="作成">
</form>
END
}

sub EDIT_HTML{
	local ($file_pass) = @_;
	if ($text){
		&WRITE_DIV($file_pass,'content',$text,$encode);
		print "<font color=\"red\">編集が完了しました。</font>";
	}
	open(FH, "$file_pass") or ERROR("指定されたファイルが見つかりません。");
	my %counter;
	my %content;
	my %flg;
	my %id;
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		while ($data =~ /<\s*(\w+)\s*((?:"[^"]*"|'[^']*'|[^"'>])*?)(?:\s*\/\s*)?>/g){
			my $tag = $1;
			my $attribute = $2;
			my %attributes;
			while ($attribute =~ m/(\w+?)(?:\s*=\s*("[^"]*"|'[^']*'|[^"']*))?(?:\s+|$)/g){
				my $atr_name = $1;
				my $atr_value = $2;
				$atr_value =~ s/^(["'])(.*?)\1$/$2/;
				$attributes{$atr_name} = $atr_value;
			}
			$counter{$tag}++;
			$flg{$tag}[$counter{$tag}] = 1;
			$id{$tag}[$counter{$tag}] = $attributes{"id"};
		}
		foreach (keys(%flg)){
			for ($i = 1; $i < ($counter{$_} + 2); $i++){
				if ($flg{$_}[$i] == 1){
					my $data = $data;
					$content{$_}[$i] .= "$data\n";
				}
			}
		}
		while ($data =~ /<\s*\/\s*(\w+)\s*>/g){
			my $tag = $1;
			for ($i = $counter{$tag}; $i > 0; $i--){
				if ($flg{$tag}[$i] == 1){
					$flg{$tag}[$i] = 0;
					last;
				}
			}
		}

	}
	close(FH);
	print "<h3>$file_passを編集中</h3>";
	print "<form method=\"POST\">";
	print "<TEXTAREA name=\"text\" rows=\"20\" cols=\"100\">";
	for ($i = 1; $i < ($counter{"div"} + 1); $i++){
		if ($id{"div"}[$i] eq 'content'){
			my $text = $content{"div"}[$i];
			chomp($text);
			$text =~ s/^\s*<\s*div[^>]*>(.*?)/$1/ig;
			$text =~ s/(.*?)<\s*\/\s*div\s*>\s*$/$1/ig;
			print "$text";
		}
	}
	print "</TEXTAREA>";
	print "<br>";
	print <<END;
<select name="encode">
<option value="sjis" selected>Shift-JIS</option>
<option value="euc">EUC-JP</option>
<option value="utf8">UTF-8</option>
</select>
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="file_pass" value="$file_pass">
<input type="submit" value="書き換え">
</form>
END
}

sub WRITE_DIV{
	local ($file_pass,$id,$wite_text,$encode) = @_;
	unless ($wite_text) {return;}
	my $before_div;
	my $after_div;
	my $target_counter;
	my $counter;
	my $content;
	my @flg;
	open(FH, "$file_pass") or ERROR("$file_passが見つかりません。（読み込み時のエラー）");
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		unless ($flg[$target_counter] == 2){
		while ($data =~ /<\s*div\s*((?:"[^"]*"|'[^']*'|[^"'>])*?)(?:\s*\/\s*)?>/ig){
			my $attribute = $1;
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
				$target_counter = $counter;
			}
		}
		if ($flg[$target_counter] == 1){
			$content .= "$data\n";
		}elsif ($flg[$target_counter] == 0){
			$before_div .= "$data\n";
		}
		while ($data =~ /<\s*\/\s*div\s*>/ig){
			for ($i = $counter; $i > 0; $i--){
				if ($flg[$i] == 1){
					if ($i == $target_counter){
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
	close(FH);
	open(FH, "> $file_pass") or ERROR("$file_passが見つかりません。（書き込み時のエラー）");
	my $data = "$before_div<div id=\"$id\">\n$wite_text</div>\n$after_div";
	$data = jcode($data)->$encode;
	print FH $data;
	close(FH);
}

sub OPEN_DIR{
	local ($dir_pass,$type,$text,$encode) = @_;
	opendir (DIR, "$dir_pass");
	foreach (readdir(DIR)){
		next if /^\.{1,2}$/;
		if (-d "$dir_pass/$_"){
			&OPEN_DIR("$dir_pass/$_",$type,$text,$encode);
		}elsif ($_ =~ /\.html?$/){
			&WRITE_DIV("$dir_pass/$_",$type,$text,$encode);
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
	print "<h3>$typeを編集中</h3>";
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

sub ERROR{
	local ($text) = @_;
	print "<h2>$text</h2>";
	print "<ul><li>システム管理者に問い合わせてください。</li></ul>";
	&VIEW_FOOTER();
	exit;
}

exit;