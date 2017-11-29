#!/usr/bin/env python

"""
Module Metrology for ATLAS ITk
"""

__author__ = "Craig Sawyer <craig.sawyer@stfc.ac.uk>"

import ROOT, math
from array import *
import sys

# GET FILE NAME FROM USER
user_input = raw_input("Enter module name (eg. RAL_TM1): ")


# RUNNING PARAMETERS
fname = user_input+"_Metrology.txt"		# NAME OF METROLOGY OUTPUT FILE

hybridThickness = 0.250			# ASSUMED HYBRID THICKNESS
LH_present = 1					# WHETHER LH HYBRID IS PRESENT
RH_present = 1					# WHETHER RH HYBRID IS PRESENT

# OPEN FILE
f = open(fname)

# SETUP ROOT
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

# CHANGE MEASUREMENT ORDER DEPENDENT ON WHAT IS PRESENT
if LH_present and RH_present:
	LH_start = 68   
	RH_start = 26   
	if user_input == "RAL_TM1":
		LH_start = 24   # 24 for RAL_TM1, 68 for others
		RH_start = 4   # 4 for RAL_TM1, 26 for others
elif LH_present and not RH_present:
	LH_start = 68
	RH_start = -1
elif RH_present and not LH_present:
	LH_start = -1
	RH_start = 26
else:
	print "\nERROR - I'm not a sensor metrology script!!!"
	sys.exit()
	
# READ MEASUREMENT VALUES
x_m,y_m,z_m = [],[],[]
for l in f.readlines():
	l = l.strip()
	if not ("X" in l[0] or "Y" in l[0] or "Z" in l[0]): continue
	val = float(l.split()[1])
	if "X" in l[0]: x_m.append(val)
	elif "Y" in l[0]: y_m.append(val)
	elif "Z" in l[0]: z_m.append(val)
	
# DRAW BASIC MODULE
c1 = ROOT.TCanvas("c1","c1",600,600)
c1.SetTopMargin(0.1)
c1.SetLeftMargin(0.1)
c1.SetRightMargin(0.1)
c1.SetBottomMargin(0.1)

module = ROOT.TH1F("module","module",1,0,97.54)
module.SetMinimum(0)
module.SetMaximum(97.54)

module.GetXaxis().SetTickLength(0)
module.GetXaxis().SetLabelSize(0)
module.GetYaxis().SetTickLength(0)
module.GetYaxis().SetLabelSize(0)

module.Draw()

text = ROOT.TLatex(0,0,"")
text.SetTextFont(43)
text.SetTextSize(20)
line = ROOT.TLine(0,0,0,0)
arrow = ROOT.TArrow(0,0,0,0)
smalltext = ROOT.TLatex(0,0,"")
smalltext.SetTextFont(43)
smalltext.SetTextSize(12)

if RH_present:
	# DRAW MEASURED EDGE OF RH HYBRID
	line.DrawLine(0,y_m[0],97.54,y_m[1])
	arrow.DrawArrow(1.5,0,1.5,y_m[0],0.02,"<>")
	text.DrawLatex(2.5,y_m[0]/2.2,str(y_m[0]))
	arrow.DrawArrow(97.54-1.5,0,97.54-1.5,y_m[1],0.02,"<>")
	text.DrawLatex(97.54-14.5,y_m[1]/2.2,str(y_m[1]))

	# DRAW REST OF RH HYBRID
	line.DrawLine(0,y_m[0]+17,20.5,y_m[0]+17+(y_m[1]-y_m[0])/97.54*20.5)
	line.DrawLine(20.5,y_m[0]+17+(y_m[1]-y_m[0])/97.54*20.5,22,y_m[0]+17+(y_m[1]-y_m[0])/97.54*20.5-1.5)
	line.DrawLine(22,y_m[0]+17+(y_m[1]-y_m[0])/97.54*20.5-1.5,97.54,y_m[1]+15.5)

if LH_present:
	# DRAW MEASURED EDGE OF LH HYBRID
	line.DrawLine(0,97.54-y_m[2],97.54,97.54-y_m[3])
	arrow.DrawArrow(1.5,97.54,1.5,97.54-y_m[2],0.02,"<>")
	text.DrawLatex(2.5,97.54-y_m[2]/1.8,str(y_m[2]))
	arrow.DrawArrow(97.54-1.5,97.54,97.54-1.5,97.54-y_m[3],0.02,"<>")
	text.DrawLatex(97.54-14.5,97.54-y_m[3]/1.8,str(y_m[3]))

	# DRAW REST OF LH HYBRID
	line.DrawLine(0,97.54-y_m[2]-17,20.5,97.54-y_m[2]-17-(y_m[2]-y_m[3])/97.54*20.5)
	line.DrawLine(20.5,97.54-y_m[2]-17-(y_m[2]-y_m[3])/97.54*20.5,22,97.54-y_m[2]-17-(y_m[2]-y_m[3])/97.54*20.5+1.5)
	line.DrawLine(22,97.54-y_m[2]-17-(y_m[2]-y_m[3])/97.54*20.5+1.5,97.54,97.54-y_m[3]-15.5)

if RH_present:
	# MAKE LIST OF MEASUREMENT POINTS ON RH HYBRIDS
	x_RH,y_RH,z_RH = [],[],[]
	for p in range(RH_start,RH_start+20):
		x_RH.append(x_m[p])
		y_RH.append(y_m[p]+y_m[0])
		z_RH.append(z_m[p])
		smalltext.DrawLatex(x_m[p]+1.5,y_m[p]+y_m[0]-1,str(z_m[p]-hybridThickness))
		
	# MAKE GRAPH OF X-Y POINTS ON RH HYBRIDS
	g_RH = ROOT.TGraph(len(x_RH),array('f',x_RH),array('f',y_RH))
	g_RH.SetMarkerStyle(29)
	g_RH.Draw("psame")

if LH_present:
	# MAKE LIST OF MEASUREMENT POINTS ON LH HYBRIDS
	x_LH,y_LH,z_LH = [],[],[]
	for p in range(LH_start,LH_start+21):
		x_LH.append(97.54-x_m[p])
		y_LH.append(97.54-y_m[2]-y_m[p])
		z_LH.append(z_m[p])
		smalltext.DrawLatex(97.54-x_m[p]+1.5,97.54-y_m[2]-y_m[p]-1,str(z_m[p]-hybridThickness))
		
	# MAKE GRAPH OF X-Y POINTS ON LH HYBRIDS
	g_LH = ROOT.TGraph(len(x_LH),array('f',x_LH),array('f',y_LH))
	g_LH.SetMarkerStyle(29)
	g_LH.Draw("psame")

#c1.Print("module_"+user_input+".png")
c1.Print("module_"+user_input+".pdf")

# OUTPUT RESULTS TO CSV FILE

outfile = open("results_"+user_input+".csv","w")

print >> outfile, ",LH,RH"
print >> outfile, "Data-end,"+str(y_m[2])+","+str(y_m[0])
print >> outfile, "Power-end,"+str(y_m[3])+","+str(y_m[1])
for fid in range(0,21):
	if fid == 3:
		print >> outfile, "F"+str(fid)+","+str(z_m[LH_start+20-fid]-hybridThickness)
	elif fid < 3:
		print >> outfile, "F"+str(fid)+","+str(z_m[LH_start+20-fid]-hybridThickness)+","+str(z_m[RH_start+fid]-hybridThickness)
	elif fid > 3:
		print >> outfile, "F"+str(fid)+","+str(z_m[LH_start+20-fid]-hybridThickness)+","+str(z_m[RH_start+fid-1]-hybridThickness)
	

