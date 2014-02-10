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
##mcJetBkgFiles = ['out_redBkg_Comb','out_redBkg_Comb']
mcJetBkgHistogram = TH1F( 'mcJetBkgHistogram', 'MC Jet Background Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit)
higgs.setHistogram(mcJetBkgHistogram, mcJetBkgFiles, 'm4l_constrained', 'weight', ['tree'], [[0.22+0.03,0.19,0.03,2.8,2.5],[2.4+0.14,2.5+0.1,5.2,3.2]])
higgs.formatHistogram(mcJetBkgHistogram, kViolet)

mcZZBkgFiles = ['mc11_ZZComb','mc12_ZZComb']
mcZZBkgHistogram = TH1F( 'mcZZBkgHistogram', 'MC ZZ Background Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.setHistogram(mcZZBkgHistogram, mcZZBkgFiles)
higgs.formatHistogram(mcZZBkgHistogram, kRed)

mcSignalFiles = ['mc11_signalComb','mc12_signalComb']
mcSignalHistogram = TH1F( 'mcSignalHistogram', 'MC Signal Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.setHistogram(mcSignalHistogram, mcSignalFiles)
higgs.formatHistogram(mcSignalHistogram, kCyan)

# Fitting the experimental data

# Create the fit functions
fitHiggs = TF1('fitHiggs', 'gaus', 120, 130)
fitZBkg = TF1('fitZBkg', 'gaus', 80, 100)
fitOtherBkg = TF1('fitOtherBkg', 'gaus', higgs.lowerLimit, higgs.upperLimit)

# Create a combined fit function
fitAllData = TF1('fitAllData', 'gaus(0)+gaus(3)+gaus(6)', higgs.lowerLimit, higgs.upperLimit)

higgs.fitHistogram(dataHistogram, fitAllData, [], [fitHiggs,fitZBkg,fitOtherBkg])

histogramList = [dataHistogram, mcJetBkgHistogram, mcZZBkgHistogram, mcSignalHistogram]
histogramNames = ['Experimental Data', 'MC Background Z+jets, t#bar{t}', 'MC Background ZZ^{(*)}', 'MC Signal (m_{H} = 125 GeV)']
histogramOptions = ['pe','f','f','f']

higgs.drawCombinedHistogram(histogramList,histogramNames, histogramOptions, 'combinedGraphs/HiggsWithFit', higgs.axesLabel)

# Print all relevant data from fit function
fitAllData.SetParNames('Higgs Amplitude', 'Higgs Mass', 'Higgs #sigma', 'Z Amplitude', 'Z Mass', 'Z #sigma', 'Bkg Amplitude', 'Bkg Mass', 'Bkg #sigma')
print 'Experimental Data Fit Results'
for i in xrange(9):
    print str(fitAllData.GetParName(i)) + ':   ' + str(fitAllData.GetParameter(i))


# Fitting the simulated data

histogramList = [mcJetBkgHistogram, mcZZBkgHistogram, mcSignalHistogram]

mcHistogram = TH1F( 'mcHistogram', 'MC Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.combineHistograms(mcHistogram, histogramList)

fitHighMass = TF1('fitHighMass', 'gaus', 120,130)
fitLowMass = TF1('fitLowMass', 'gaus', 80, 100)
fitOtherBkg = TF1('fitOtherBkg', 'gaus', higgs.lowerLimit, higgs.upperLimit)

fitMC = TF1('fitMC', 'gaus(0)+gaus(3)+gaus(6)', higgs.lowerLimit, higgs.upperLimit)

higgs.fitHistogram(mcHistogram, fitMC, [], [fitHighMass, fitLowMass, fitOtherBkg])

higgs.drawHistogram(mcHistogram, 'e', '4l', '', 'combinedGraphs/mcHistogram', higgs.axesLabel)

# Print all relevant data from fit function
fitMC.SetParNames('Higgs Amplitude', 'Higgs Mass', 'Higgs #sigma', 'Z Amplitude', 'Z Mass', 'Z #sigma', 'Bkg Amplitude', 'Bkg Mass', 'Bkg #sigma')
print '\nSimulation Data Fit Results'
for i in xrange(9):
    print str(fitMC.GetParName(i)) + ':   ' + str(fitMC.GetParameter(i))



