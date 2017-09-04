#!/usr/bin/env python


"""
Hybrid Metrology for ATLAS ITk 

Adapted from Liejian Chen's moduleMetrology.py  
"""

__author__ = "SHI Xin <shixin@ihep.ac.cn>"



import sys
import matplotlib.pyplot as plt

ASIC_THICKNESS = 300 #um 


def main():
    args = sys.argv[1:]
    if len(args) == 0 :
        return usage()
    if len(args) == 1: 
        inputfile = args[0]
        sys.stdout.write('Input file: %s\n' % inputfile)
        sys.stdout.write('ASCI_THICKNESS: %s um\n' % ASIC_THICKNESS)
        return plot_hybrid_glue_thickness(inputfile)


def usage():
    sys.stdout.write('''
NAME
    hybrid.py 
SYNOPSIS
    hybrid.py inputdata.txt

AUTHOR
    SHI Xin <shixin@ihep.ac.cn>.

DATE
    September 2017 
\n''')



def plot_hybrid_glue_thickness(filename): 
    zd = readHybridWithASICs(filename)
    glue_thickness = [h*1000-ASIC_THICKNESS for h in zd ]#
    print glue_thickness
    plt.plot(glue_thickness)
    plt.ylabel('glue thickness [um]')
    plt.show()


def readHybridWithASICs(filename):
    with open(filename) as f:
        data = f.readlines()
    f.close()

    z_pos = []
    z_d = []
    z_d.append(0) # Datum plane, no distance
    nlines = len(data)
    for line in range(nlines):
        value = data[line].split()
        if value[0]=='Z':
            #print(value[3])
            z_pos.append(float(value[3]))  # z position
        elif value[0]=='ZD':
            #print(value[3])
            z_d.append(float(value[3])) # z distance

    results = zip(z_pos,z_d)
    results = zip(*results)

    zd = z_d[1:11]
    return zd



if __name__ == '__main__':
    main()

