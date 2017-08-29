###################################################################
# File Name: stat_fq.pl
# Author: yaomingyue
# mail: yaomingyue@fuanhua.com
# Created Time: 2017年08月04日 星期五 16时02分21秒
#=============================================================
#!/usr/bin/env perl
use strict;
use warnings;
die "This script was stat the fq.gz\n\nUsage:\n\tperl $0 <fq.gz> <report> [33 or 64, 33 is default]\n" unless @ARGV>=2 and @ARGV<=3;
my ($fq_gz,$report,$Phred)=@ARGV;
$Phred||=33;
my $leng=0;
my (%base,%qual);
my $read_num=0;
my $base_num=0;
my $N_num=0;
my $GC_num=0;
my $Q20_num=0;
my $Q30_num=0;
my @ATCGN=qw/A T C G N/;
open IN,"gzip -dc $fq_gz|" or die "can't open it";
while(<IN>){
	chomp;
	chomp(my $read=<IN>);
	$leng=length $read if $leng<=length $read;
	my @letter=split("",$read);
	my $plus=<IN>;
	chomp(my $value=<IN>);
	$read_num++;
	my @val=split("",$value);
	for my $i(0..$#letter){
		$base_num++;
		if ($letter[$i] eq "N"){
			$N_num++;
		}elsif ($letter[$i] eq "G" or $letter[$i] eq "C"){
			$GC_num++;
		}elsif ($letter[$i] ne "A" and  $letter[$i] ne "T"){
			die "$_ exist $letter[$i]\n";
		}
		if (exists $base{$i}{$letter[$i]}){
			$base{$i}{$letter[$i]}++;
		}else{
			$base{$i}{$letter[$i]}=1;
		}
		my $phred=ord($val[$i])-$Phred;
		if ($phred>42){die "########$_ has phred of a letter >42\n"}
		if ($phred>=20){$Q20_num++}
		if ($phred>=30){$Q30_num++}
		if (exists $qual{$i}{$phred}){
			$qual{$i}{$phred}++;
		}else{
			$qual{$i}{$phred}=1;
		}
	}
}
close IN;
open OUT,">$report" or die "can't open $report\n";
print OUT "#\tA\tT\tC\tG\tN";
for my $j(0..42){
	print OUT "\t$j";
}
print OUT "\n";
for my $k(1..$leng){
	print OUT "$k";
	for my $l (@ATCGN){
		if (exists $base{$k-1}{$l}){
			print OUT "\t$base{$k-1}{$l}";
		}else{
			print OUT "\t0";
		}
	}
	for my $m (0..42){
		if (exists $qual{$k-1}{$m}){
			print OUT "\t$qual{$k-1}{$m}";
		}else{
			print OUT "\t0";
		}
	}
	print OUT "\n";
}
my $N_percent=$N_num/$base_num*100;
my $GC_percent=$GC_num/$base_num*100;
my $Q20_percent=$Q20_num/$base_num*100;
my $Q30_percent=$Q30_num/$base_num*100;
print OUT "#total reads\t$read_num\n";
print OUT "#total_base\t$base_num\n";
printf OUT ("#N_percent(%%)\t%.3f\n",$N_percent);
printf OUT ("#Q20(%%)\t%.3f\n",$Q20_percent);            #single % should use %%
printf OUT ("#Q30(%%)\t%.3f\n",$Q30_percent);
printf OUT ("#GC_percent(%%)\t%.3f\n",$GC_percent);
close OUT;
