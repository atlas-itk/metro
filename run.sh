#!/usr/bin/env bash

# Main driver to submit jobs 
# Author SHI Xin <shixin@ihep.ac.cn>
# Created [2017-11-23 Thu 10:47] 

usage() {
    printf "NAME\n\trun.sh - Main driver to run metro\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%-5s\n" "./run.sh [OPTION]" 
    printf "\nOPTIONS\n" 
printf "\n\t%-9s  %-40s" "20171123" " Yiming: 20171123" 

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
    
    # --------------------------------------------------------------------------
    #  20171123 Yiming
    # --------------------------------------------------------------------------

    20171123) echo "Running on 20171123 Yiming"
	./python/metroHybrid.py data/panel102_h2_20171123.TXT data/set_11_laser_171123.TXT 
	;;

esac
