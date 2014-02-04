from ROOT import *
gROOT.LoadMacro('atlasstyle/AtlasStyle.C')
import PlotHiggs
SetAtlasStyle()

higgs = PlotHiggs.PlotHiggs(32, 80, 170, 0.05, 25)

dataFiles = ['data11','data12']
dataHistogram = TH1F( 'dataHistogram', 'Data Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.setHistogram(dataHistogram, dataFiles)

mcJetBkgFiles = ['out_redBkg_Comb','out_redBkg_Comb']
mcJetBkgHistogram = TH1F( 'mcJetBkgHistogram', 'MC Jet Background Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit)
higgs.setHistogramJets(mcJetBkgHistogram, mcJetBkgFiles)
higgs.formatHistogram(mcJetBkgHistogram, kViolet)

mcZZBkgFiles = ['mc11_ZZComb','mc12_ZZComb']
mcZZBkgHistogram = TH1F( 'mcZZBkgHistogram', 'MC ZZ Background Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit)
higgs.setHistogram(mcZZBkgHistogram, mcZZBkgFiles)
higgs.formatHistogram(mcZZBkgHistogram, kRed)

mcSignalFiles = ['mc11_signalComb','mc12_signalComb']
mcSignalHistogram = TH1F( 'mcSignalHistogram', 'MC Signal Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.setHistogram(mcSignalHistogram, mcSignalFiles)
higgs.formatHistogram(mcSignalHistogram, kCyan)

# Create a combined fit function
combinedFit = TF1('fitAllData', 'gaus(0)+gaus(3)+gaus(6)', higgs.lowerLimit, higgs.upperLimit)

higgs.fitHistogram(dataHistogram, combinedFit, [13, 125, 1.7, 12.05, 90.35, 2.4, 2.2, 137, 39])
##higgs.fitHistogram(dataHistogram, combinedFit, [16.2, 124.4, 2.1, 13.3, 90.3, 2.7, 2.6, 120.4, 95.2])
##higgs.fitHistogram(dataHistogram, combinedFit, [5,130,5])

histogramList = [dataHistogram, mcJetBkgHistogram, mcZZBkgHistogram, mcSignalHistogram]
histogramNames = ['Experimental Data', 'MC Background Z+jets, t#bar{t}', 'MC Background ZZ^{(*)}', 'MC Signal (m_{H} = 125 GeV)']
histogramOptions = ['pe','f','f','f']

higgs.drawCombinedHistogram(histogramList,histogramNames, histogramOptions, 'combinedGraphs/HiggsWithFit2')
