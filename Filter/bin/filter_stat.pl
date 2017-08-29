###################################################################
# File Name: filter_stat.pl
# Author: yaomingyue
# mail: yaomingyue@fuanhua.com
# Created Time: 2017年08月28日 星期一 15时22分57秒
#=============================================================
#!/usr/bin/env perl
use strict;
use warnings;
use File::Basename;
die "Usage:\n\tperl $0 <indir (includes Rawdata and Cleandata)> <output>\n" unless @ARGV==2;
my($indir,$output)=@ARGV;
my(%hash,@samples);
my @files=glob("$indir/Cleandata/*");
for my $i (@files){
    my @reports=glob("$i/*report");
    my $tmp=basename($i);
    push @samples,$tmp;
    if (@reports==2){
        $hash{$tmp}{"type"}="PE";
    }else{
        $hash{$tmp}{"type"}="SE";
    }
    for my $j (@reports){
        open IN,"<$j" or die "Can't open $j\n";
        my $line=<IN>;
        while(<IN>){
            chomp;
            my @a=split(/\t/,$_);
            unless (/^#/){
                if (exists $hash{$tmp}{"len"}){
                    $hash{$tmp}{"len"}=$a[0] if $a[0]>$hash{$tmp}{"len"};
                }else{
                    $hash{$tmp}{"len"}=$a[0];
                }
            }
            if (/reads/){
                if (exists $hash{$tmp}{"Clean_reads"}){
                    $hash{$tmp}{"Clean_reads"}+=$a[1];
                }else{
                    $hash{$tmp}{"Clean_reads"}=$a[1];
                }
            }elsif (/base/){
                if (exists $hash{$tmp}{"Clean_base"}){
                    $hash{$tmp}{"Clean_base"}+=$a[1];
                }else{
                    $hash{$tmp}{"Clean_base"}=$a[1];
                }
            }elsif(/Q30/){
                if (exists $hash{$tmp}{"Clean_Q30"}){
                    $hash{$tmp}{"Clean_Q30"}+=$a[1];
                    $hash{$tmp}{"Clean_Q30"}/=2;
                }else{
                    $hash{$tmp}{"Clean_Q30"}=$a[1];
                }
            }
       }
       close IN;
    }
}
for my $k (@samples){
    my @raw_reports=glob("$indir/Rawdata/$k/*report");
    for my $m(@raw_reports){
        open ININ,"<$m" or die "Can't open $m\n";
        my $line=<ININ>;
        while(<ININ>){
            chomp;
            my @b=split(/\t/,$_);
            if (/reads/){
                if (exists $hash{$k}{"Raw_reads"}){
                    $hash{$k}{"Raw_reads"}+=$b[1];
                }else{
                    $hash{$k}{"Raw_reads"}=$b[1];
                }
            }elsif (/base/){
                if (exists $hash{$k}{"Raw_base"}){
                    $hash{$k}{"Raw_base"}+=$b[1];
                }else{
                    $hash{$k}{"Raw_base"}=$b[1];
                }
            }elsif(/Q30/){
                if (exists $hash{$k}{"Raw_Q30"}){
                    $hash{$k}{"Raw_Q30"}+=$b[1];
                    $hash{$k}{"Raw_Q30"}/=2;
                }else{
                    $hash{$k}{"Raw_Q30"}=$b[1];
                }
            }
       }
       close ININ;
    }
}
open OUT,">$output" or die "Can't open $output\n";
print OUT "Sample\tRaw Reads\tRaw bases\tClean Reads\tClean bases\tClean rate(%)\tRaw Q30(%)\tClean Q30(%)\tSequence type\n";
for my $sample(@samples){
    my $clean_rate=$hash{$sample}{"Clean_base"}/$hash{$sample}{"Raw_base"};
    print OUT "$sample\t$hash{$sample}{Raw_reads}\t$hash{$sample}{Raw_base}\t$hash{$sample}{Clean_reads}\t$hash{$sample}{Clean_base}\t$clean_rate\t$hash{$sample}{Raw_Q30}\t$hash{$sample}{Clean_Q30}\t$hash{$sample}{type}$hash{$sample}{len}\n";
}
close OUT;
    
