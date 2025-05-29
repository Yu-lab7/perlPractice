open(DATA,"datafile");
while(<DATA>){
    print $_;
}

close(DATA);