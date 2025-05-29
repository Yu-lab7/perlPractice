$line = 'aaa,bbb,ccc';
($a, $b, $c) = split(/,/, $line);
print $a, $b, $c;