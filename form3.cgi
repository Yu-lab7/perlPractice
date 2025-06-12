#!/usr/local/bin/perl
use CGI;

$q = new CGI;
$body = $q->param('body'); #行 (a)

printHTML($body);

sub printHTML {
    my ($body) = @_;
    my $msg = ($body eq '') ? '<span style="color:red;">入力がありません</span>' : $body;
    print << "EOF";
Content-type: text/html

<html>
<head>
<title>フォーム練習</title>
<meta http-equiv="Content-type" content="text/html; charset=UTF-8">
</head>
<body>
<h1>フォーム練習1</h1>

<form method="post" action="form3.cgi"> <!-- 行 (b) -->
    メッセージ本文<br>
    <textarea name="body" cols="80" rows="5"></textarea> <!-- 行(c) -->
    <br><br>
    入力内容が正しければ「OK」ボタンをクリックしてください
    <input type="submit" value="OK"> <!-- 行(d) -->
</form>

<hr>
$msg
</body>
</html>
EOF
}