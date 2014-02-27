from ROOT import *
gROOT.LoadMacro('atlasstyle/AtlasStyle.C')
import PlotHiggs
import math
SetAtlasStyle()

deadCanvas = TCanvas('','',0,0,0,0)

higgs = PlotHiggs.PlotHiggs(36, 80, 170, 0.05, 25)

dataFiles = ['data11','data12']
dataHistogram = TH1F( 'dataHistogram', 'Data Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.setHistogram(dataHistogram, dataFiles)

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

mcBkgHistogram = TH1F( 'mcBkgHistogram', 'MC Background Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit)
higgs.combineHistograms(mcBkgHistogram, [mcZZBkgHistogram, mcJetBkgHistogram], [1,1])

# Fitting the experimental data

# Create the fit functions
fitHiggs = TF1('fitHiggs', 'gaus', 120, 130)
fitZMass = TF1('fitZMass', 'gaus', 80, 106)
fitOtherBkg = TF1('fitOtherBkg', 'gaus', 106, higgs.upperLimit)
# Create a combined fit function
fitAllData = TF1('fitAllData', 'gaus(0)+gaus(3)+gaus(6)', higgs.lowerLimit, higgs.upperLimit)

higgs.fitHistogram(dataHistogram, fitAllData, [], [fitHiggs,fitZMass,fitOtherBkg])

higgs.drawHistogram(dataHistogram, 'e', '4l', '', 'fitGraphs/fitHiggs', higgs.axesLabel, fitHiggs)
higgs.drawHistogram(dataHistogram, 'e', '4l', '', 'fitGraphs/fitZMass', higgs.axesLabel, fitZMass)
higgs.drawHistogram(dataHistogram, 'e', '4l', '', 'fitGraphs/fitOtherBkg', higgs.axesLabel, fitOtherBkg)

histogramList = [dataHistogram, mcJetBkgHistogram, mcZZBkgHistogram, mcSignalHistogram]
histogramNames = ['Experimental Data', 'MC Background Z+jets, t#bar{t}', 'MC Background ZZ^{(*)}', 'MC Signal (m_{H} = 125 GeV)']
histogramOptions = ['pe','f','f','f']

higgs.drawCombinedHistogram(histogramList, histogramNames, histogramOptions, 'combinedGraphs/HiggsWithFit', higgs.axesLabel, fitAllData)

# Print all relevant data from fit function
parameterNames = ['Higgs Amplitude', 'Higgs Mass', 'Higgs #sigma', 'Z Amplitude', 'Z Mass', 'Z #sigma']
for index in xrange(6):
    fitAllData.SetParName(index, parameterNames[index])
print 'Experimental Data Fit Results'
for i in xrange(6):
    print str(fitAllData.GetParName(i)) + ':   ' + str(round(10*fitAllData.GetParameter(i))/10)


# Fitting the simulated data

# Create the fit functions
fitMCSignal = TF1('fitMCSignal', 'gaus', 120, 130)
fitMCZMass = TF1('fitMCZMass', 'gaus', higgs.lowerLimit, 106)
fitMCOtherBkg = TF1('fitMCOtherBkg', 'gaus', 106, higgs.upperLimit)
# Combined
fitMC = TF1('fitMC', 'gaus(0)+gaus(3)+gaus(6)', higgs.lowerLimit, higgs.upperLimit)

higgs.fitHistogram(mcSignalHistogram, fitMCSignal)
higgs.drawHistogram(mcSignalHistogram, 'e', '4l', '', 'fitGraphs/fitMCSignal', higgs.axesLabel, fitMCSignal)

higgs.fitHistogram(mcZZBkgHistogram, fitMCZMass)
higgs.drawHistogram(mcZZBkgHistogram, 'e', '4l', '', 'fitGraphs/fitMCZMass', higgs.axesLabel, fitMCZMass)

higgs.fitHistogram(mcBkgHistogram, fitMCOtherBkg)
higgs.drawHistogram(mcBkgHistogram, 'e', '4l', '', 'fitGraphs/fitMCOtherBkg', higgs.axesLabel, fitMCOtherBkg)

mcHistogram = TH1F( 'mcHistogram', 'MC Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.combineHistograms(mcHistogram, [mcJetBkgHistogram, mcZZBkgHistogram, mcSignalHistogram])
higgs.fitHistogram(mcHistogram, fitMC, [], [fitMCSignal, fitMCZMass, fitMCOtherBkg])
higgs.drawHistogram(mcHistogram, 'e', '4l', '', 'combinedGraphs/mcHistogram', higgs.axesLabel, fitMC)

# Print all relevant data from fit function
parameterNames = ['Higgs Amplitude', 'Higgs Mass', 'Higgs #sigma', 'Z Amplitude', 'Z Mass', 'Z #sigma']
for index in xrange(6):
    fitMC.SetParName(index, parameterNames[index])
print '\nSimulation Data Fit Results'
for i in xrange(6):
    print str(fitMC.GetParName(i)) + ':   ' + str(round(10*fitMC.GetParameter(i))/10)



simulationHiggsMass = round(10*fitMC.GetParameter(1))/10
simulationHiggsError = math.ceil(10*fitMC.GetParameter(2)/math.sqrt(28))/10

experimentalHiggsMass = round(10*fitAllData.GetParameter(1))/10
experimentalHiggsError = math.ceil(10*fitAllData.GetParameter(2)/math.sqrt(32))/10

print
print 'Experimental Higgs Mass:', str(experimentalHiggsMass), u'\u00B1', str(experimentalHiggsError), 'GeV'
print 'Simulation Higgs Mass:', str(simulationHiggsMass), u'\u00B1', str(simulationHiggsError), 'GeV'


signalStrength = round(10*fitAllData.GetParameter(0)/fitMC.GetParameter(0))/10
signalStrengthError = round(10*signalStrength*(1/math.sqrt(fitAllData.GetParameter(0))+1/math.sqrt(fitMC.GetParameter(0))))/10
print 'Signal Strength:', str(signalStrength), u'\u00B1', str(signalStrengthError)











