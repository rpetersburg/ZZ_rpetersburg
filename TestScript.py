from ROOT import *
gROOT.LoadMacro('atlasstyle/AtlasStyle.C')
gROOT.LoadMacro('atlasstyle/AtlasLabels.C')

SetAtlasStyle()

nBins = 34
lowerLimit = 80
upperLimit = 250
titleOffset = 0.05
maxY = 35

jetHistogram = TH1F( 'mcJetBkgHistogram', 'MC Jet Background Histogram', nBins, lowerLimit, upperLimit)

channels = ['tree_incl_4mu','tree_incl_2mu2e','tree_incl_2e2mu','tree_incl_4e']

rootFileNames = ['out_redBkg_Comb','out_redBkg_Comb']

jetFile = TFile("C:/Users/ryanrp/Documents/CERN/analysis/ZZ_rpetersburg/rootFiles/redBkg_smoothed.root", "read")

eeHistogram = jetFile.Get('Reducible_bkg_1D_llee_0')
mmHistogram = jetFile.Get('Reducible_bkg_1D_llmumu_0')

normNumber = [[1.3,0.97,1.33,0.67],[0.13,0.52,0.107,0.52]]

testCanvas = TCanvas('test','test',0,0,1000,800)
testCanvas.Divide(4,2)

for yearIndex, fileName in enumerate(rootFileNames):
    for channelIndex, channel in enumerate(channels):
        testCanvas.cd(4*yearIndex+channelIndex+1)
        currentHistogramName = fileName+'_'+channel
        currentHistogram = TH1F( currentHistogramName, currentHistogramName, nBins, lowerLimit, upperLimit)
        for k in xrange(mmHistogram.GetNbinsX()):
            if channelIndex%2 == 0:
                currentHistogram.Fill(mmHistogram.GetBinCenter(k), mmHistogram.GetBinContent(k))
##                print mmHistogram.GetBinCenter(k), mmHistogram.GetBinContent(k)
            else:
                currentHistogram.Fill(eeHistogram.GetBinCenter(k)+0.01, eeHistogram.GetBinContent(k))
        currentHistogram.Draw()
        currentHistogram.Scale(normNumber[yearIndex][channelIndex]/currentHistogram.Integral())
        print currentHistogram.Integral()
        jetHistogram.Add(currentHistogram)
testCanvas.Update()
testCanvas.SaveAs('test.png')

