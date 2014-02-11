from ROOT import *
gROOT.LoadMacro('atlasstyle/AtlasStyle.C')
import PlotHiggs
SetAtlasStyle()

deadCanvas = TCanvas('','',0,0,0,0)

higgs = PlotHiggs.PlotHiggs(36, 80, 170, 0.05, 25)

dataFiles = ['data11','data12']
dataHistogram = TH1F( 'dataHistogram', 'Data Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.setHistogram(dataHistogram, dataFiles)

##mcJetBkgFiles = ['out_redBkg_Comb','out_redBkg_Comb']
##mcJetBkgHistogram = TH1F( 'mcJetBkgHistogram', 'MC Jet Background Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
##higgs.setHistogramJets(mcJetBkgHistogram, mcJetBkgFiles)
##higgs.formatHistogram(mcJetBkgHistogram, kViolet)
mcJetBkgFiles = ['extraFiles/MC11c/ZPlusJetsForShapes/reduxbkg_tree_v2',
                 'extraFiles/MC12a/ZPlusJetsForShapes/reduxbkg_tree_v2']
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

dataSignalHistogram = TH1F('dataSignalHistogram', 'Data Signal Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.combineHistograms(dataSignalHistogram, [dataHistogram, mcZZBkgHistogram, mcJetBkgHistogram], [1,-1,-1])

dataZZBkgHistogram = TH1F( 'dataZZBkgHistogram', 'Data ZZ Background Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit)
higgs.combineHistograms(dataZZBkgHistogram, [dataHistogram, mcSignalHistogram, mcJetBkgHistogram], [1,-1,-1])

dataJetBkgHistogram = TH1F( 'dataJetBkgHistogram', 'Data Jet Background Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit)
higgs.combineHistograms(dataJetBkgHistogram, [dataHistogram, mcSignalHistogram, mcZZBkgHistogram], [1,-1,-1])

# Fitting the experimental data

# Create the fit functions
fitHiggs = TF1('fitHiggs', 'gaus', 120, 130)
fitZBkg = TF1('fitZBkg', 'gaus(0)+pol3(3)', higgs.lowerLimit, higgs.upperLimit)
fitZMass = TF1('fitZMass', 'gaus', higgs.lowerLimit, 106)
fitZOtherBkg = TF1('fitZOtherBkg', 'pol3', 106, higgs.upperLimit)
fitJetBkg = TF1('fitJetBkg', 'pol3', higgs.lowerLimit, higgs.upperLimit)
# Create a combined fit function
fitAllData = TF1('fitAllData', 'gaus(0)+gaus(3)+pol3(6)+pol3(10)', higgs.lowerLimit, higgs.upperLimit)

higgs.fitHistogram(dataSignalHistogram, fitHiggs, [])
higgs.drawHistogram(dataSignalHistogram, 'e', '4l', '', 'combinedGraphs/dataSignalHistogram', higgs.axesLabel, fitHiggs)

higgs.fitHistogram(dataZZBkgHistogram, fitZBkg, [], [fitZMass, fitZOtherBkg])
higgs.drawHistogram(dataZZBkgHistogram, 'e', '4l', '', 'combinedGraphs/dataZZBkgHistogram', higgs.axesLabel, fitZBkg)

higgs.fitHistogram(dataJetBkgHistogram, fitJetBkg, [])
higgs.drawHistogram(dataJetBkgHistogram, 'e', '4l', '', 'combinedGraphs/dataJetBkgHistogram', higgs.axesLabel, fitJetBkg)

higgs.fitHistogram(dataHistogram, fitAllData, [], [], [fitHiggs,fitZBkg,fitJetBkg])

histogramList = [dataHistogram, mcJetBkgHistogram, mcZZBkgHistogram, mcSignalHistogram]
histogramNames = ['Experimental Data', 'MC Background Z+jets, t#bar{t}', 'MC Background ZZ^{(*)}', 'MC Signal (m_{H} = 125 GeV)']
histogramOptions = ['pe','f','f','f']

higgs.drawCombinedHistogram(histogramList, histogramNames, histogramOptions, 'combinedGraphs/HiggsWithFit', higgs.axesLabel, fitAllData)

# Print all relevant data from fit function
parameterNames = ['Higgs Amplitude', 'Higgs Mass', 'Higgs #sigma', 'Z Amplitude', 'Z Mass', 'Z #sigma', 'Z Bkg Amplitude', 'Z Bkg Mass', 'Z Bkg #sigma']
for index in xrange(9):
    fitAllData.SetParName(index, parameterNames[index])
print 'Experimental Data Fit Results'
for i in xrange(9):
    print str(fitAllData.GetParName(i)) + ':   ' + str(fitAllData.GetParameter(i))


# Fitting the simulated data

# Create the fit functions
fitMCSignal = TF1('fitMCSignal', 'gaus', 120, 130)
fitMCZBkg = TF1('fitMCZBkg', 'gaus(0)+pol3(3)', higgs.lowerLimit, higgs.upperLimit)
fitMCZMass = TF1('fitMCZMass', 'gaus', higgs.lowerLimit, 106)
fitMCZOtherBkg = TF1('fitMCZOtherBkg', 'pol3', 106, higgs.upperLimit)
fitMCJetBkg = TF1('fitMCJetBkg', 'pol3', higgs.lowerLimit, higgs.upperLimit)
# Combined
fitMC = TF1('fitMC', 'gaus(0)+gaus(3)+pol3(6)+pol3(10)', higgs.lowerLimit, higgs.upperLimit)

higgs.fitHistogram(mcSignalHistogram, fitMCSignal, [])
higgs.drawHistogram(mcSignalHistogram, 'e', '4l', '', 'combinedGraphs/mcSignalHistogram', higgs.axesLabel, fitMCSignal)

higgs.fitHistogram(mcZZBkgHistogram, fitMCZBkg, [], [fitMCZMass, fitMCZOtherBkg])
higgs.drawHistogram(mcZZBkgHistogram, 'e', '4l', '', 'combinedGraphs/mcZZBkgHistogram', higgs.axesLabel, fitMCZBkg)

higgs.fitHistogram(mcJetBkgHistogram, fitMCJetBkg, [])
higgs.drawHistogram(mcJetBkgHistogram, 'e', '4l', '', 'combinedGraphs/mcJetBkgHistogram', higgs.axesLabel, fitMCJetBkg)

mcHistogram = TH1F( 'mcHistogram', 'MC Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.combineHistograms(mcHistogram, [mcJetBkgHistogram, mcZZBkgHistogram, mcSignalHistogram])
higgs.fitHistogram(mcHistogram, fitMC, [], [], [fitMCSignal, fitMCZBkg, fitMCJetBkg])
higgs.drawHistogram(mcHistogram, 'e', '4l', '', 'combinedGraphs/mcHistogram', higgs.axesLabel, fitMC)

# Print all relevant data from fit function
parameterNames = ['Higgs Amplitude', 'Higgs Mass', 'Higgs #sigma', 'Z Amplitude', 'Z Mass', 'Z #sigma', 'Z Bkg Amplitude', 'Z Bkg Mass', 'Z Bkg #sigma']
for index in xrange(9):
    fitMC.SetParName(index, parameterNames[index])
print '\nSimulation Data Fit Results'
for i in xrange(9):
    print str(fitMC.GetParName(i)) + ':   ' + str(fitMC.GetParameter(i))







