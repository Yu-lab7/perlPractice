#!/usr/local/bin/perl
use CGI;

$q = new CGI;
$body = $q->param('body');

printHTML($body);

sub printHTML {
    my ($body) = @_;
    my $msg = (defined($ENV{'CONTENT_LENGTH'}) && $body eq '') ? '<span style="color:red;">入力がありません</span>' : $body;

    print << "EOF";
Content-type: text/html

<html>
<head>
<title>フォーム練習</title>
<meta http-equiv="Content-type" content="text/html; charset=UTF-8">
</head>
<body>
<h1>フォーム練習1</h1>

<form method="post" action="form4.cgi">
    メッセージ本文<br>
    <textarea name="body" cols="80" rows="5"></textarea>
    <br><br>
    入力内容が正しければ「OK」ボタンをクリックしてください
    <input type="submit" value="OK">
</form>

<hr>
$msg
</body>
</html>
EOF
}