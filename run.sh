#!/usr/bin/env bash

# Main driver to submit jobs 
# Author SHI Xin <shixin@ihep.ac.cn>
# Created [2017-11-23 Thu 10:47] 

usage() {
    printf "NAME\n\trun.sh - Main driver to run metro\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%-5s\n" "./run.sh [OPTION]" 
    printf "\nOPTIONS\n" 
    printf "\n\t%-9s  %-40s" "20170223" " Hybrid with distance"
    printf "\n\t%-9s  %-40s" "20171123P" " Yiming predicted: 20171123P" 
    printf "\n\t%-9s  %-40s" "20171123M" " Yiming measured: 20171123M" 
    printf "\n\t%-9s  %-40s" "20171124M" " Xin measured: 20171124M" 
    printf "\n\t%-9s  %-40s" "20171127c" " Compare bridge tool No.11 metrology on 27th and 23rd Nov"
    printf "\n\t%-9s  %-40s" "20171127P1" " Yiming predicted: 20171123P1 for adjusting set No.31 targetting 120um" 
    printf "\n\t%-9s  %-40s" "20171127P2" " Yiming predicted: 20171123P2 set No.31 targetting 120um after 1st adjustion" 

    printf "\n\n" 
}

if [[ $# -eq 0 ]]; then
    usage
    echo "Please enter your option: "
    read option
else
    option=$1    
fi

case $option in
    
    20170223) echo "Hybrid with distance"
	./python/metroHybrid.py data/panel_VII_20170223_h2.txt data/set_11_laser_170116.txt
	;;
 
    20171123P) echo "Running on 20171123 Yiming: predicted glue thickness for adjustment"
	./python/metroHybrid.py data/panel102_h2_20171123.TXT data/set_11_laser_171123.TXT 
	;;
    
    20171123M) echo "Running on 20171123 Yiming: measured glue thickness"
  ./python/metroHybrid.py data/panel102_h2_20171123.txt data/panel102_h2_20171123_withASICs.TXT data/set_11_laser_171123.TXT
	;;

    20171124M) echo "Running on 20171124 Xin: measured glue thickness"
  ./python/metroHybrid.py data/panel102_h5_20171124.TXT data/panel102_h5_20171124_withASICs.TXT data/set_11_laser_171123.TXT
	;;

    20171127c) echo "Comparing bridge tool metrology on 20171123 and 20171127. NB: 0.0 in last column = no difference"
    diff -y ./data/set_11_laser_171123.txt ./data/set_11_laser_171127.txt | grep Z | awk '{ print $1, $2, $8 }'
    ;;

    20171127P1) echo "Running on 20171127 Yiming: predicted glue thickness for adjustment set No.31"
	./python/metroHybrid.py data/panel102_h2_20171123.TXT data/set_31_laser_171127.TXT 
	;;

    20171127P2) echo "Running on 20171127 Yiming: predicted glue thickness for adjustment set No.31"
	./python/metroHybrid.py data/panel102_h2_20171123.TXT data/set_31_laser_171127_adjust1.TXT 
	;;

esac
