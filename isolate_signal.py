from ROOT import *
gROOT.LoadMacro('atlasstyle/AtlasStyle.C')
import PlotHiggs
SetAtlasStyle()

deadCanvas = TCanvas('','',0,0,0,0)
deadCanvas.cd()

higgs = PlotHiggs.PlotHiggs(36, 80, 170, 0.05, 25)

dataFiles = ['data11','data12']
dataHistogram = TH1F( 'dataHistogram', 'Data Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.setHistogram(dataHistogram, dataFiles)

mcJetBkgFiles = ['out_redBkg_Comb','out_redBkg_Comb']
mcJetBkgHistogram = TH1F( 'mcJetBkgHistogram', 'MC Jet Background Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.setHistogramJets(mcJetBkgHistogram, mcJetBkgFiles)
higgs.formatHistogram(mcJetBkgHistogram, kViolet)

mcZZBkgFiles = ['mc11_ZZComb','mc12_ZZComb']
mcZZBkgHistogram = TH1F( 'mcZZBkgHistogram', 'MC ZZ Background Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.setHistogram(mcZZBkgHistogram, mcZZBkgFiles)
higgs.formatHistogram(mcZZBkgHistogram, kRed)

dataSignalHistogram = TH1F('dataSignalHistogram', 'dataSignalHistogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit)
dataSignalHistogram.Add(dataHistogram)

higgs.combineHistograms(dataSignalHistogram, [mcJetBkgHistogram, mcZZBkgHistogram], -1)

fitSignal = TF1('fitSignal', 'gaus', 120, 130)

higgs.fitHistogram(dataSignalHistogram, fitSignal, [12, 125, 2])

histogramNames = ['Experimental Data - MC Background']
histogramOptions = ['pe']

higgs.drawHistogram(dataSignalHistogram, 'e', '4l', '', 'combinedGraphs/dataSignal')




