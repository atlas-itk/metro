#!/bin/python

__author__ = "CHEN Liejian <chenlj@ihep.ac.cn>"

import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
HybridThickness=0.254
#----------------------------------------------------------------------
def csv_writer(data, path):
    """
    Write data to a CSV file path
    """
    with open(path, "w") as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        for val in data:
            writer.writerow([val])

#----------------------------------------------------------------------
def csv_writer_table(data, path):
    """
    Write data to a CSV file path
    """
    with open(path, "w") as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        for val in data:
            writer.writerows([val])

#----------------------------------------------------------------------
def readBridgeTool(filename):
    with open(filename) as f:
        data = f.readlines()
        f.close()
    x_pos = []
    y_pos = []
    z_pos = []
    nlines = len(data)
    for line in range(nlines):
        value = data[line].split()
        if value[0]=='X':
            print(value[3])
            x_pos.append(float(value[3]))  # x position#
        elif value[0]=='Y':
            print(value[3])
            y_pos.append(float(value[3]))
        elif value[0]=='Z':
            print(value[3])
            z_pos.append(float(value[3]))

    results = zip(x_pos,y_pos,z_pos)
    results = zip(*results)

    path = str(filename) + ".csv"
    csv_writer_table(results,path)

    return z_pos

#----------------------------------------------------------------------
def readHybridWithoutASICs(filename):
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
            print(value[3])
            z_pos.append(float(value[3]))  # z position
        elif value[0]=='ZD':
            print(value[3])
            z_d.append(float(value[3])) # z distance

    results = zip(z_pos,z_d)
    results = zip(*results)

    path = str(filename) + ".csv"
    csv_writer_table(results,path)

    zd = z_d[1:11]
    return zd

#----------------------------------------------------------------------
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
            print(value[3])
            z_pos.append(float(value[3]))  # z position
        elif value[0]=='ZD':
            print(value[3])
            z_d.append(float(value[3])) # z distance

    results = zip(z_pos,z_d)
    results = zip(*results)

    path = str(filename) + ".csv"
    csv_writer_table(results,path)

    zd = z_d[1:11]
    return zd

def readDummyModules(filename):
    with open(filename) as f:
        data = f.readlines()
    f.close()

    x_pos = []
    y_pos = []
    z_pos = []
    z_d = []

    nlines = len(data)
    for line in range(nlines):
        value = data[line].split()
        if value[0]=='X':
            print(value[3])
            x_pos.append(float(value[3]))  # x position#
        elif value[0]=='Y':
            print(value[3])
            y_pos.append(float(value[3]))
        elif value[0]=='Z':
            print(value[3])
            z_pos.append(float(value[3]))
        elif value[0]=='ZD':
            z_d.append(float(value[3])) # z distance

    p_sensor=[x_pos[0:4],y_pos[0:4]]
    p_left=[x_pos[4:10],y_pos[4:10]]
    p_right=[x_pos[10:16],y_pos[10:16]]
    pd_left=[x_pos[16:27],y_pos[16:27]]
    pd_right=[x_pos[27:38],y_pos[27:38]]
    zd_left=z_d[0:11]
    zd_right=z_d[11:22]

    return p_sensor,p_left,p_right,pd_left,pd_right,zd_left,zd_right

def line2box(datalist):
    databox_x=datalist[0] # x
    databox_x.append(datalist[0][0])
    databox_y=datalist[1] # y
    databox_y.append(datalist[1][0])
    return databox_x, databox_y

def plot_DummyModule(p_sensor,p_left,p_right,pd_left,pd_right,zd_left,zd_right):
    sensor_x, sensor_y=line2box(p_sensor)
    sensor_line=Line2D(sensor_x,sensor_y)

    left_x, left_y=line2box(p_left)
    left_line=Line2D(left_x,left_y)

    right_x, right_y=line2box(p_right)
    right_line=Line2D(right_x,right_y)

    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.add_line(sensor_line)
    ax.add_line(left_line)
    ax.add_line(right_line)
    ax.set_xlim(min(sensor_x)-10,max(sensor_x)+10)
    ax.set_ylim(min(sensor_y)-10,max(sensor_y)+10)

    ax.plot(pd_left[0],pd_left[1],marker='o',color='r',ls='')
    ax.plot(pd_right[0],pd_right[1],marker='o',color='r',ls='')

    for i in range(len(zd_left)):
        ax.text(pd_left[0][i],pd_left[1][i]-10,"{:1.3f}".format(zd_left[i]-HybridThickness))
        ax.text(pd_right[0][i],pd_right[1][i]-10,"{:1.3f}".format(zd_right[i]-HybridThickness))

    ax.text(-1,101,"Dummy Module M1")
    plt.show()

#----------------------------------------------------------------------
def average_bridge(zpos):
    zd_asic = []
    z_touchpin = np.mean(zpos[0:4])
    for i in range(1,11):
        zpos_asic = np.mean(zpos[(0+4*i):(4+4*i)])
        zd_asic.append(z_touchpin-zpos_asic)
    return zd_asic

#----------------------------------------------------------------------
if __name__ == "__main__":


    ### Hybrid
    '''
    filename1 = 'set_09_laser_170413_H5.TXT'
    zpos_BridgeTool = readBridgeTool(filename1)

    filename2 = 'panelVII_20170413_H5_h2.TXT'
    zd_Hybrid_wo = readHybridWithoutASICs(filename2)

    filename3 = 'panelVII_20170509_H5_h2_ASICs.TXT'
    zd_Hybrid_w = readHybridWithASICs(filename3)

    print("zpos_BridgeTool: " + str(zpos_BridgeTool))
    print("zd_Hybrid_wo: " + str(zd_Hybrid_wo))
    print("zd_Hybrid_w: " + str(zd_Hybrid_w))

    zd_BridgeTool = average_bridge(zpos_BridgeTool)
    print(zd_BridgeTool)
    expected_glue_thickness = []
    measured_glue_thickness = []
    for i in range(0,(len(zd_Hybrid_wo))):
        expected_glue_thickness.append((zd_BridgeTool[i] + zd_Hybrid_wo[i] - 0.3)*1000)
        measured_glue_thickness.append((zd_Hybrid_w[i] + zd_Hybrid_wo[i] - 0.3)*1000)

    print("expected_glue_thickness: " + str(expected_glue_thickness))
    print("measured_glue_thickness: " + str(measured_glue_thickness))

    csv_writer(expected_glue_thickness,"expected_results.csv")
    csv_writer(measured_glue_thickness,"measured_results.csv")
    '''

    filename='DummyModule_M1.TXT'
    p_sensor,p_left,p_right,pd_left,pd_right,zd_left,zd_right=readDummyModules(filename)
    plot_DummyModule( p_sensor,p_left,p_right,pd_left,pd_right,zd_left,zd_right)

