#!/usr/local/bin/perl

use strict;
use warnings;
use utf8;
use CGI;
use CGI::Carp qw/ fatalsToBrowser /;
use Fcntl qw(:flock); # flockのために追加

# require './init.cgi'; # init.cgiで $q を生成していると仮定
my $q = CGI->new;

my $script = $ENV{'SCRIPT_NAME'};
my $log_file = './log.txt';

# ---- メインロジック ----
# フォームが送信されたか（HTTPメソッドがPOSTか）で判断
if ($q->request_method eq 'POST') {
    # フォームが送信された場合
    my $name    = $q->param('name');
    my $subject = $q->param('subject');
    my $message = $q->param('message');

    # E-mail以外が入力されているか検証
    if ($name && $subject && $message) {
        # 検証OK：ログを保存してリダイレクト (PRGパターン)
        &saveLog;
        print $q->redirect(-uri => $script, -status => 303);
        exit;
    } else {
        # 検証NG：エラーページを表示
        &printHTMLnotValid;
    }
} else {
    # ページを初回表示する場合
    &printHTML;
}


# 新規メッセージをログファイルに保存するサブルーチン
sub saveLog {
    my $time    = &getTime;
    my $name    = $q->param('name');
    my $address = $q->param('address');
    my $subject = $q->param('subject');
    my $message = $q->param('message');
    
    # メッセージ内の改行を <br> に置換
    $message =~ s/\r?\n/<br>/g;
    
    # タブ文字を区切り文字としてデータを連結
    my $log_line = join("\t", $time, $name, $address, $subject, $message) . "\n";
    
    open my $fh, '>>', $log_file or &printError("ログファイルが開けません: $log_file");
    
    # ファイルを排他ロックしてから書き込む
    flock($fh, LOCK_EX);
    print $fh $log_line;
    close $fh;
}

# メッセージをログファイルから読み込み、HTMLとして出力するサブルーチン
sub getLog {
    open my $fh, '<', $log_file or return "<p>まだ投稿はありません。</p>"; # エラーでもdieさせない
    my @lines = <$fh>;
    close $fh;
    
    my @html_lines;
    foreach my $line (reverse @lines) { # 新しい投稿を上に表示
        chomp $line;
        # タブで分割し、各要素をHTMLエスケープ
        my ($time, $name, $address, $subject, $message) = map { $q->escapeHTML($_) } split /\t/, $line;
        
        my $escaped_address = $address ? "($address)" : ""; # アドレスが空なら表示しない

        # メッセージの<br>はエスケープ済みなので元に戻す
        $message =~ s/&lt;br&gt;/<br>/gi;

        push @html_lines, <<"EOF";
<div style="border-bottom: 1px solid #ccc; padding: 10px 0;">
  <p><strong>件名: $subject</strong></p>
  <p>名前: <em>$name</em> $escaped_address</p>
  <p>$message</p>
  <p style="text-align: right; color: #555; font-size: 0.9em;">$time</p>
</div>
EOF
    }
    return join("\n", @html_lines);
}

# フォームをHTMLとして出力するサブルーチン（入力値保持対応）
sub getForm {
    # フォームの各入力値を取得してHTMLエスケープ
    my $name    = $q->escapeHTML($q->param('name'));
    my $address = $q->escapeHTML($q->param('address'));
    my $subject = $q->escapeHTML($q->param('subject'));
    my $message = $q->escapeHTML($q->param('message'));

    return <<"EOF";
<form method="POST" action="$script" style="border: 1px solid #ccc; padding: 15px; margin-top: 20px;">
  <label for="name">名前: <span style="color:red;">*</span></label><br>
  <input type="text" id="name" name="name" value="$name" required style="width: 50%;"><br><br>
  
  <label for="address">アドレス:</label><br>
  <input type="text" id="address" name="address" value="$address" style="width: 50%;"><br><br>
  
  <label for="subject">件名: <span style="color:red;">*</span></label><br>
  <input type="text" id="subject" name="subject" value="$subject" required style="width: 80%;"><br><br>
  
  <label for="message">メッセージ: <span style="color:red;">*</span></label><br>
  <textarea id="message" name="message" required rows="5" style="width: 80%;">$message</textarea><br><br>
  
  <input type="submit" value="送信">
</form>
EOF
}

# エラーメッセージをHTMLとして出力するサブルーチン
sub printError {
    my ($error_message) = @_;
    print $q->header('text/html; charset=UTF-8');
    print <<"EOF";
<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><title>CGIエラー</title></head>
<body><h1>エラーが発生しました</h1>
<p>申し訳ありませんが、処理中にエラーが発生しました。</p>
<p style="color: red;"><strong>@{[ $q->escapeHTML($error_message) ]}</strong></p>
</body></html>
EOF
    exit; # dieではなくexit
}

# 現在の時刻を取得するサブルーチン
sub getTime {
    my @t = localtime(time);
    return sprintf("%04d-%02d-%02d %02d:%02d:%02d", $t[5]+1900, $t[4]+1, $t[3], $t[2], $t[1], $t[0]);
}

# 完全なHTMLを出力するサブルーチン
sub printHTML {
    print $q->header('text/html; charset=UTF-8');
    print <<"EOF";
<!DOCTYPE html>
<html lang="ja">
<head><meta charset="UTF-8"><title>掲示板</title></head>
<body>
  <h1>掲示板</h1>
  <hr>
  <h2>投稿一覧</h2>
  <div>
    @{[&getLog]}
  </div>
  <hr>
  <h2>新規投稿</h2>
  <div>
    @{[&getForm]}
  </div>
</body>
</html>
EOF
}

# 入力漏れがあった場合に注意を促すHTMLを出力するサブルーチン
sub printHTMLnotValid {
    print $q->header('text/html; charset=UTF-8');
    print <<"EOF";
<!DOCTYPE html>
<html lang="ja">
<head><meta charset="UTF-8"><title>入力エラー</title></head>
<body>
  <h1>入力エラー</h1>
  <p style="color: red;"><strong>名前、件名、メッセージは必須項目です。全て入力してください。</strong></p>
  <hr>
  @{[&getForm]}
</body>
</html>
EOF
}