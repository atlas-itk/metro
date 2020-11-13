#!/usr/bin/python
import ROOT
import numpy as np
import matplotlib.pyplot as plt


def Plot_Hybrid_Glue_height(inFileName):
  # in data file
  inFile = open(inFileName, "r")
  #print(inFile)

  lines = inFile.readlines()
 
  ASICS = ["ABC0", "ABC1", "ABC2", "ABC3", "ABC4", "ABC5", "ABC6", "ABC7", "ABC8", "ABC9"]
  hight = []
  for line in lines:
    #print(line.split()[:15])
    if "Math" in line:
      for item in line.split()[2:15]:
        hight.append(float(item))
  #print(hight)
  #print(hight[::-1])

  glue_thickness = [h*1000 for h in hight[::-1]] 
  print (glue_thickness)
  fig=plt.figure()
  plt.style.use('classic')
  plt.plot(glue_thickness,'-or',label='measured glue thickness')
  plt.ylabel('Glue+ASICS thickness [$\mu$m]')
  plt.xlim([-1, 10])
  plt.ylim([200, 600])
  plt.tick_params(axis='both', direction='in', length=6, width=1, colors='k',grid_color='k', grid_alpha=0.5)
  plt.xticks(np.arange(10), ASICS, rotation=60)
  fig.show()

  plt.savefig('../plots/Glue_Height.png')


if __name__ == "__main__":

  inFileName = "../data/Hybrid_metrology_GlueHeight.txt"
  Plot_Hybrid_Glue_height(inFileName)
