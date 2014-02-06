from ROOT import *
gROOT.LoadMacro('atlasstyle/AtlasStyle.C')
import PlotHiggs
import math
SetAtlasStyle()

deadCanvas = TCanvas('','',0,0,0,0)

higgsObjects = [PlotHiggs.PlotHiggs(12, -3.14159, 3.14159, 0.05, 12),PlotHiggs.PlotHiggs(12, -1, 1, 0.05, 12)]
labels = [higgsObjects[0].phiLabel, higgsObjects[0].cosThetaLabel]
angles = ['phi', 'cth1']

for index, higgs in enumerate(higgsObjects):

    dataFiles = ['data11','data12']
    dataHistogram = TH1F( 'dataSpinHistogram'+angles[index], 'Data Spin Histogram '+angles[index], higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
    higgs.setHistogramWithChain(dataHistogram, dataFiles, angles[index], 'abs(weight)*(m4l_constrained<130 && m4l_constrained>115)')

    mcJetBkgFiles = ['out_redBkg_Comb','out_redBkg_Comb']
    mcJetBkgHistogram = TH1F( 'mcJetBkgSpinHistogram'+angles[index], 'MC Jet Spin Background Histogram '+angles[index], higgs.nBins, higgs.lowerLimit, higgs.upperLimit)
    higgs.setHistogram(mcJetBkgHistogram, mcJetBkgFiles, angles[index], 'abs(weight)*(m4l_constrained<130 && m4l_constrained>115)')
    higgs.formatHistogram(mcJetBkgHistogram, kViolet, 3.92)

    mcZZBkgFiles = ['mc11_ZZComb','mc12_ZZComb']
    mcZZBkgHistogram = TH1F( 'mcZZBkgSpinHistogram'+angles[index], 'MC ZZ Background Spin Histogram '+angles[index], higgs.nBins, higgs.lowerLimit, higgs.upperLimit)
    higgs.setHistogram(mcZZBkgHistogram, mcZZBkgFiles, angles[index], 'abs(weight)*(m4l_constrained<130 && m4l_constrained>115)')
    higgs.formatHistogram(mcZZBkgHistogram, kRed)

    mcSignalFiles = ['mc11_signalComb','mc12_signalComb']
    mcSignalHistogram = TH1F( 'mcSignalSpinHistogram'+angles[index], 'MC Signal Spin Histogram '+angles[index], higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
    higgs.setHistogram(mcSignalHistogram, mcSignalFiles, angles[index], 'abs(weight)*(m4l_constrained<130 && m4l_constrained>115)')
    higgs.formatHistogram(mcSignalHistogram, kCyan)

    histogramList = [dataHistogram, mcJetBkgHistogram, mcZZBkgHistogram, mcSignalHistogram]
    histogramNames = ['Experimental Data', 'MC Background Z+jets','MC Background ZZ^{(*)}', 'MC Signal (m_{H} = 125 GeV)']
    histogramOptions = ['pe','f','f','f']

    higgs.drawCombinedHistogram(histogramList,histogramNames, histogramOptions, 'combinedGraphs/HiggsSpin'+angles[index], labels[index])


