#!/usr/bin/perl

# モジュール
use Jcode;
use Time::Local;
use CGI qw(:standard);

# 日付関連グローバル変数
$time = time;
($sec, $min, $hour, $date, $mon, $year, $wday) = localtime($time);
$year += 1900;
$mon++;

# パラメータ処理
$mode = param('mode');
$type = param('type');
$pass = param('pass');
## カレンダーの現在地
$cyear = param('cyear');
unless($cyear){
	$cyear = $year;
}
$cmon = param('cmon');
unless($cmon){
	$cmon = $mon;
}
$cdate = param('cdate');
## 予約関連　※スクリプト排除をちゃんとやったほうが良い
$rpass = param('rpass');
$rcomment = param('rcomment');
$ryear = param('ryear');
$rmon = param('rmon');
$rdate = param('rdate');
$rhour_b = param('rhour_b');
$rmin_b = param('rmin_b');
$rhour_e = param('rhour_e');
$rmin_e = param('rmin_e');
$rplace = param('rplace');
$rplace = jcode($rplace)->euc;
$rname = param('rname');
$rname = jcode($rname)->euc;

$ifrom = param('ifrom');
$ifrom = jcode($ifrom)->euc;
$iki = param('iki');
$imail = param('imail');

$aname = param('aname');
my $num = 0;
while(1){
	$akanji[$num] = param('akanji' . $num);
	$aki[$num] = param('aki' . $num);
	$amail[$num] = param('amail' . $num);
	unless($akanji[$num]){
		$num_akanji = $num;
		last;
	}
	$num++;
}
$aintro = param('aintro');

# モード処理（メイン）
if ($mode eq 'reserve'){
	&VIEW_HEADER('予約');
	&RESERVE();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'cancel'){
	&VIEW_HEADER('予約取消');
	&CANCEL();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'comment'){
	&VIEW_HEADER('コメント');
	&VIEW_COMMENT();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'lists'){
	&VIEW_HEADER('部会一覧');
	&VIEW_LISTS_OF_BUKAI();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'detail'){
	&VIEW_HEADER('部会紹介');
	&VIEW_DETAIL();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'join'){
	&VIEW_HEADER('参加希望');
	&VIEW_JOIN();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'send'){
	&VIEW_HEADER('参加希望');
	&SEND_MAIL();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'admin'){
	&VIEW_HEADER('管理');
	&VIEW_ADMIN();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'view_reserve'){
	&VIEW_HEADER('予約');
	&VIEW_RESERVE();
	&VIEW_FOOTER();
	exit;
}else{
	&VIEW_HEADER('部会ナビ');
	&VIEW_MAIN();
	&VIEW_FOOTER();
	exit;
}

# ヘッダー表示
sub VIEW_HEADER(){
	local($title) = @_;
	print "Content-type: text/html\n\n";
	print <<END;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=euc-jp" />
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="style.css" rel="stylesheet" type="text/css">
<title>$title - 第一高等学校・東京大学弁論部</title>
<script type="text/javascript">
<!--
var ItemField = {
    add : function () {
        this.currentNumber++;

        var field = document.getElementById('item' + this.currentNumber);

        var newItem = this.itemTemplate.replace(/__count__/mg, this.currentNumber);
        field.innerHTML = newItem;

        var nextNumber = this.currentNumber + 1;
        var new_area = document.createElement("tr");
        new_area.setAttribute("id", "item" + nextNumber);
	var objBody = document.getElementById('wrapper');
	objBody.appendChild(new_area);
    },
    remove : function () {
        if ( this.currentNumber == 0 ) { return; }

        var field = document.getElementById('item' + this.currentNumber);
        field.removeChild(field.lastChild);
        field.innerHTML = '';

        this.currentNumber--;
    }
}
// -->
</script>

</head>
<body>
<div id="top">部会NAVI</div>
<div id="main">
<div id="content">
END
}

# フッター表示
sub VIEW_FOOTER(){
	print <<END;
</div>
<div id="footer">
<p><a href=\"?mode=admin\">管理ページ</a></p>
<p>Copyright(C)2016 第一高等学校・東京大学弁論部. All rights reserved.</p>
</div>
</div>
</body>
</html>
END
}

# メインページ表示
sub VIEW_MAIN(){
	print <<END;
<div id="header">
<ul>
<li><a href="?mode=" class="open">予約状況</a></li>
<li><a href="?mode=lists">部会一覧</a></li>
</ul>
</div>
END
	my $file_pass = './data/reserve.dat';
	open(FH, "$file_pass") or ERROR("$file_passが見つかりません。");
	my $num_reserved = 0;
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		@sdata = split(/\//,$data);
		for (my $i = 0; $i <= $#sdata; $i++){
			$reserved[$num_reserved][$i] = $sdata[$i];
		}
		if ($cyear == $reserved[$num_reserved][2] && $cmon == $reserved[$num_reserved][3]){
			if ($reserved[$num_reserved][1] eq '駒場部室'){
				$komaba[$reserved[$num_reserved][4]][$num_komaba[$reserved[$num_reserved][4]]] = $num_reserved;
				$num_komaba[$reserved[$num_reserved][4]]++;
			}
			elsif ($reserved[$num_reserved][1] eq '本郷部室'){
				$hongo[$reserved[$num_reserved][4]][$num_hongo[$reserved[$num_reserved][4]]] = $num_reserved;
				$num_hongo[$reserved[$num_reserved][4]]++;
			}
		}
		$num_reserved++;
	}
	close(FH);
my $byear;
my $bmon;
my $ayear;
my $amon;
if ($cmon == 1){
	$byear = $cyear - 1;
	$bmon = 12;
	$ayear = $cyear;
	$amon = $cmon + 1;
}elsif ($cmon == 12){
	$ayear = $cyear + 1;
	$amon = 1;
	$byear = $cyear;
	$bmon = $cmon - 1;
}else{
	$ayear = $cyear;
	$amon = $cmon + 1;
	$byear = $cyear;
	$bmon = $cmon - 1;
}
	print <<END;
<p style="text-align:center;"><a href="?cyear=$byear&cmon=$bmon">&lt;&lt;</a> $cyear年$cmon月 <a href="?cyear=$ayear&cmon=$amon">&gt;&gt;</a></p>
END
	@days = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
	if ($cmon == 2 and ($cyear % 4 == 0 and $cyear % 100 != 0 or $cyear % 400 == 0)) {
		$days[1]++; # うるう年
	}
	$enddate = $days[$cmon - 1]; # 月の日数
	@wdays = ("日","月","火","水","木","金","土");
	for ($i = 1 ; $i <= $enddate ; $i++) {
		$cwday = (localtime( timelocal(0, 0, 0, $i, $cmon - 1, $cyear)))[6];
		if ($cyear < $year || ($cyear == $year && $cmon < $mon) || ($cyear == $year && $cmon == $mon && $i < $date)){
			next;
		}
		print "<h3>$cmon月$i日（$wdays[$cwday]）</h3>";
		print "<div class=\"bukai\">";
		print "<h4>駒場部室</h4>";
		print "<ul>";
		my @aaa;
		for (my $j = 0; $j < $num_komaba[$i]; $j++){
			for (my $k = 0; $k < 11; $k++){
				$aaa[$j][$k] = $reserved[$komaba[$i][$j]][$k];
			}
		}
		@aaa = sort { ($a->[5] * 60 + $a->[6]) <=> ($b->[5] * 60 + $b->[6]) } @aaa;
		for (my $j = 0; $j < $num_komaba[$i]; $j++){
			my $detail_url = "?mode=detail&rname=$aaa[$j][0]";
			my $cancel_url = "?mode=cancel&rplace=$aaa[$j][1]&ryear=$aaa[$j][2]&rmon=$aaa[$j][3]&rdate=$aaa[$j][4]&rhour_b=$aaa[$j][5]&rmin_b=$aaa[$j][6]&rhour_e=$aaa[$j][7]&rmin_e=$aaa[$j][8]";
			my $join_url = "?mode=join&rname=$aaa[$j][0]&rplace=$aaa[$j][1]&ryear=$aaa[$j][2]&rmon=$aaa[$j][3]&rdate=$aaa[$j][4]&rhour_b=$aaa[$j][5]&rmin_b=$aaa[$j][6]&rhour_e=$aaa[$j][7]&rmin_e=$aaa[$j][8]";
			my $min_b = sprintf("%02d",$aaa[$j][6]);
			my $min_e = sprintf("%02d",$aaa[$j][8]);
			my $comment_url;
			if ($aaa[$j][10]){
				$comment_url = "?mode=comment&rplace=$aaa[$j][1]&ryear=$aaa[$j][2]&rmon=$aaa[$j][3]&rdate=$aaa[$j][4]&rhour_b=$aaa[$j][5]&rmin_b=$aaa[$j][6]&rhour_e=$aaa[$j][7]&rmin_e=$aaa[$j][8]"
			}
			print "<li>";
			print "<p class=\"time\"><span class=\"time1\">$aaa[$j][5]:$min_b</span><span class=\"time2\">〜$aaa[$j][7]:$min_e</span></p>";
			print "<p class=\"name\"><a href=\"$detail_url\" target=\"_blank\">$aaa[$j][0]部会</a></p>";
			print "<p class=\"links\">";
			if ($comment_url){
				print "<a href=\"$comment_url\" target=\"_blank\">詳細</a>&nbsp;|&nbsp;";
			}
			print "<a href=\"$join_url\" target=\"_blank\">参加</a>&nbsp;|&nbsp;<a href=\"$cancel_url\" target=\"_blank\">取消</a>";
			print "</p>";
			print "</li>";
		}
		unless ($num_komaba[$i]){
			print "</ul><ul class=\"no_reserve\"><li>";
			print "<p class=\"name\"><a href=\"#\">予約なし</a></p>";
			print "<p class=\"links\"><a href=\"?mode=view_reserve&cyear=$cyear&cmon=$cmon&cdate=$i\" target=\"_blank\">今すぐ予約</a></p>";
			print "</li>";
		}
		print "</ul>";
		print "</div><div style=\"clear:both\"></div>";
		print "<div class=\"bukai\">";
		print "<h4>本郷部室</h4>";
		print "<ul>";
		my @aaa;
		for (my $j = 0; $j < $num_hongo[$i]; $j++){
			for (my $k = 0; $k < 11; $k++){
				$aaa[$j][$k] = $reserved[$hongo[$i][$j]][$k];
			}
		}
		@aaa = sort { ($a->[5] * 60 + $a->[6]) <=> ($b->[5] * 60 + $b->[6]) } @aaa;
		for (my $j = 0; $j < $num_hongo[$i]; $j++){
			my $detail_url = "?mode=detail&rname=$aaa[$j][0]";
			my $cancel_url = "?mode=cancel&rplace=$aaa[$j][1]&ryear=$aaa[$j][2]&rmon=$aaa[$j][3]&rdate=$aaa[$j][4]&rhour_b=$aaa[$j][5]&rmin_b=$aaa[$j][6]&rhour_e=$aaa[$j][7]&rmin_e=$aaa[$j][8]";
			my $join_url = "?mode=join&rname=$aaa[$j][0]&rplace=$aaa[$j][1]&ryear=$aaa[$j][2]&rmon=$aaa[$j][3]&rdate=$aaa[$j][4]&rhour_b=$aaa[$j][5]&rmin_b=$aaa[$j][6]&rhour_e=$aaa[$j][7]&rmin_e=$aaa[$j][8]";
			my $min_b = sprintf("%02d",$aaa[$j][6]);
			my $min_e = sprintf("%02d",$aaa[$j][8]);
			my $comment_url;
			if ($aaa[$j][10]){
				$comment_url = "?mode=comment&rplace=$aaa[$j][1]&ryear=$aaa[$j][2]&rmon=$aaa[$j][3]&rdate=$aaa[$j][4]&rhour_b=$aaa[$j][5]&rmin_b=$aaa[$j][6]&rhour_e=$aaa[$j][7]&rmin_e=$aaa[$j][8]"
			}
			print "<li>";
			print "<p class=\"time\"><span class=\"time1\">$aaa[$j][5]:$min_b</span><span class=\"time2\">〜$aaa[$j][7]:$min_e</span></p>";
			print "<p class=\"name\"><a href=\"$detail_url\" target=\"_blank\">$aaa[$j][0]部会</a></p>";
			print "<p class=\"links\">";
			if ($comment_url){
				print "<a href=\"$comment_url\" target=\"_blank\">詳細</a>&nbsp;|&nbsp;";
			}
			print "<a href=\"$join_url\" target=\"_blank\">参加</a>&nbsp;|&nbsp;<a href=\"$cancel_url\" target=\"_blank\">取消</a>";
			print "</p>";
			print "</li>";
		}
		unless ($num_hongo[$i]){
			print "</ul><ul class=\"no_reserve\"><li>";
			print "<p class=\"name\"><a href=\"#\">予約なし</a></p>";
			print "<p class=\"links\"><a href=\"?mode=view_reserve&cyear=$cyear&cmon=$cmon&cdate=$i\" target=\"_blank\">今すぐ予約</a></p>";
			print "</li>";
		}
		print "</ul>";
		print "</div><div style=\"clear:both\"></div>";
		print "<a class=\"button\" href=\"?mode=view_reserve&cyear=$cyear&cmon=$cmon&cdate=$i\" target=\"_blank\">予約</a>";
	}
	print <<END;
END
}

# 部会一覧表示
sub VIEW_LISTS_OF_BUKAI{
	print <<END;
<div id="header">
<ul>
<li><a href="?mode=">予約状況</a></li>
<li><a href="?mode=lists" class="open">部会一覧</a></li>
</ul>
</div>
END
	my $file_pass = './data/bukai.dat';
	open(FH, "$file_pass") or ERROR("$file_passが見つかりません。");
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		@sdata = split(/\#\#/,$data);
		my $kanji;
		my @name_s = split(/\,/, $sdata[1]);
		my @ki_s = split(/\,/, $sdata[2]);
		my @mail_s = split(/\,/, $sdata[3]);
		for (my $i = 0; $i < $#name_s + 1; $i++){
			$kanji .= "<li>$name_s[$i]（$ki_s[$i]期）</li>";
		}
		print "<h5>$sdata[0]部会</h5><div class=\"whitebox\"><p><ul>$kanji</ul></p><p>$sdata[4]</p></div>";
	}
	close(FH);
	print <<END;
END
}

# 予約フォーム表示
sub VIEW_RESERVE(){
	print <<END;
<h2>$cyear年$cmon月$cdate日 予約</h2>
<form method = "POST">
<table>
<tr><th>部会名</th><td><input type = "text" name = "rname" value = "">部会</td></tr>
<tr><th>場所</th><td><select name = "rplace">
<option value="駒場部室" selected>駒場部室</option>
<option value="本郷部室">本郷部室</option>
</select>
</td></tr>
END
print "<tr><th>時間</th><td>";
print "<select name = \"rhour_b\">";
for (my $i = 8; $i <= 21; $i++){
	print "<option value=\"$i\">$i</option>";
}
print "</select>時";
print "<select name = \"rmin_b\">";
for (my $i = 0; $i <= 59; $i++){
	print "<option value=\"$i\">$i</option>";
}
print "</select>分〜";
print "<select name = \"rhour_e\">";
for (my $i = 8; $i <= 21; $i++){
	print "<option value=\"$i\"";
	if ($i == 9){
		print " selected";
	}
	print ">$i</option>";
}
print "</select>時";
print "<select name = \"rmin_e\">";
for (my $i = 0; $i <= 59; $i++){
	print "<option value=\"$i\">$i</option>";
}
print "</select>分";
print "</td></tr>";
	print <<END;
<tr><th>取消用パス</th><td><input type="password" name="rpass" value=""><br>※ 半角数字4文字</td></tr>
<tr><th>コメント</th><td><textarea name="rcomment" rows="10" cols="20"></textarea></td></tr>
</table>
<p><input class="button" type = "submit" value = "予約"></p>
<input type = "hidden" name = "ryear" value = "$cyear">
<input type = "hidden" name = "rmon" value = "$cmon">
<input type = "hidden" name = "rdate" value = "$cdate">
<input type = "hidden" name = "mode" value = "reserve">
</form>
<p><a class="button" href="javascript:;" onclick="window.close();">戻る</a></p>
END
}

# コメント表示
sub VIEW_COMMENT(){
	my $file_pass = './data/reserve.dat';
	open(FH, "$file_pass") or ERROR("$file_passが見つかりません。");
	my @target;
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		@sdata = split(/\//,$data);
		if ($sdata[1] eq $rplace && $sdata[2] == $ryear && $sdata[3] == $rmon && $sdata[4] == $rdate && $sdata[5] == $rhour_b && $sdata[6] == $rmin_b && $sdata[7] == $rhour_e && $sdata[8] == $rmin_e){
			@target = @sdata;
			last;
		}
	}
	close(FH);
	if ($target[10]){
		print "<h2>$target[0]部会</h2>";
		print "<h3>$target[2]年$target[3]月$target[4]日$target[5]時$target[6]分〜$target[7]時$target[8]分 ＠$target[1]</h3>";
		print "$target[10]";
	}else{
		print "コメントはありません。";
	}
	print "<p><a class=\"button\" href=\"javascript:;\" onclick=\"window.close();\">閉じる</a></p>";
}

# 予約関連処理
sub RESERVE(){
	unless (&CHECK_BUKAI($rname)){
		&ERROR("<i>$rname部会</i>は、部会一覧に登録された部会ではありません。");
	}
	if (($rhour_b * 60 + $rmin_b) >= ($rhour_e * 60 + $rmin_e)){
		&ERROR("予約時間が不正です。");
	}
	unless ($rpass =~ /^\d{4}$/){
		&ERROR("パスワードは半角数字4文字です。");
	}
	if ($ryear < $year || ($ryear == $year && $rmon < $mon) || ($ryear == $year && $rmon == $mon && $rdate <= $date)){
		&ERROR("翌日以降の予約しかできません。");
	}
	$rname =~ s/\</＜/igo;
	$rname =~ s/\>/＞/igo;
	$rname =~ s/\//／/igo;
	$rname =~ s/\n//igo;
	$rname =~ s/\r//igo;
	$rcomment =~ s/\</＜/igo;
	$rcomment =~ s/\>/＞/igo;
	$rcomment =~ s/\//／/igo;
	$rcomment =~ s/\r\n/<br>/igo;
	$rcomment =~ s/\r/<br>/igo;
	$rcomment =~ s/\n/<br>/igo;
	my $file_pass = './data/reserve.dat';
	open(FH, "$file_pass") or ERROR("$file_passが見つかりません。");
	my $num_reserved = 0;
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		@sdata = split(/\//,$data);
		for (my $i = 0; $i <= $#sdata; $i++){
			$reserved[$num_reserved][$i] = $sdata[$i];
		}
		$num_reserved++;
	}
	close(FH);
	for (my $i = 0; $i < $num_reserved; $i++){
		if ($rplace eq $reserved[$i][1] && $ryear == $reserved[$i][2] && $rmon == $reserved[$i][3] && $rdate == $reserved[$i][4]){
			if (($rhour_b * 60 + $rmin_b) <= ($reserved[$i][7] * 60 + $reserved[$i][8]) && ($reserved[$i][5] * 60 + $reserved[$i][6]) <= ($rhour_e * 60 + $rmin_e)){
				&ERROR("予約時間が重複しています。");
			}
		}
	}
	open(FH, ">> $file_pass") or ERROR("$file_passへの書き込みに失敗しました。");
	my $data = "$rname/$rplace/$ryear/$rmon/$rdate/$rhour_b/$rmin_b/$rhour_e/$rmin_e/$rpass/$rcomment\n";
	$data = jcode($data)->euc;
	print FH $data;
	close(FH);
	print <<END;
<h2>予約が完了しました。</h2>
<table>
<tr><th>名称</th><td>$rname</td></tr>
<tr><th>場所</th><td>$rplace</td></tr>
<tr><th>日時</th><td>$ryear年$rmon月$rdate日$rhour_b時$rmin_b分〜$rhour_e時$rmin_e分</td></tr>
<tr><th>コメント</th><td>$rcomment</td></tr>
</table>
<p><a class="button" href="javascript:;" onclick="window.opener.location.reload();window.close();">閉じる</a></p>
END
}

# 取消処理
sub CANCEL(){
	my $file_pass = './data/reserve.dat';
	open(FH, "$file_pass") or ERROR("$file_passが見つかりません。");
	my $num_reserved = 0;
	my $flg;
	my $c_pass;
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		@sdata = split(/\//,$data);
		if ($sdata[1] eq $rplace && $sdata[2] == $ryear && $sdata[3] == $rmon && $sdata[4] == $rdate && $sdata[5] == $rhour_b && $sdata[6] == $rmin_b && $sdata[7] == $rhour_e && $sdata[8] == $rmin_e){
			$flg = 1;
			$c_pass = $sdata[9];
			next;
		}
		for (my $i = 0; $i <= $#sdata; $i++){
			$reserved[$num_reserved][$i] = $sdata[$i];
		}
		$num_reserved++;
	}
	close(FH);
	unless ($flg){
		&ERROR("指定の予約が見つかりませんでした。");
	}
	unless ($pass eq $c_pass){
		print <<END;
<h2>取消用パスワードを入力してください</h2>
<form method="POST">
<input type="password" name="pass" value="">
<input type="hidden" name="mode" value="cancel">
<input type="hidden" name="rplace" value="$rplace">
<input type="hidden" name="ryear" value="$ryear">
<input type="hidden" name="rmon" value="$rmon">
<input type="hidden" name="rdate" value="$rdate">
<input type="hidden" name="rhour_b" value="$rhour_b">
<input type="hidden" name="rmin_b" value="$rmin_b">
<input type="hidden" name="rhour_e" value="$rhour_e">
<input type="hidden" name="rmin_e" value="$rmin_e">
<input class="button" type="submit" value="予約を取り消す">
</form>
<p><a class="button" href="javascript:;" onclick="window.close();">戻る</a></p>
END
		&VIEW_FOOTER();
		exit;
	}
	open(FH, "> $file_pass") or ERROR("$file_passへの書き込みに失敗しました。");
	my $data;
	for (my $i = 0; $i < $num_reserved; $i++){
		for (my $j = 0; $j < 11; $j++){
			if ($j < 10){
				$data .= "$reserved[$i][$j]/";
			}else{
				$data .= "$reserved[$i][$j]\n";
			}
		}
	}
	$data = jcode($data)->euc;
	print FH $data;
	close(FH);
	print <<END;
<h2>予約を取り消しました。</h2>
<p><a class="button" href="javascript:;" onclick="window.opener.location.reload();window.close();">閉じる</a></p>
END
}

sub CHECK_BUKAI{
	local ($name) = @_;
	my @lists_of_bukai;
	@lists_of_bukai = &GET_LISTS_OF_BUKAI("0");
	foreach (@lists_of_bukai){
		if ($_ eq $name){
			return 1;
		}
	}
	return 0;
}

sub GET_DATA_OF_A_BUKAI{
	local ($name, $mode) = @_;
	my $file_pass = './data/bukai.dat';
	open(FH, "$file_pass") or ERROR("$file_passが見つかりません。");
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		@sdata = split(/\#\#/,$data);
		if ($sdata[0] eq $name){
			close(FH);
			return $sdata[$mode];
		}
	}
	close(FH);
	return 0;
}

sub GET_LISTS_OF_BUKAI{
	local ($mode) = @_;
	my $file_pass = './data/bukai.dat';
	my @return;
	open(FH, "$file_pass") or ERROR("$file_passが見つかりません。");
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		@sdata = split(/\#\#/,$data);
		push(@return, $sdata[$mode]);
	}
	close(FH);
	return @return;
}

sub VIEW_JOIN{
	print <<END;
<h2>参加</h2>
<h3>$rname部会\n$ryear年$rmon月$rdate日$rhour_b時$rmin_b分〜$rhour_e時$rmin_e分 ＠$rplace</h3>
<ul>
<li>あなたが上記の部会に参加を希望していることを幹事に伝えることができます。</li>
<li>以下に<b>あなた</b>の情報を入力して、「参加」を選択してください。</li>
<li>入力された情報は、すべて幹事に伝えられます。</li>
</ul>
<form method = "POST">
<table>
<tr><th>名前</th><td><input type = "text" name = "ifrom" value = ""></td></tr>
<tr><th>期</th><td><input type = "text" name = "iki" value = ""></td></tr>
<tr><th>メールアドレス</th><td><input type = "text" name = "imail" value = ""></td></tr>
</table>
<input type="hidden" name="mode" value="send">
<input type="hidden" name="rname" value="$rname">
<input type="hidden" name="rplace" value="$rplace">
<input type="hidden" name="ryear" value="$ryear">
<input type="hidden" name="rmon" value="$rmon">
<input type="hidden" name="rdate" value="$rdate">
<input type="hidden" name="rhour_b" value="$rhour_b">
<input type="hidden" name="rmin_b" value="$rmin_b">
<input type="hidden" name="rhour_e" value="$rhour_e">
<input type="hidden" name="rmin_e" value="$rmin_e">
<input class="button" type="submit" value="参加">
</form>
<p><a class="button" href="javascript:;" onclick="window.close();">戻る</a></p>
END
}

sub SEND_MAIL{
	unless ($ifrom){
		&ERROR("名前が入力されていません。");
	}
	unless ($iki){
		&ERROR("期が入力されていません。");
	}
	unless ($imail =~ /^([a-zA-Z0-9])+([a-zA-Z0-9\._-])*@([a-zA-Z0-9_-])+([a-zA-Z0-9\._-]+)+$/){
		&ERROR("メールアドレスが不正です。");
	}
	my $sendmail;
	my $from;
	my $to;
	my $mails;
	$sendmail = '/usr/lib/sendmail';
	$mails = &GET_DATA_OF_A_BUKAI($rname, 3);
	unless ($mails){
		&ERROR("指定された部会が見つからないか、幹事のメールアドレスが登録されていません。");
	}
	my @to_s = split(/\,/, $mails);
	for (my $i = 0; $i < $#to_s + 1;$i++){
		unless($to_s[$i]){
			next;
		}
		$to .= $to_s[$i];
		unless($i == $#to_s){
			$to .= ",";
		}
	}
	$from = 'info@utbenron.com';
	$subject = "$ifromさんが、あなたの部会への参加を希望しています。";
	&Jcode::convert(\$subject,'jis');
	$subject = jcode($subject)->mime_encode;
	$mail_body = "$ifromさんが、あなたの部会への参加を希望しています。\n\n";
	$mail_body .= "（１）部会\n$rname部会\n$ryear年$rmon月$rdate日$rhour_b時$rmin_b分〜$rhour_e時$rmin_e分 ＠$rplace\n\n";
	$mail_body .= "（２）名前\n$ifrom\n\n";
	$mail_body .= "（３）期\n$iki\n\n";
	$mail_body .= "（４）メールアドレス\n$imail\n\n";
	$mail_body .= "※注意\n参加希望者に返信する場合、このメールに直接返信せず、参加希望者のメールアドレス<$imail>に返信してください。\n\n部会ナビ";
	&Jcode::convert(\$mail_body,'jis');
	open(MAIL,"| $sendmail -t");
	print MAIL "To: \n";
	print MAIL "Bcc: $to\n";
	print MAIL "From: $from\n";
	print MAIL "Subject: $subject\n";
	print MAIL "\n";
	print MAIL "$mail_body\n";
	close(MAIL);
	print <<END;
<h2>参加</h2>
<p>幹事宛に参加希望メールを送信しました。</p>
<p><a class="button" href="javascript:;" onclick="window.close();">閉じる</a></p>
END
}

sub VIEW_DETAIL{
	my $kanji;
	my $names;
	my $kis;
	my $intro;
	$names = &GET_DATA_OF_A_BUKAI($rname, 1);
	my @name_s = split(/\,/, $names);
	$kis = &GET_DATA_OF_A_BUKAI($rname, 2);
	my @ki_s = split(/\,/, $kis);
	for (my $i = 0; $i < $#name_s + 1; $i++){
		$kanji .= "$name_s[$i]（$ki_s[$i]期）";
		unless ($i == $#name_s){
			$kanji .= " ";
		}
	}
	$intro = &GET_DATA_OF_A_BUKAI($rname, 4);
	print <<END;
<h2>$rname部会</h2>
<ul>
<li>幹事：$kanji</li>
<li>紹介文：<br>$intro</li>
</ul>
<p><a class="button" href="javascript:;" onclick="window.close();">閉じる</a></p>
END

}

sub VIEW_ADMIN_MAIN{
	print <<END;
<h2>部会一覧</h2>
<form name="form1" method="POST" target="_blank">
<input type="hidden" name="type" value="">
<input type="hidden" name="pass" value="$pass">
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="aname" value="">
END
	my $file_pass = './data/bukai.dat';
	open(FH, "$file_pass") or ERROR("$file_passが見つかりません。");
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		@sdata = split(/\#\#/,$data);
		my $kanji;
		my @name_s = split(/\,/, $sdata[1]);
		my @ki_s = split(/\,/, $sdata[2]);
		my @mail_s = split(/\,/, $sdata[3]);
		for (my $i = 0; $i < $#name_s + 1; $i++){
			$kanji .= "<li>$name_s[$i]（$ki_s[$i]期）<br>$mail_s[$i]</li>";
		}
		print <<END;
<h5>$sdata[0]部会<br>
<font size="-1">
[<a onClick="document.form1.method='POST';document.form1.target='_blank';document.form1.type.value='del';document.form1.aname.value='$sdata[0]';document.form1.submit();">削除</a> |
<a onClick="document.form1.method='POST';document.form1.target='_blank';document.form1.type.value='sort0';document.form1.aname.value='$sdata[0]';document.form1.submit();">↑</a> |
<a onClick="document.form1.method='POST';document.form1.target='_blank';document.form1.type.value='sort1';document.form1.aname.value='$sdata[0]';document.form1.submit();">↓</a>]
</font>
</h5>
<div class="whitebox">
<ul>$kanji</ul><p>$sdata[4]</p>
</div>
END
	}
	close(FH);
	print <<END;
</form>
<h3>追加</h3>
<p>複数の幹事が置かれている場合、「＋」で欄を追加してください（「−」で削除できます）。</p>
<div class="scroll">
<form method = "POST" target="_blank">
<table id ="wrapper">
<tr><th>名称</th><td><input type="text" name="aname" value="">部会</td></tr>
<tr><th>紹介文</th><td><textarea name="aintro" rows="10" cols="40"></textarea></td></tr>
<tr><th>幹事<br><input type="button" value="＋" onClick="ItemField.add();" /><input type="button" value="−" onClick="ItemField.remove();" /></th>
<td><table><tr><td>氏名</td><td><input type="text" name="akanji0"></td></tr><tr><td>期</td><td><input type="text" name="aki0">期</td></tr><tr><td>メールアドレス</td><td><input type="text" name="amail0"></td></tr></table></td></tr>
<tr id="item1"></tr>
<script type="text/javascript">
ItemField.currentNumber = 0;
ItemField.itemTemplate
    = '<th>幹事<br></th><td><table><tr><td>氏名</td><td><input type="text" name="akanji__count__"></td></tr><tr><td>期</td><td><input type="text" name="aki__count__">期</td></tr><tr><td>メールアドレス</td><td><input type="text" name="amail__count__"></td></tr></table></td>';
</script>
</table>
<input type="hidden" name="pass" value="$pass">
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="type" value="add">
<input class="button" type="submit" value="追加">
</form>
</div>
END

}

sub SORT_BUKAI{
	my $file_pass = './data/bukai.dat';
	open(FH, "$file_pass") or ERROR("$file_passが見つかりません。");
	my $new;
	my $before;
	my $before_all;
	my $target;
	my $flg;
	my $after_all;
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		@sdata = split(/\#\#/,$data);
		if (!$target){
			if ($sdata[0] eq $aname){
				if ($type eq 'sort0'){
					$target = $data;
					if ($before){
						$after_all .= "$before\n";
					}
				}else{
					$target = $data;
				}
			}else{
				if ($type eq 'sort0'){
					if ($before){
						$before_all .= "$before\n";
					}
					$before = $data;
				}else{
					$before_all .= "$data\n";
				}
			}
		}else{
			if ($type eq 'sort0'){
				$after_all .= "$data\n";
			}else{
				if ($flg){
					$after_all .= "$data\n";
				}else{
					$before_all .= "$data\n";
					$flg = 1;					
				}
			}
		}
	}
	close(FH);
	unless ($target){
		&ERROR("該当する部会が見つかりませんでした。");
	}
	$new = "$before_all$target\n$after_all";
	open(FH, "> $file_pass") or ERROR("$file_passへの書き込みに失敗しました。");
	$new = jcode($new)->euc;
	print FH $new;
	close(FH);
	print <<END;
<script type="text/javascript">
window.opener.location.reload();window.close();
</script>
END
}

sub DEL_BUKAI{
	my $file_pass = './data/bukai.dat';
	open(FH, "$file_pass") or ERROR("$file_passが見つかりません。");
	my $new;
	my $flg;
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		@sdata = split(/\#\#/,$data);
		if (!$flg && $sdata[0] eq $aname){
			$flg = 1;
			next;
		}else{
			$new .= "$data\n";
		}
	}
	close(FH);
	unless ($flg){
		&ERROR("該当する部会が見つかりませんでした。");
	}
	open(FH, "> $file_pass") or ERROR("$file_passへの書き込みに失敗しました。");
	$new = jcode($new)->euc;
	print FH $new;
	close(FH);
	print <<END;
<h2>部会一覧からの削除</h2>
<p>削除しました。</p>
<p><a class="button" href="javascript:;" onclick="window.opener.location.reload();window.close();">閉じる</a></p>
END
}

sub ADD_BUKAI{
	$aname =~ s/\#\#/＃＃/igo;
	my $kanji;
	my $ki;
	my $mail;
	unless ($aname){
		&ERROR("名称が入力されていません。");
	}
	unless ($num_akanji){
		&ERROR("幹事の氏名が１件も入力されていません。");
	}
	for (my $i = 0; $i < $num_akanji; $i++){
		$akanji[$i] =~ s/\#\#/＃＃/igo;
		$aki[$i] =~ s/\#\#/＃＃/igo;
		$amail[$i] =~ s/\#\#/＃＃/igo;
		$akanji[$i] =~ s/\,/，/igo;
		$aki[$i] =~ s/\,/，/igo;
		$amail[$i] =~ s/\,/，/igo;
		$kanji .= $akanji[$i];
		$ki .= $aki[$i];
		$mail .= $amail[$i];
		unless ($i == $num_akanji - 1){
			$kanji .= ",";
			$ki .= ",";
			$mail .= ",";
		}
	}
	$aintro =~ s/\</＜/igo;
	$aintro =~ s/\>/＞/igo;
	$aintro =~ s/\#\#/＃＃/igo;
	$aintro =~ s/\r\n/<br>/igo;
	$aintro =~ s/\r/<br>/igo;
	$aintro =~ s/\n/<br>/igo;
	my $file_pass = './data/bukai.dat';
	open(FH, ">> $file_pass") or ERROR("$file_passへの書き込みに失敗しました。");
	my $data = "$aname##$kanji##$ki##$mail##$aintro\n";
	$data = jcode($data)->euc;
	print FH $data;
	close(FH);
	print <<END;
<h2>部会一覧への追加</h2>
<p>以下の部会を部会一覧に追加しました。</p>
<table>
<tr><th>名称</th><td>$aname</td></tr>
END
	for (my $i = 0; $i < $num_akanji; $i++){
		print "<tr><th>幹事</th><td>$akanji[$i]（$aki[$i]期）$amail[$i]</td></tr>";
	}
	print <<END;
<tr><th>紹介文</th><td>$aintro</td></tr>
</table>
<p><a class="button" href="javascript:;" onclick="window.opener.location.reload();window.close();">閉じる</a></p>
END
}

sub VIEW_ADMIN{
	unless ($pass eq 'utbenron'){
		print <<END;
<h2>管理用パスワードを入力してください</h2>
<form method="POST">
<input type="password" name="pass" value="">
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="aname" value="$aname">
<input type="hidden" name="aki" value="$aki">
<input type="hidden" name="amail" value="$amail">
<input type="hidden" name="aintro" value="$aintro">
<input class="button" type="submit" value="ログイン">
</form>
END
		&VIEW_FOOTER();
		exit;
	}
	if ($type eq 'add'){
		&ADD_BUKAI();
	}elsif ($type eq 'del'){
		&DEL_BUKAI();
	}elsif ($type =~ /^sort\d$/){
		&SORT_BUKAI();
	}else{
		&VIEW_ADMIN_MAIN();
	}
}

# エラー処理
sub ERROR{
	local ($text) = @_;
	print "<h2>エラー</h2>";
	print "<ul><li>$text</li></ul>";
	print "<p><a class=\"button\" href=\"javascript:;\" onclick=\"window.close();\">閉じる</a></p>";
	&VIEW_FOOTER();
	exit;
}