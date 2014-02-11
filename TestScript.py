from ROOT import *
gROOT.LoadMacro('atlasstyle/AtlasStyle.C')
gROOT.LoadMacro('atlasstyle/AtlasLabels.C')
import PlotHiggs
SetAtlasStyle()

dir11 = "C:/Users/ryanrp/Documents/CERN/analysis/ZZ_new/checkPlots/ZZ/ZZ/v02/MC11c/"
dir12 = "C:/Users/ryanrp/Documents/CERN/analysis/ZZ_new/checkPlots/ZZ/ZZ/v02/MC12a/"
## Hist Info
nBin = 36
uprLim = 170
lwrLim = 80
label = ";m_{4l} [GeV]; Events/2.5GeV"

nZZJetsFile = 2

ZZJetsFile = [dir12 + "ZPlusJetsForShapes/reduxbkg_tree_v2.root",
              dir11 + "ZPlusJetsForShapes/reduxbkg_tree_v2.root"]

## Reading the file and filling the TTree with that data
zzJetsMCBkgFile = [0,0]
zzJetsMCBkg = [0,0]
for i in xrange(nZZJetsFile):
    zzJetsMCBkgFile[i] = TFile(ZZJetsFile[i], "read")
    zzJetsMCBkg[i] = zzJetsMCBkgFile[i].Get("tree")

## Plotting the Z+Jets MC
## New Canvas
c10 = TCanvas ("c10", "Z+jets TTbar MC", 0, 0, 600, 600)
c10.cd()

## Array of histrogram
zzJetsMCBkgHist = [[0,0,0,0],[0,0,0,0]]
zzJetsMCBkgSum = TH1F ("zzJetsMCBkgSum", "Background Z+Jets TTbar"+label, nBin, lwrLim, uprLim)
zzJetsMCBkgSumCh = [0,0,0,0]
zzNorm = [2.4, 2.5, 5.2, 3.2, 0.22, 0.22, 2.8, 2.5]

## Init the histogram and filling the data
for j in xrange(4):
    zzJetsMCBkgSumCh[j] = TH1F ("zzJetsMCBkgSum"+str(j), "Background Z+Jets TTbar"+str(j)+label, nBin, lwrLim, uprLim)
    for i in xrange(nZZJetsFile):
        zzJetsMCBkgHist[i][j] = TH1F ("zzJetsMCBkgHist"+str(i)+str(j), ZZJetsFile[i]+label, nBin, lwrLim, uprLim)
        
        zzJetsMCBkg[i].Draw("m4l_constrained>>zzJetsMCBkgHist"+str(i)+str(j), "weight")
        
        zzJetsMCBkgHist[i][j].Scale(zzNorm[i*4 + j]/zzJetsMCBkgHist[i][j].Integral())
        zzJetsMCBkgSumCh[j].Add(zzJetsMCBkgHist[i][j])
    zzJetsMCBkgSum.Add(zzJetsMCBkgSumCh[j]);
##                Saving the file
##//			c2->SaveAs("Plots/zzJetsBkg"+nHist[i]+nHist[j]+".pdf");
zzJetsMCBkgSum.SetFillColor(kGreen)
##zzJetsMCBkgSum.SetStats(0)
zzJetsMCBkgSum.Draw()
