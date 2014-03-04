from ROOT import *
gROOT.LoadMacro('atlasstyle/AtlasStyle.C')
import PlotHiggs
import math
##SetAtlasStyle()

##deadCanvas = TCanvas('','',0,0,0,0)

higgs = PlotHiggs.PlotHiggs(36)

channels = ['tree_incl_4mu','tree_incl_2mu2e','tree_incl_2e2mu','tree_incl_4e']

##dataFiles = ['data11','data12']
dataFiles = ['mc11_signalComb','mc12_signalComb']
dataHistogram = TH1F( 'dataHistogram', 'Data Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
chain = TChain('dataChain', 'Data Chain')

for fileName in dataFiles:
    for channel in channels:
        chain.Add(higgs.dir+fileName+'.root/'+channel)

scatterPlot = TH2F( 'scatterPlot', 'Scatter Plot', higgs.nBins, 80, 170, higgs.nBins, 0, 30)

for event in chain:
    value = event.__getattr__('m4l_constrained')
    print value
    scatterPlot.Fill(value, chain.GetEntries('m4l_constrained > '+str(value-1.0)+' && m4l_constrained < '+str(value+1.0)))

canvas = TCanvas('Test', 'Test', 0, 0, 1000, 800)
canvas.cd()
scatterPlot.Draw('escat')

                    

