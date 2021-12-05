#!/usr/bin/perl

use Jcode;
use CGI qw(:standard);
use Image::Magick;

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
}elsif ($mode eq 'edit_news'){
	&VIEW_HEADER("新着情報更新");
	&VIEW_SIDEBAR($dir_pass);
	&EDIT_NEWS();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'edit_poster'){
	&VIEW_HEADER("ポスター掲示板更新");
	&VIEW_SIDEBAR($dir_pass);
	&EDIT_POSTER();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'write_news'){
	&VIEW_HEADER("新着情報更新");
	&VIEW_SIDEBAR($dir_pass);
	&WRITE_NEWS($title,$text,$category,$encode);
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'write_poster'){
	&VIEW_HEADER("ポスター掲示板更新");
	&VIEW_SIDEBAR($dir_pass);
	&WRITE_POSTER($file_name, $title, $encode, $url, $type, $no);
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
<title>$title - ichigochan (ver.2.05)</title>
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

<div id="top">
<b>ichigochan</b> - ITBウェブページ管理システム
</div>
<div id="header">
<ul>
<li><a href="?mode=">メインページ</a></li>
<li><a href="?mode=edit_news">新着情報</a></li>
<li><a href="?mode=edit_poster">ポスター掲示板</a></li>
<li><a href="?mode=edit_hsf&type=header">ヘッダー</a></li>
<li><a href="?mode=edit_hsf&type=sidebar">サイドバー</a></li>
<li><a href="?mode=edit_hsf&type=footer">フッター</a></li>
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
<p>第一高等学校・東京大学弁論部<br>Ichiko Todai Benronbu</p>
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
	if ($dir_pass eq '..'){
		print "<h2>メインページ</h2>";
		print "<p>ようこそ。<b>ichigochan</b>は第一高等学校・東京大学弁論部公式サイトを管理するためのシステムです。</p>";
		print "<p>システム作成者は<a href=\"mailto:daabubu@gmail.com\">石井</a>（124期）です。システムの動作に関するお問い合わせはこちらまで。</p>";
		print "<ul><li>フォルダを移動する場合は、サイドバーの「下層フォルダ」から移動先のフォルダを選択してください。</li><li>現在のフォルダ内にあるHTMLファイル（ウェブページ）の一覧はサイドバーの「HTMLファイル」に列記されています。ページを編集する場合は、ファイル名の下の「編集」を、削除する場合は「削除」を選択してください。</li></ul>";
	}else{
		print "<h2>$dir_pass</h2>";
	}
	print <<END;
<h3>新規HTMLファイル作成</h3>
<p>このフォルダ内に白紙のHTMLファイルを作成します。</p>
<h4>手順</h4>
<ol>
<li>以下の欄を全て埋めた上で「作成」を選択します。</li>
<li>白紙のファイルが作成されるので、左のサイドバーから作成したファイルを探し、「編集」を選択して編集します。</li>
</ol>
<form method="POST">
<fieldset><legend>記入欄</legend>
<p>タイトル： <input type="text" name="new_title" value=""> 例）「大会結果」</p>
<p>ファイル名（.html以前。半角英数字）： <input type="text" name="file_name" value=""> 例）「index」,「tatenokai」</p>
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
</fieldset>
</form>
<h4>注意</h4>
<ul>
<li>新規作成ファイルの殻となるのはindex.htmlです。index.htmlのtitleタグが1行で記述されていない場合、正常に動作しません。</li>
</ul>
<h3>新規フォルダ作成</h3>
<p>このフォルダの下層に新しいフォルダ（サブフォルダ）を作成します。</p>
<h4>手順</h4>
<ol>
<li>フォルダ名を入力し、「作成」を選択します。</li>
</ol>
<form method="POST">
<fieldset><legend>記入欄</legend>
<p>
フォルダ名（半角英数字）： <input type="text" name="dir_name" value=""> 例）「event」
<input type="hidden" name="mode" value="new_dir">
<input type="hidden" name="dir_pass" value="$dir_pass">
</p>
<p><input type="submit" value="作成"></p>
</fieldset>
</form>
<h3>ファイルのアップロード</h3>
<p>このフォルダ内にファイルをアップロードします。HTMLファイルだけでなく、画像ファイル等もアップロードすることができます。</p>
<h4>手順</h4>
<ol>
<li>「参照」（Chromeは「ファイルを選択」）を選択します。</li>
<li>「開く」ウィンドウが開くので、アップロードしたいファイルを選択して右下の「開く(O)」を選択します。</li>
<li>「アップロード」ボタンを選択します。</li>
</ol>
<form method="POST" enctype="multipart/form-data">
<fieldset><legend>記入欄</legend>
<p> <input type="file" name="file_name"></p>
<p>
<input type="hidden" name="dir_pass" value="$dir_pass">
<input type="hidden" name="mode" value="upload">
<input type="submit" value="アップロード">
</p>
</fieldset>
</form>
<h4>注意</h4>
<ul>
<li>同一名のファイルが存在する場合、<u>上書きされます</u>。</li>
<li>画像をアップロードしてウェブページ内に引用する場合は、画像のファイル名を半角英数字（＋一部の記号）のみで記述する必要があります。アップロードするファイルの名前が半角英数字等で記述されているか確認してください。</li>
</ul>
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
	print <<END;
<h2>$file_passを編集中</h2>
<p>HTMLファイルを編集します。</p>
<h4>手順</h4>
<ol>
<li>「内容」欄に記事を入力します。HTMLタグを用いて記述する場合は、「<>」ボタンを選択してください。</li>
<li>「文字コード」（デフォルトは「Shift-JIS」）を選択した上で「書き換え」を選択します。</li>
</ol>
<form method="POST">
<fieldset><legend>記入欄</legend>
<p>内容：
<TEXTAREA name="text" rows="20">$data</TEXTAREA>
</p>
<p>文字コード：
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
<input type="submit" value="書き換え">
</p>
</fieldset>
</form>
END
}

sub EDIT_NEWS{
	print <<END;
<h2>新着情報更新</h2>
<p><img src="./images/screen2.png"></p>
<p>新着情報一覧に、新しい新着情報を追加します。</p>
<h4>手順</h4>
<ol>
<li>「タイトル」に記事のタイトルを入力します。これはトップページ（../index.html）の「新着情報」一覧に掲載されるほか、記事ページのタイトルにもなります。</li>
<li>「ジャンル」を選択します。弁論関連の記事であれば「弁論」、ディベート関連であれば「ディベート」、それ以外は「運営」を選択することが想定されています。</li>
<li>「内容」に記事の内容を入力します。ここで入力した情報はトップページの「新着情報」一覧からリンクを飛んだ先の記事ページに掲載されるものです。「<>」ボタンを選択するとHTMLタグを用いた編集ができます。</li>
<li>「文字コード」を選択します。通常は「Shift-JIS」のままにしておきます。</li>
<li>内容を確認し、「更新」を選択します。</li>
</ol>
<form method="POST">
<fieldset><legend>記入欄</legend>
<p>タイトル： <input type="text" name="title" value=""> 例）「第37回学生新人弁論大会に出場しました。」</p>
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
</fieldset>
</form>
END
}

sub EDIT_POSTER{
	print <<END;
<h2>ポスター掲示板編集</h2>
<p><img src="./images/screen1.png"></p>
<p>ポスター掲示板に掲示されたポスターの追加・削除、「終了しました」バナーを付加・除去します。</p>
<h3>現在の掲示板</h3>
<ul>
<li>数字の順番に左から掲示されます。</li>
<li>「終了にする」／「終了をはずす」を選択すると、「終了しました」バナーを付けたり外したりすることができます。</li>
<li>「削除」を選択すると、そのポスターを掲示板から削除します。ただし画像ファイルはサーバー上からは削除されません。</li>
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
		print "[<a href=\"$poster_image\">画像を表示</a>] ";
		if ($end_flg){
			print "[<a href=\"?mode=write_poster&type=end&no=$i\">終了をはずす</a>]";
		}else{
			print "[<a href=\"?mode=write_poster&type=end&no=$i\">終了にする</a>]";
		}
		print " [<a href=\"?mode=write_poster&type=del&no=$i\">削除</a>]";
		print "</li>";
		$i++;
	}
	print "</ol>";
	print <<END;
<h3>新しいポスターを追加する</h3>
<h4>手順</h4>
<ol>
<li>「画像」欄の「参照」（Chromeは「ファイルを選択」）を選択し、「開く」ウィンドウが開いたら、アップロードしたいファイルを選択して右下の「開く(O)」を選択します。</li>
<li>「リンク先のアドレス」を入力します。これは、ポスターをクリックすると飛ぶ詳細なイベント情報のページのアドレスが想定されています。<br>基本的にイベントページは「event」フォルダの中で集中的に管理されています。新しくページを作る場合は、左のサイドバーから「event」フォルダを選択して、「新規HTMLファイルの作成」から白紙のページを作成したあと、サイドバーから「編集」します。その際作成したページのアドレスを記憶しておき、ポスターを掲示する際にこの「リンク先のアドレス」欄に入力します。</li>
<li>「イベントのタイトル」を入力し、「文字コード」を選択した上で「追加」を選択します。</li>
</ol>
<form method="POST" enctype="multipart/form-data">
<fieldset><legend>記入欄</legend>
<ul>
<p>画像： <input type="file" name="file_name"></p>
<p>リンク先のアドレス： <input type="text" name="url"> 例）五月祭なら「http://utbenron.com/event/mayfest.html」</li>
<p>イベントのタイトル： <input type="text" name="title"> 例）「第10回五月祭記念弁論大会」</p>
<p>文字コード：
<select name="encode">
<option value="sjis" selected>Shift-JIS</option>
<option value="euc">EUC-JP</option>
<option value="utf8">UTF-8</option>
</select>
</p>
<p><input type="hidden" name="mode" value="write_poster"><input type="hidden" name="type" value="add"><input type="submit" value="追加"></p>
</fieldset>
<h4>注意</h4>
<ul>
<li><u>アップロードするポスター画像のファイル名が半角英数字であることを確認してください。</u></li>
<li>ポスターのサイズは縦200px、横141pxがデフォルトです。それより大きいファイルを選択した場合、自動的に高さが200pxに揃えられます。</li>
<li>ポスターの順番を入れ替えたいときは、一度全て「削除」した上で「新しいポスターを追加する」から正しい順番に追加します。</li>
<li>ポスターの掲載だけでなく、詳細ページの編集も行ってください。</li>
<ul>
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
			&ERROR("アップロードするファイルを選択してください。");
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
	print "<li>index.htmlへの書き込みが完了しました。</li>";
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
	print <<END;
<h2>$typeを編集中</h2>
<p><b>全ての</b>ページのヘッダー／サイドバー／フッターを書き換えます。</p>
<p>divタグを使用する場合は<b>絶対に</b>開いたタグと閉じたタグの個数が同一であることを確認してください（可能であれば<u>divタグを使用しないでください</u>）。万一失敗すると、全ての編集システムの機能が使用できなくなります。</p>
<h4>手順</h4>
<ol><li>基本的に「編集」と同じです。</li></ol>
<form method="POST">
<fieldset><legend>記入欄</legend>
<p>内容：
<TEXTAREA name="text" rows="20">
END
	open(FH, "$open_file") or ERROR("指定されたファイルが見つかりません。");
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		print "$data\n";
	}
	close(FH);
	print <<END;
</TEXTAREA>
</p>
<p>文字コード：
<select name="encode">
<option value="sjis" selected>Shift-JIS</option>
<option value="euc">EUC-JP</option>
<option value="utf8">UTF-8</option>
</select>
</p>
<p>
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="type" value="$type">
<input type="submit" value="書き換え">
</p>
</fieldset>
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
	close($write_file);
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