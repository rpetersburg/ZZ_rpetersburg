from ROOT import *
gROOT.LoadMacro('atlasstyle/AtlasStyle.C')
import PlotHiggs
SetAtlasStyle()

deadCanvas = TCanvas('','',0,0,0,0)

higgs = PlotHiggs.PlotHiggs(34)

dataFiles = ['data11','data12']
dataHistogram = TH1F( 'dataHistogram', 'Data Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.setHistogram(dataHistogram, dataFiles)

##mcJetBkgFiles = ['out_redBkg_Comb','out_redBkg_Comb']
##mcJetBkgHistogram = TH1F( 'mcJetBkgHistogram', 'MC Jet Background Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
##higgs.setHistogramJets(mcJetBkgHistogram, mcJetBkgFiles)
##higgs.formatHistogram(mcJetBkgHistogram, kViolet)
mcJetBkgFiles = ['extraFiles/MC11c/ZPlusJetsForShapes/reduxbkg_tree_v2',
                 'extraFiles/MC12a/ZPlusJetsForShapes/reduxbkg_tree_v2']
##mcJetBkgFiles = ['out_redBkg_Comb','out_redBkg_Comb']
mcJetBkgHistogram = TH1F( 'mcJetBkgHistogram', 'MC Jet Background Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit)
higgs.setHistogram(mcJetBkgHistogram, mcJetBkgFiles, 'm4l_constrained', 'weight', ['tree','tree','tree','tree'], [[0.25,0.22,2.8,2.5],[2.54,2.6,5.2,3.2]])
higgs.formatHistogram(mcJetBkgHistogram, kViolet)

mcZZBkgFiles = ['mc11_ZZComb','mc12_ZZComb']
mcZZBkgHistogram = TH1F( 'mcZZBkgHistogram', 'MC ZZ Background Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.setHistogram(mcZZBkgHistogram, mcZZBkgFiles)
higgs.formatHistogram(mcZZBkgHistogram, kRed)

mcSignalFiles = ['mc11_signalComb','mc12_signalComb']
mcSignalHistogram = TH1F( 'mcSignalHistogram', 'MC Signal Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.setHistogram(mcSignalHistogram, mcSignalFiles)
higgs.formatHistogram(mcSignalHistogram, kCyan)

histogramList = [dataHistogram, mcJetBkgHistogram, mcZZBkgHistogram, mcSignalHistogram]
histogramNames = ['Experimental Data', 'MC Background Z+jets, t#bar{t}', 'MC Background ZZ^{(*)}', 'MC Signal (m_{H} = 125 GeV)']
histogramOptions = ['pe','f','f','f']

higgs.drawCombinedHistogram(histogramList,histogramNames, histogramOptions, 'combinedGraphs/HiggsNoFit', higgs.axesLabel)

