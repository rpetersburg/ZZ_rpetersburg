from ROOT import *
gROOT.LoadMacro('atlasstyle/AtlasStyle.C')
import PlotHiggs
SetAtlasStyle()

deadCanvas = TCanvas('','',0,0,0,0)

higgs = PlotHiggs.PlotHiggs(36, 80, 170, 0.05, 25)

mcJetBkgFiles = ['out_redBkg_Comb','out_redBkg_Comb']
mcJetBkgHistogram = TH1F( 'mcJetBkgHistogram', 'MC Jet Background Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.setHistogramJets(mcJetBkgHistogram, mcJetBkgFiles)
higgs.formatHistogram(mcJetBkgHistogram, kViolet)

mcZZBkgFiles = ['mc11_ZZComb','mc12_ZZComb']
mcZZBkgHistogram = TH1F( 'mcZZBkgHistogram', 'MC ZZ Background Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.setHistogram(mcZZBkgHistogram, mcZZBkgFiles)
higgs.formatHistogram(mcZZBkgHistogram, kRed)

mcSignalFiles = ['mc11_signalComb','mc12_signalComb']
mcSignalHistogram = TH1F( 'mcSignalHistogram', 'MC Signal Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.setHistogram(mcSignalHistogram, mcSignalFiles)
higgs.formatHistogram(mcSignalHistogram, kCyan)

histogramList = [mcJetBkgHistogram, mcZZBkgHistogram, mcSignalHistogram]

mcHistogram = TH1F( 'mcHistogram', 'MC Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.combineHistograms(mcHistogram, histogramList)

fitHighMass = TF1('fitHighMass', 'gaus', 120,130)
fitLowMass = TF1('fitLowMass', 'gaus', 80, 100)
fitOtherBkg = TF1('fitOtherBkg', 'gaus', higgs.lowerLimit, higgs.upperLimit)

fitMC = TF1('fitMC', 'gaus(0)+gaus(3)+gaus(6)', higgs.lowerLimit, higgs.upperLimit)

higgs.fitHistogram(mcHistogram, fitMC, [], [fitHighMass, fitLowMass])

higgs.drawHistogram(mcHistogram, 'e', '4l', '', 'combinedGraphs/mcHistogram', higgs.axesLabel)

# Print all relevant data from fit function
fitMC.SetParNames('Higgs Amplitude', 'Higgs Mass', 'Higgs #sigma', 'Z Amplitude', 'Z Mass', 'Z #sigma', 'Bkg Amplitude', 'Bkg Mass', 'Bkg #sigma')
for i in xrange(9):
    print str(fitMC.GetParName(i)) + ':   ' + str(fitMC.GetParameter(i))






