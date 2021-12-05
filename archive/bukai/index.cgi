#!/usr/bin/perl

# �⥸�塼��
use Jcode;
use Time::Local;
use CGI qw(:standard);

# ���մ�Ϣ�����Х��ѿ�
$time = time;
($sec, $min, $hour, $date, $mon, $year, $wday) = localtime($time);
$year += 1900;
$mon++;

# �ѥ�᡼������
$mode = param('mode');
$type = param('type');
$pass = param('pass');
## ���������θ�����
$cyear = param('cyear');
unless($cyear){
	$cyear = $year;
}
$cmon = param('cmon');
unless($cmon){
	$cmon = $mon;
}
$cdate = param('cdate');
## ͽ���Ϣ����������ץ��ӽ�������Ȥ�ä��ۤ����ɤ�
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

# �⡼�ɽ����ʥᥤ���
if ($mode eq 'reserve'){
	&VIEW_HEADER('ͽ��');
	&RESERVE();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'cancel'){
	&VIEW_HEADER('ͽ����');
	&CANCEL();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'comment'){
	&VIEW_HEADER('������');
	&VIEW_COMMENT();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'lists'){
	&VIEW_HEADER('�������');
	&VIEW_LISTS_OF_BUKAI();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'detail'){
	&VIEW_HEADER('����Ҳ�');
	&VIEW_DETAIL();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'join'){
	&VIEW_HEADER('���ô�˾');
	&VIEW_JOIN();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'send'){
	&VIEW_HEADER('���ô�˾');
	&SEND_MAIL();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'admin'){
	&VIEW_HEADER('����');
	&VIEW_ADMIN();
	&VIEW_FOOTER();
	exit;
}elsif ($mode eq 'view_reserve'){
	&VIEW_HEADER('ͽ��');
	&VIEW_RESERVE();
	&VIEW_FOOTER();
	exit;
}else{
	&VIEW_HEADER('����ʥ�');
	&VIEW_MAIN();
	&VIEW_FOOTER();
	exit;
}

# �إå���ɽ��
sub VIEW_HEADER(){
	local($title) = @_;
	print "Content-type: text/html\n\n";
	print <<END;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=euc-jp" />
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="style.css" rel="stylesheet" type="text/css">
<title>$title - �������ع���������������</title>
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
<div id="top">����NAVI</div>
<div id="main">
<div id="content">
END
}

# �եå���ɽ��
sub VIEW_FOOTER(){
	print <<END;
</div>
<div id="footer">
<p><a href=\"?mode=admin\">�����ڡ���</a></p>
<p>Copyright(C)2016 �������ع���������������. All rights reserved.</p>
</div>
</div>
</body>
</html>
END
}

# �ᥤ��ڡ���ɽ��
sub VIEW_MAIN(){
	print <<END;
<div id="header">
<ul>
<li><a href="?mode=" class="open">ͽ�����</a></li>
<li><a href="?mode=lists">�������</a></li>
</ul>
</div>
END
	my $file_pass = './data/reserve.dat';
	open(FH, "$file_pass") or ERROR("$file_pass�����Ĥ���ޤ���");
	my $num_reserved = 0;
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		@sdata = split(/\//,$data);
		for (my $i = 0; $i <= $#sdata; $i++){
			$reserved[$num_reserved][$i] = $sdata[$i];
		}
		if ($cyear == $reserved[$num_reserved][2] && $cmon == $reserved[$num_reserved][3]){
			if ($reserved[$num_reserved][1] eq '�������'){
				$komaba[$reserved[$num_reserved][4]][$num_komaba[$reserved[$num_reserved][4]]] = $num_reserved;
				$num_komaba[$reserved[$num_reserved][4]]++;
			}
			elsif ($reserved[$num_reserved][1] eq '�ܶ�����'){
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
<p style="text-align:center;"><a href="?cyear=$byear&cmon=$bmon">&lt;&lt;</a> $cyearǯ$cmon�� <a href="?cyear=$ayear&cmon=$amon">&gt;&gt;</a></p>
END
	@days = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
	if ($cmon == 2 and ($cyear % 4 == 0 and $cyear % 100 != 0 or $cyear % 400 == 0)) {
		$days[1]++; # ���뤦ǯ
	}
	$enddate = $days[$cmon - 1]; # �������
	@wdays = ("��","��","��","��","��","��","��");
	for ($i = 1 ; $i <= $enddate ; $i++) {
		$cwday = (localtime( timelocal(0, 0, 0, $i, $cmon - 1, $cyear)))[6];
		if ($cyear < $year || ($cyear == $year && $cmon < $mon) || ($cyear == $year && $cmon == $mon && $i < $date)){
			next;
		}
		print "<h3>$cmon��$i����$wdays[$cwday]��</h3>";
		print "<div class=\"bukai\">";
		print "<h4>�������</h4>";
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
			print "<p class=\"time\"><span class=\"time1\">$aaa[$j][5]:$min_b</span><span class=\"time2\">��$aaa[$j][7]:$min_e</span></p>";
			print "<p class=\"name\"><a href=\"$detail_url\" target=\"_blank\">$aaa[$j][0]����</a></p>";
			print "<p class=\"links\">";
			if ($comment_url){
				print "<a href=\"$comment_url\" target=\"_blank\">�ܺ�</a>&nbsp;|&nbsp;";
			}
			print "<a href=\"$join_url\" target=\"_blank\">����</a>&nbsp;|&nbsp;<a href=\"$cancel_url\" target=\"_blank\">���</a>";
			print "</p>";
			print "</li>";
		}
		unless ($num_komaba[$i]){
			print "</ul><ul class=\"no_reserve\"><li>";
			print "<p class=\"name\"><a href=\"#\">ͽ��ʤ�</a></p>";
			print "<p class=\"links\"><a href=\"?mode=view_reserve&cyear=$cyear&cmon=$cmon&cdate=$i\" target=\"_blank\">������ͽ��</a></p>";
			print "</li>";
		}
		print "</ul>";
		print "</div><div style=\"clear:both\"></div>";
		print "<div class=\"bukai\">";
		print "<h4>�ܶ�����</h4>";
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
			print "<p class=\"time\"><span class=\"time1\">$aaa[$j][5]:$min_b</span><span class=\"time2\">��$aaa[$j][7]:$min_e</span></p>";
			print "<p class=\"name\"><a href=\"$detail_url\" target=\"_blank\">$aaa[$j][0]����</a></p>";
			print "<p class=\"links\">";
			if ($comment_url){
				print "<a href=\"$comment_url\" target=\"_blank\">�ܺ�</a>&nbsp;|&nbsp;";
			}
			print "<a href=\"$join_url\" target=\"_blank\">����</a>&nbsp;|&nbsp;<a href=\"$cancel_url\" target=\"_blank\">���</a>";
			print "</p>";
			print "</li>";
		}
		unless ($num_hongo[$i]){
			print "</ul><ul class=\"no_reserve\"><li>";
			print "<p class=\"name\"><a href=\"#\">ͽ��ʤ�</a></p>";
			print "<p class=\"links\"><a href=\"?mode=view_reserve&cyear=$cyear&cmon=$cmon&cdate=$i\" target=\"_blank\">������ͽ��</a></p>";
			print "</li>";
		}
		print "</ul>";
		print "</div><div style=\"clear:both\"></div>";
		print "<a class=\"button\" href=\"?mode=view_reserve&cyear=$cyear&cmon=$cmon&cdate=$i\" target=\"_blank\">ͽ��</a>";
	}
	print <<END;
END
}

# �������ɽ��
sub VIEW_LISTS_OF_BUKAI{
	print <<END;
<div id="header">
<ul>
<li><a href="?mode=">ͽ�����</a></li>
<li><a href="?mode=lists" class="open">�������</a></li>
</ul>
</div>
END
	my $file_pass = './data/bukai.dat';
	open(FH, "$file_pass") or ERROR("$file_pass�����Ĥ���ޤ���");
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		@sdata = split(/\#\#/,$data);
		my $kanji;
		my @name_s = split(/\,/, $sdata[1]);
		my @ki_s = split(/\,/, $sdata[2]);
		my @mail_s = split(/\,/, $sdata[3]);
		for (my $i = 0; $i < $#name_s + 1; $i++){
			$kanji .= "<li>$name_s[$i]��$ki_s[$i]����</li>";
		}
		print "<h5>$sdata[0]����</h5><div class=\"whitebox\"><p><ul>$kanji</ul></p><p>$sdata[4]</p></div>";
	}
	close(FH);
	print <<END;
END
}

# ͽ��ե�����ɽ��
sub VIEW_RESERVE(){
	print <<END;
<h2>$cyearǯ$cmon��$cdate�� ͽ��</h2>
<form method = "POST">
<table>
<tr><th>����̾</th><td><input type = "text" name = "rname" value = "">����</td></tr>
<tr><th>���</th><td><select name = "rplace">
<option value="�������" selected>�������</option>
<option value="�ܶ�����">�ܶ�����</option>
</select>
</td></tr>
END
print "<tr><th>����</th><td>";
print "<select name = \"rhour_b\">";
for (my $i = 8; $i <= 21; $i++){
	print "<option value=\"$i\">$i</option>";
}
print "</select>��";
print "<select name = \"rmin_b\">";
for (my $i = 0; $i <= 59; $i++){
	print "<option value=\"$i\">$i</option>";
}
print "</select>ʬ��";
print "<select name = \"rhour_e\">";
for (my $i = 8; $i <= 21; $i++){
	print "<option value=\"$i\"";
	if ($i == 9){
		print " selected";
	}
	print ">$i</option>";
}
print "</select>��";
print "<select name = \"rmin_e\">";
for (my $i = 0; $i <= 59; $i++){
	print "<option value=\"$i\">$i</option>";
}
print "</select>ʬ";
print "</td></tr>";
	print <<END;
<tr><th>����ѥѥ�</th><td><input type="password" name="rpass" value=""><br>�� Ⱦ�ѿ���4ʸ��</td></tr>
<tr><th>������</th><td><textarea name="rcomment" rows="10" cols="20"></textarea></td></tr>
</table>
<p><input class="button" type = "submit" value = "ͽ��"></p>
<input type = "hidden" name = "ryear" value = "$cyear">
<input type = "hidden" name = "rmon" value = "$cmon">
<input type = "hidden" name = "rdate" value = "$cdate">
<input type = "hidden" name = "mode" value = "reserve">
</form>
<p><a class="button" href="javascript:;" onclick="window.close();">���</a></p>
END
}

# ������ɽ��
sub VIEW_COMMENT(){
	my $file_pass = './data/reserve.dat';
	open(FH, "$file_pass") or ERROR("$file_pass�����Ĥ���ޤ���");
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
		print "<h2>$target[0]����</h2>";
		print "<h3>$target[2]ǯ$target[3]��$target[4]��$target[5]��$target[6]ʬ��$target[7]��$target[8]ʬ ��$target[1]</h3>";
		print "$target[10]";
	}else{
		print "�����ȤϤ���ޤ���";
	}
	print "<p><a class=\"button\" href=\"javascript:;\" onclick=\"window.close();\">�Ĥ���</a></p>";
}

# ͽ���Ϣ����
sub RESERVE(){
	unless (&CHECK_BUKAI($rname)){
		&ERROR("<i>$rname����</i>�ϡ������������Ͽ���줿����ǤϤ���ޤ���");
	}
	if (($rhour_b * 60 + $rmin_b) >= ($rhour_e * 60 + $rmin_e)){
		&ERROR("ͽ����֤������Ǥ���");
	}
	unless ($rpass =~ /^\d{4}$/){
		&ERROR("�ѥ���ɤ�Ⱦ�ѿ���4ʸ���Ǥ���");
	}
	if ($ryear < $year || ($ryear == $year && $rmon < $mon) || ($ryear == $year && $rmon == $mon && $rdate <= $date)){
		&ERROR("�����ʹߤ�ͽ�󤷤��Ǥ��ޤ���");
	}
	$rname =~ s/\</��/igo;
	$rname =~ s/\>/��/igo;
	$rname =~ s/\//��/igo;
	$rname =~ s/\n//igo;
	$rname =~ s/\r//igo;
	$rcomment =~ s/\</��/igo;
	$rcomment =~ s/\>/��/igo;
	$rcomment =~ s/\//��/igo;
	$rcomment =~ s/\r\n/<br>/igo;
	$rcomment =~ s/\r/<br>/igo;
	$rcomment =~ s/\n/<br>/igo;
	my $file_pass = './data/reserve.dat';
	open(FH, "$file_pass") or ERROR("$file_pass�����Ĥ���ޤ���");
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
				&ERROR("ͽ����֤���ʣ���Ƥ��ޤ���");
			}
		}
	}
	open(FH, ">> $file_pass") or ERROR("$file_pass�ؤν񤭹��ߤ˼��Ԥ��ޤ�����");
	my $data = "$rname/$rplace/$ryear/$rmon/$rdate/$rhour_b/$rmin_b/$rhour_e/$rmin_e/$rpass/$rcomment\n";
	$data = jcode($data)->euc;
	print FH $data;
	close(FH);
	print <<END;
<h2>ͽ�󤬴�λ���ޤ�����</h2>
<table>
<tr><th>̾��</th><td>$rname</td></tr>
<tr><th>���</th><td>$rplace</td></tr>
<tr><th>����</th><td>$ryearǯ$rmon��$rdate��$rhour_b��$rmin_bʬ��$rhour_e��$rmin_eʬ</td></tr>
<tr><th>������</th><td>$rcomment</td></tr>
</table>
<p><a class="button" href="javascript:;" onclick="window.opener.location.reload();window.close();">�Ĥ���</a></p>
END
}

# ��ý���
sub CANCEL(){
	my $file_pass = './data/reserve.dat';
	open(FH, "$file_pass") or ERROR("$file_pass�����Ĥ���ޤ���");
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
		&ERROR("�����ͽ�󤬸��Ĥ���ޤ���Ǥ�����");
	}
	unless ($pass eq $c_pass){
		print <<END;
<h2>����ѥѥ���ɤ����Ϥ��Ƥ�������</h2>
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
<input class="button" type="submit" value="ͽ�����ä�">
</form>
<p><a class="button" href="javascript:;" onclick="window.close();">���</a></p>
END
		&VIEW_FOOTER();
		exit;
	}
	open(FH, "> $file_pass") or ERROR("$file_pass�ؤν񤭹��ߤ˼��Ԥ��ޤ�����");
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
<h2>ͽ�����ä��ޤ�����</h2>
<p><a class="button" href="javascript:;" onclick="window.opener.location.reload();window.close();">�Ĥ���</a></p>
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
	open(FH, "$file_pass") or ERROR("$file_pass�����Ĥ���ޤ���");
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
	open(FH, "$file_pass") or ERROR("$file_pass�����Ĥ���ޤ���");
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
<h2>����</h2>
<h3>$rname����\n$ryearǯ$rmon��$rdate��$rhour_b��$rmin_bʬ��$rhour_e��$rmin_eʬ ��$rplace</h3>
<ul>
<li>���ʤ����嵭������˻��ä��˾���Ƥ��뤳�Ȥ򴴻��������뤳�Ȥ��Ǥ��ޤ���</li>
<li>�ʲ���<b>���ʤ�</b>�ξ�������Ϥ��ơ��ֻ��áפ����򤷤Ƥ���������</li>
<li>���Ϥ��줿����ϡ����٤ƴ������������ޤ���</li>
</ul>
<form method = "POST">
<table>
<tr><th>̾��</th><td><input type = "text" name = "ifrom" value = ""></td></tr>
<tr><th>��</th><td><input type = "text" name = "iki" value = ""></td></tr>
<tr><th>�᡼�륢�ɥ쥹</th><td><input type = "text" name = "imail" value = ""></td></tr>
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
<input class="button" type="submit" value="����">
</form>
<p><a class="button" href="javascript:;" onclick="window.close();">���</a></p>
END
}

sub SEND_MAIL{
	unless ($ifrom){
		&ERROR("̾�������Ϥ���Ƥ��ޤ���");
	}
	unless ($iki){
		&ERROR("�������Ϥ���Ƥ��ޤ���");
	}
	unless ($imail =~ /^([a-zA-Z0-9])+([a-zA-Z0-9\._-])*@([a-zA-Z0-9_-])+([a-zA-Z0-9\._-]+)+$/){
		&ERROR("�᡼�륢�ɥ쥹�������Ǥ���");
	}
	my $sendmail;
	my $from;
	my $to;
	my $mails;
	$sendmail = '/usr/lib/sendmail';
	$mails = &GET_DATA_OF_A_BUKAI($rname, 3);
	unless ($mails){
		&ERROR("���ꤵ�줿���񤬸��Ĥ���ʤ����������Υ᡼�륢�ɥ쥹����Ͽ����Ƥ��ޤ���");
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
	$subject = "$ifrom���󤬡����ʤ�������ؤλ��ä��˾���Ƥ��ޤ���";
	&Jcode::convert(\$subject,'jis');
	$subject = jcode($subject)->mime_encode;
	$mail_body = "$ifrom���󤬡����ʤ�������ؤλ��ä��˾���Ƥ��ޤ���\n\n";
	$mail_body .= "�ʣ�������\n$rname����\n$ryearǯ$rmon��$rdate��$rhour_b��$rmin_bʬ��$rhour_e��$rmin_eʬ ��$rplace\n\n";
	$mail_body .= "�ʣ���̾��\n$ifrom\n\n";
	$mail_body .= "�ʣ��˴�\n$iki\n\n";
	$mail_body .= "�ʣ��˥᡼�륢�ɥ쥹\n$imail\n\n";
	$mail_body .= "�����\n���ô�˾�Ԥ��ֿ������硢���Υ᡼���ľ���ֿ����������ô�˾�ԤΥ᡼�륢�ɥ쥹<$imail>���ֿ����Ƥ���������\n\n����ʥ�";
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
<h2>����</h2>
<p>�������˻��ô�˾�᡼����������ޤ�����</p>
<p><a class="button" href="javascript:;" onclick="window.close();">�Ĥ���</a></p>
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
		$kanji .= "$name_s[$i]��$ki_s[$i]����";
		unless ($i == $#name_s){
			$kanji .= " ";
		}
	}
	$intro = &GET_DATA_OF_A_BUKAI($rname, 4);
	print <<END;
<h2>$rname����</h2>
<ul>
<li>������$kanji</li>
<li>�Ҳ�ʸ��<br>$intro</li>
</ul>
<p><a class="button" href="javascript:;" onclick="window.close();">�Ĥ���</a></p>
END

}

sub VIEW_ADMIN_MAIN{
	print <<END;
<h2>�������</h2>
<form name="form1" method="POST" target="_blank">
<input type="hidden" name="type" value="">
<input type="hidden" name="pass" value="$pass">
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="aname" value="">
END
	my $file_pass = './data/bukai.dat';
	open(FH, "$file_pass") or ERROR("$file_pass�����Ĥ���ޤ���");
	while ($data = <FH>) {
		$data = jcode($data)->euc;
		chomp $data;
		@sdata = split(/\#\#/,$data);
		my $kanji;
		my @name_s = split(/\,/, $sdata[1]);
		my @ki_s = split(/\,/, $sdata[2]);
		my @mail_s = split(/\,/, $sdata[3]);
		for (my $i = 0; $i < $#name_s + 1; $i++){
			$kanji .= "<li>$name_s[$i]��$ki_s[$i]����<br>$mail_s[$i]</li>";
		}
		print <<END;
<h5>$sdata[0]����<br>
<font size="-1">
[<a onClick="document.form1.method='POST';document.form1.target='_blank';document.form1.type.value='del';document.form1.aname.value='$sdata[0]';document.form1.submit();">���</a> |
<a onClick="document.form1.method='POST';document.form1.target='_blank';document.form1.type.value='sort0';document.form1.aname.value='$sdata[0]';document.form1.submit();">��</a> |
<a onClick="document.form1.method='POST';document.form1.target='_blank';document.form1.type.value='sort1';document.form1.aname.value='$sdata[0]';document.form1.submit();">��</a>]
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
<h3>�ɲ�</h3>
<p>ʣ���δ������֤���Ƥ����硢�֡ܡפ�����ɲä��Ƥ��������ʡ֡ݡפǺ���Ǥ��ޤ��ˡ�</p>
<div class="scroll">
<form method = "POST" target="_blank">
<table id ="wrapper">
<tr><th>̾��</th><td><input type="text" name="aname" value="">����</td></tr>
<tr><th>�Ҳ�ʸ</th><td><textarea name="aintro" rows="10" cols="40"></textarea></td></tr>
<tr><th>����<br><input type="button" value="��" onClick="ItemField.add();" /><input type="button" value="��" onClick="ItemField.remove();" /></th>
<td><table><tr><td>��̾</td><td><input type="text" name="akanji0"></td></tr><tr><td>��</td><td><input type="text" name="aki0">��</td></tr><tr><td>�᡼�륢�ɥ쥹</td><td><input type="text" name="amail0"></td></tr></table></td></tr>
<tr id="item1"></tr>
<script type="text/javascript">
ItemField.currentNumber = 0;
ItemField.itemTemplate
    = '<th>����<br></th><td><table><tr><td>��̾</td><td><input type="text" name="akanji__count__"></td></tr><tr><td>��</td><td><input type="text" name="aki__count__">��</td></tr><tr><td>�᡼�륢�ɥ쥹</td><td><input type="text" name="amail__count__"></td></tr></table></td>';
</script>
</table>
<input type="hidden" name="pass" value="$pass">
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="type" value="add">
<input class="button" type="submit" value="�ɲ�">
</form>
</div>
END

}

sub SORT_BUKAI{
	my $file_pass = './data/bukai.dat';
	open(FH, "$file_pass") or ERROR("$file_pass�����Ĥ���ޤ���");
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
		&ERROR("�����������񤬸��Ĥ���ޤ���Ǥ�����");
	}
	$new = "$before_all$target\n$after_all";
	open(FH, "> $file_pass") or ERROR("$file_pass�ؤν񤭹��ߤ˼��Ԥ��ޤ�����");
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
	open(FH, "$file_pass") or ERROR("$file_pass�����Ĥ���ޤ���");
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
		&ERROR("�����������񤬸��Ĥ���ޤ���Ǥ�����");
	}
	open(FH, "> $file_pass") or ERROR("$file_pass�ؤν񤭹��ߤ˼��Ԥ��ޤ�����");
	$new = jcode($new)->euc;
	print FH $new;
	close(FH);
	print <<END;
<h2>�����������κ��</h2>
<p>������ޤ�����</p>
<p><a class="button" href="javascript:;" onclick="window.opener.location.reload();window.close();">�Ĥ���</a></p>
END
}

sub ADD_BUKAI{
	$aname =~ s/\#\#/����/igo;
	my $kanji;
	my $ki;
	my $mail;
	unless ($aname){
		&ERROR("̾�Τ����Ϥ���Ƥ��ޤ���");
	}
	unless ($num_akanji){
		&ERROR("�����λ�̾����������Ϥ���Ƥ��ޤ���");
	}
	for (my $i = 0; $i < $num_akanji; $i++){
		$akanji[$i] =~ s/\#\#/����/igo;
		$aki[$i] =~ s/\#\#/����/igo;
		$amail[$i] =~ s/\#\#/����/igo;
		$akanji[$i] =~ s/\,/��/igo;
		$aki[$i] =~ s/\,/��/igo;
		$amail[$i] =~ s/\,/��/igo;
		$kanji .= $akanji[$i];
		$ki .= $aki[$i];
		$mail .= $amail[$i];
		unless ($i == $num_akanji - 1){
			$kanji .= ",";
			$ki .= ",";
			$mail .= ",";
		}
	}
	$aintro =~ s/\</��/igo;
	$aintro =~ s/\>/��/igo;
	$aintro =~ s/\#\#/����/igo;
	$aintro =~ s/\r\n/<br>/igo;
	$aintro =~ s/\r/<br>/igo;
	$aintro =~ s/\n/<br>/igo;
	my $file_pass = './data/bukai.dat';
	open(FH, ">> $file_pass") or ERROR("$file_pass�ؤν񤭹��ߤ˼��Ԥ��ޤ�����");
	my $data = "$aname##$kanji##$ki##$mail##$aintro\n";
	$data = jcode($data)->euc;
	print FH $data;
	close(FH);
	print <<END;
<h2>��������ؤ��ɲ�</h2>
<p>�ʲ������������������ɲä��ޤ�����</p>
<table>
<tr><th>̾��</th><td>$aname</td></tr>
END
	for (my $i = 0; $i < $num_akanji; $i++){
		print "<tr><th>����</th><td>$akanji[$i]��$aki[$i]����$amail[$i]</td></tr>";
	}
	print <<END;
<tr><th>�Ҳ�ʸ</th><td>$aintro</td></tr>
</table>
<p><a class="button" href="javascript:;" onclick="window.opener.location.reload();window.close();">�Ĥ���</a></p>
END
}

sub VIEW_ADMIN{
	unless ($pass eq 'utbenron'){
		print <<END;
<h2>�����ѥѥ���ɤ����Ϥ��Ƥ�������</h2>
<form method="POST">
<input type="password" name="pass" value="">
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="aname" value="$aname">
<input type="hidden" name="aki" value="$aki">
<input type="hidden" name="amail" value="$amail">
<input type="hidden" name="aintro" value="$aintro">
<input class="button" type="submit" value="������">
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

# ���顼����
sub ERROR{
	local ($text) = @_;
	print "<h2>���顼</h2>";
	print "<ul><li>$text</li></ul>";
	print "<p><a class=\"button\" href=\"javascript:;\" onclick=\"window.close();\">�Ĥ���</a></p>";
	&VIEW_FOOTER();
	exit;
}