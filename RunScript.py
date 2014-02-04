from ROOT import *
gROOT.LoadMacro('atlasstyle/AtlasStyle.C')
gROOT.LoadMacro('atlasstyle/AtlasLabels.C')
from PlotHiggs import *

app = PlotHiggs()
SetAtlasStyle()

dataFiles = ['data11','data12']
dataHistogram = app.getHistogram(dataFiles, 'dataHistogram', 'Data Histogram')

mcSignalFiles = ['mc11_signalComb','mc12_signalComb']
mcSignalHistogram = app.getHistogram(mcSignalFiles, 'mcSignalHistogram', 'MC Signal Histogram')
print dataHistogram, mcSignalHistogram
app.formatHistogram(mcSignalHistogram, kCyan)

histogramNames = ['Experimental Data', 'MC Signal (m_{H} = 125 GeV)']
histogramOptions = ['pe','f']

histogramList = [dataHistogram, mcSignalHistogram]
print histogramList

app.drawCombinedHistogram(histogramList,histogramNames, histogramOptions)
