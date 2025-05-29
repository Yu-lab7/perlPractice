print "Content-Type: text/html; charset=UTF-8\n\n";
print <<'HTML';

<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>フォーム練習</title>
    </head>
    <body>
        <h1>フォーム練習</h1>
        <form method="post" action="form.cgi">
            メッセージ本文<br>
            <textarea name="body" cols="80" rows="5"></textarea>
            <br><br>
            入力内容が正しければ「OK」ボタンをクリックしてください。<br>
            <input type="submit" value="OK">
        </form>
    </body>
</html>
HTML