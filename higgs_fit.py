from ROOT import *
gROOT.LoadMacro('atlasstyle/AtlasStyle.C')
import PlotHiggs
SetAtlasStyle()

higgs = PlotHiggs.PlotHiggs(34, 80, 170, 0.05, 28)

dataFiles = ['data11','data12']
dataHistogram = TH1F( 'dataHistogram', 'Data Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit)
higgs.setHistogram(dataHistogram, dataFiles)

##fitFunction = TF1('fitFunction',PlotHiggs.LorentzianFit(),80.,170.,3)
fitFunction = TF1('fitFunction', 'gaus', 80., 170.)

dataHistogram.Fit(fitFunction)

par = fitFunction.GetParameters()
print par[0], par[1], par[2], par[3]

higgs.drawHistogram(dataHistogram)
