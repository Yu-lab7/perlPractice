my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime(time);
printf("%d 年 %02d 月 %02d 日 %02d 時 %02d 分", $year + 1900, $mon + 1, $mday, $hour, $min);