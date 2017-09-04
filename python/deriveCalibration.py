import ROOT, math
from array import *

ROOT.gStyle.SetOptStat(0)

# configuration variables
glueTarget = 80                       # target for glue thickness in microns
panelID = "IHEP"                        # panel ID for reading hybrid data
panelDate = "170814"                  # date for reading hybrid data
bridgeID = "06f"                       # bridge ID for reading bridge data
bridgeDate = "170814"                 # date for reading bridge data
micronsPerTurn = 254                  # thread of screw in terms of microns per full turn
weights = [1,1,1,1,1,1,1,1]	          # define the weight applied to each hybrid when deriving the calibration required
method = "laser"                      # define the method of bridge metrology

# define useful things
corrections = [0.0,0.0,0.0,0.0]
outfile = ROOT.TFile("out_panel_"+panelID+"_"+panelDate+"_bridge_"+bridgeID+"_"+method+"_"+bridgeDate+".root","RECREATE")

#normalise weights
sumOfWeights = 0
for w in weights: sumOfWeights += w
for w in weights: w = w / sumOfWeights * 8.0

# read panel data
panel_hists = []
for i in range(0,8):
	panel_hists.append(ROOT.TH1F("hybrid_"+str(i),"hybrid "+str(i),10,-0.5,9.5))
	fname = "panel_"+panelID+"_"+panelDate+"_h"+str(i)+".txt"
	f = open(fname)
	count = 0
	for l in f.readlines():
		l = l.strip()
		if "Z" not in l[:2]: continue
		val = -1*float(l.split()[3])*1000
		panel_hists[-1].SetBinContent(count+1,val)
		count += 1
	f.close()
	panel_hists[-1].Write()
		
# read bridge data
bridge_pins = []
bridge_pads = []
fname = "set_"+bridgeID+"_"+method+"_"+bridgeDate+".txt"
f = open(fname)
count = 1
point = []
for l in f.readlines():
	l = l.strip()
	if "X" in l[0] or "Y" in l[0]: point.append(int(float(l.split()[3])*1000))
	elif "Z" in l[0]:
		point.append(int(float(l.split()[3])*1000))
		if count < 13:
			bridge_pins.append(point)
		else:
			bridge_pads.append(point)
		point = []
	else:
		continue
	count += 1
	
# make a histogram to subtract the chip thickness
hist_chip = ROOT.TH1F("chips","chips",10,-0.5,9.5)
for i in range(0,10):
	hist_chip.SetBinContent(i+1,300)
	
def fitPlaneToPoints(points):
	x = []
	y = []
	z = []
	for p in points:
		x.append(p[0])
		y.append(p[1])
		z.append(p[2])
	g = ROOT.TGraph2D(len(x),array('f',x),array('f',y),array('f',z))
	f = ROOT.TF2("f","[0]*x+[1]*y+[2]")
	g.Fit(f,"Q")
	return [f.GetParameter(0),f.GetParameter(1),f.GetParameter(2)]
	
def makeResidualsHist(points,param,name):
	h = ROOT.TH1F("residuals_"+name,"residuals "+name,30,-15,15)
	for p in points:
		residual = (param[0]*p[0]+param[1]*p[1]-p[2]+param[2]) / math.sqrt( param[0]*param[0] + param[1]*param[1] + 1 )
		h.Fill(residual)
	return h

def derivePlaneCorrection(points,param):
	# use first point as pivot and correct plane definition
	pivot = points[0]
	param[2] -= (param[0]*pivot[0] + param[1]*pivot[1] + param[2]) - pivot[2]
	# derive corrections based on this
	for i in range(1,4):
		p = points[i]
		corrections[i] += (param[0]*p[0]+param[1]*p[1]+param[2]) - p[2]

def calculateBridgeHeights(points,param,name):
	hist = ROOT.TH1F("bridge_"+name,"bridge "+name,10,-0.5,9.5)
	for i in range(0,10):
		sum = 0.0
		for j in range(0,4):
			p = points[39-j-i*4]
			sum += (param[0]*p[0]+param[1]*p[1]-p[2]+param[2]) / math.sqrt( param[0]*param[0] + param[1]*param[1] + 1 )
		mean = sum / 4
		hist.SetBinContent(i+1,mean)
	return hist
		
def drawBridgeHist(h):
	h.SetMinimum(300)
	h.SetMaximum(350)
	h.GetXaxis().SetTitle("Position")
	h.GetYaxis().SetTitle("Touchdown to ASIC pick-up [um]")
	h.Draw()
	
def drawHybridHist(hists):
	h = hists[0]
	h.SetMinimum(40)
	h.SetMaximum(120)
	h.GetXaxis().SetTitle("Position")
	h.GetYaxis().SetTitle("Glue Thickness [um]")
	h.SetTitle(h.GetTitle().replace(" 0","s"))
	h.Draw()
	for i in range(1,8):
		hists[i].SetLineColor(i+1)
		hists[i].Draw("histsame")
		
# fit plane to touchdown and get residuals
parameters_pins = fitPlaneToPoints(bridge_pins)
residuals_pins = makeResidualsHist(bridge_pins,parameters_pins,"pins")
residuals_pins.Write()

# fit plane to ASIC pads and get residuals
parameters_pads = fitPlaneToPoints(bridge_pads)
residuals_pads = makeResidualsHist(bridge_pads,parameters_pads,"pads")
residuals_pads.Write()

# make histogram of the bridge heights before any correction
hist_bridge_before = calculateBridgeHeights(bridge_pads,parameters_pins,"before")
hist_bridge_before.Write()

# calculate the predicted glue thicknesses with current setting
hists_before = []
for hist in panel_hists:
	histClone = hist.Clone(hist.GetName()+"_before")
	histClone.SetTitle(histClone.GetTitle()+" before")
	histClone.Add(hist_bridge_before)
	histClone.Add(hist_chip,-1)
	hists_before.append(histClone)
	histClone.Write()
	
# work out what change we need to make to get the pins in a plane parallel to the pads
derivePlaneCorrection(bridge_pins,parameters_pads)

# test the corrected plane residuals (should be consistent with zero)
bridge_pins_corrected = []
for i in range(0,4):
	bridge_pins_corrected.append([bridge_pins[i][0],bridge_pins[i][1],bridge_pins[i][2]+corrections[i]])
parameters_pins_corrected = fitPlaneToPoints(bridge_pins_corrected)
residuals_pins_corrected = makeResidualsHist(bridge_pins_corrected,parameters_pins_corrected,"pins_mid-point")
residuals_pins_corrected.Write()

# make histogram of the bridge heights at this mid-point
hist_bridge_mid = calculateBridgeHeights(bridge_pads,parameters_pins_corrected,"mid-point")
hist_bridge_mid.Write()

# work out how things look at this mid-point
hists_mid = []
for hist in panel_hists:
	histClone = hist.Clone(hist.GetName()+"_mid-point")
	histClone.SetTitle(histClone.GetTitle()+" mid-point")
	histClone.Add(hist_bridge_mid)
	histClone.Add(hist_chip,-1)
	hists_mid.append(histClone)
	histClone.Write()

# get the mean glue thickness from all these histograms hybrid-by-hybrid
h_thickness = ROOT.TH1F("glue_thickness_mid-point","glue thickness mid-point",8,-0.5,7.5)
for i in range(0,8):
	sum = 0.0
	for b in range(0,10):
		sum += hists_mid[i].GetBinContent(b+1)
	mean = sum / 10.
	h_thickness.SetBinContent(i+1,mean)
h_thickness.Write()

# get mean correction for glue thickness and apply it
f_mean = ROOT.TF1("f_mean","pol0")
h_thickness.Fit(f_mean,"Q")
thickness_correction = glueTarget - f_mean.GetParameter(0)
for i in range(0,4):
	corrections[i] += thickness_correction

# test the after correction
bridge_pins_corrected = []
for i in range(0,4):
	bridge_pins_corrected.append([bridge_pins[i][0],bridge_pins[i][1],bridge_pins[i][2]+corrections[i]])
parameters_pins_corrected = fitPlaneToPoints(bridge_pins_corrected)
residuals_pins_corrected = makeResidualsHist(bridge_pins_corrected,parameters_pins_corrected,"pins_after")
residuals_pins_corrected.Write()

# make histogram of the bridge heights at this after calibration
hist_bridge_after = calculateBridgeHeights(bridge_pads,parameters_pins_corrected,"after")
hist_bridge_after.Write()

# work out how things look at this after calibration
hists_after = []
for hist in panel_hists:
	histClone = hist.Clone(hist.GetName()+"_after")
	histClone.SetTitle(histClone.GetTitle()+" after")
	histClone.Add(hist_bridge_after)
	histClone.Add(hist_chip,-1)
	hists_after.append(histClone)
	histClone.Write()

# get the mean glue thickness from all these histograms hybrid-by-hybrid
h_thickness = ROOT.TH1F("glue_thickness_after","glue thickness after",8,-0.5,7.5)
for i in range(0,8):
	sum = 0.0
	for b in range(0,10):
		sum += hists_after[i].GetBinContent(b+1)
	mean = sum / 10.
	h_thickness.SetBinContent(i+1,mean)
h_thickness.Write()

# get mean correction for glue thickness and apply it
f_mean = ROOT.TF1("f_mean","pol0")
h_thickness.Fit(f_mean,"QN")
print
print "FINAL AVERAGE GLUE THICKNESS IS","{:.2f}".format(f_mean.GetParameter(0)),"um"
print
print "HYBRID BREAKDOWN:"
for i in range(0,8):
	hists_after[i].Fit(f_mean,"QN")
	print "HYBRID",i," = ","{:.2f}".format(f_mean.GetParameter(0)),"um"
print
print "FINAL CORRECTIONS REQUIRED ARE:"
for i in range(0,4):
	if corrections[i] < 0.0:
		instructions = "PIN "+str(i)+"  =  "+"{:05.1f}".format(corrections[i]) + " um  =  "
		instructions += "ANTI-CLOCKWISE "
	else:
		instructions = "PIN "+str(i)+"  =   "+"{:04.1f}".format(corrections[i]) + " um  =  "
		instructions += "  CLOCKWISE    "
	instructions += "{:.2f}".format(math.fabs(corrections[i]/micronsPerTurn))+" turns"
	instructions += " = {:.0f} degrees".format(math.fabs(corrections[i]/micronsPerTurn)*360)
	print instructions
print

# make a pretty summary plot
can = ROOT.TCanvas("can","can",1600,1200)
can.cd()

p1 = ROOT.TPad("p1","p1",0.0,0.5,0.5,1.0)
p1.Draw()
p2 = ROOT.TPad("p2","p2",0.5,0.5,1.0,1.0)
p2.Draw()
p3 = ROOT.TPad("p3","p3",0.0,0.0,0.5,0.5)
p3.Draw()
p4 = ROOT.TPad("p4","p4",0.5,0.0,1.0,0.5)
p4.Draw()

p1.cd()
drawBridgeHist(hist_bridge_before)
p2.cd()
drawHybridHist(hists_before)
p3.cd()
drawBridgeHist(hist_bridge_after)
p4.cd()
drawHybridHist(hists_after)

can.Print("bridgeCalibration_panel_"+panelID+"_"+panelDate+"_bridge_"+bridgeID+"_"+method+"_"+bridgeDate+".pdf")

# close the output	
outfile.Close()














