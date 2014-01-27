from ROOT import gROOT
gROOT.LoadMacro("atlasstyle/AtlasStyle.C")
gROOT.LoadMacro("atlasstyle/AtlasLabels.C")
from ROOT import *

# Setting Global Variable for Histograms
nBins = 32
lowerLimit = 80
upperLimit = 250
titleOffset = 0.35

def drawHistogram(histogram, channelTextSize, leptonChannel, luminosityTextSize, luminosityString1,luminosityString2 = False):
    # Draw the Histogram with error bars
    histogram.Draw('E')
    
    # Add titles to the histogram axes
    histogram.GetXaxis().SetTitle("m_{4l}[GeV]")
    histogram.GetYaxis().SetTitle("Events/2.5GeV")
    
    # Get values for the min and max y values on the graph
    gPad.Update()
    maxY = gPad.GetFrame().GetY2()
    minY = gPad.GetFrame().GetY1()
    
    # Draw the latex titles
    latex = TLatex()
    latex.SetTextAlign(12)
    # Title designating the lepton channel
    latex.SetTextSize(channelTextSize)
    latex.DrawLatex(titleOffset*upperLimit+(1-titleOffset)*lowerLimit, maxY*0.83, "H #rightarrow ZZ^{(*)} #rightarrow " + leptonChannel)
    # Title(s) designating the year(s) (luminosity)
    latex.SetTextSize(luminosityTextSize)
    latex.DrawLatex(titleOffset*upperLimit+(1-titleOffset)*lowerLimit, maxY*0.7, luminosityString1)
    if luminosityString2:
        latex.DrawLatex(titleOffset*upperLimit+(1-titleOffset)*lowerLimit, maxY*0.6, luminosityString2)
    # Draw the Atlas Label
    ATLASLabel(.4,0.875,'Work in Progress',1)

def plotData_rpetersburg():
    SetAtlasStyle()

    # Lists of strings for channels and data years
    channels = ['tree_incl_4mu','tree_incl_2mu2e','tree_incl_2e2mu','tree_incl_4e']
    dataNames = ['data11','data12']

    # Reading Data Files
    dataDir = 'C:/Users/ryanrp/Documents/CERN/analysis/ZZ_rpetersburg/allData/'
    dataFiles = [TFile(dataDir+dataNames[0]+'.root','read'),TFile(dataDir+dataNames[1]+'.root','read')]

    #Latex strings for luminosity [2011,2012] and lepton channels
    luminosityLatexString = ["#sqrt{s} = 7 TeV: #intLdt = 4.5 fb^{-1}", "#sqrt{s} = 8 TeV: #intLdt = 20.3 fb^{-1}"]
    channelLatexString = ['4#mu','2#mu2e','2e2#mu','4e']

    dataHistograms = []
    channelHistograms = []
    yearlyHistograms = []
    channelCanvas = []
    yearlyCanvas = []
    yearlyChannelCanvas = []

    combinedHistogram = TH1F('combinedHistogram', 'Combined Histogram', nBins, lowerLimit, upperLimit)

    for channelIndex,channel in enumerate(channels):
        channelCanvas.append(TCanvas(channel+'Canvas',channel+' Canvas',0,0,1500,800))
        channelHistograms.append(TH1F(channel+'Histogram',channel+' Histogram',nBins,lowerLimit,upperLimit))
        
    for yearIndex,dataName in enumerate(dataNames):
        # Create the canvases for each year of data
        yearlyCanvas.append(TCanvas(dataName+'TotalCanvas',dataName+' Total Canvas',0,0,1500,800))
        yearlyChannelCanvas.append(TCanvas(dataName+'ChannelCanvas',dataName+' Channel Canvas',0,0,1500,800))
        yearlyChannelCanvas[yearIndex].Divide(2,2)

        yearlyHistograms.append(TH1F(dataNames[yearIndex],dataNames[yearIndex],nBins,lowerLimit,upperLimit))
                                   
        for channelIndex,channel in enumerate(channels):
            histogramName = dataName+'_'+channel
            
            currentHistogram = TH1F(histogramName,histogramName,nBins,lowerLimit,upperLimit)

            yearlyChannelCanvas[yearIndex].cd(channelIndex+1)
            
            currentTree = dataFiles[yearIndex].Get(channel)
            currentTree.Draw('m4l_constrained>>'+histogramName, 'weight', 'E')

            drawHistogram(currentHistogram, 0.0425, channelLatexString[channelIndex], 0.04, luminosityLatexString[yearIndex])
            
            dataHistograms.append(currentHistogram) # List of all histograms for later reference

            channelHistograms[channelIndex].Add(currentHistogram) # Summing histograms with same channel
            yearlyHistograms[yearIndex].Add(currentHistogram) # Summing histograms within year
            combinedHistogram.Add(currentHistogram) # Summing all histograms
        
        yearlyChannelCanvas[yearIndex].SaveAs(dataNames[yearIndex]+'_channels.png')

        yearlyCanvas[yearIndex].cd()

        drawHistogram(yearlyHistograms[yearIndex], 0.0425, '4l', 0.03, luminosityLatexString[yearIndex])

        yearlyCanvas[yearIndex].Update()
        yearlyCanvas[yearIndex].SaveAs(dataName+'.png')

    for channelIndex,channel in enumerate(channels):
        channelCanvas[channelIndex].cd()
        drawHistogram(channelHistograms[channelIndex], 0.0425, channelLatexString[channelIndex], 0.03, luminosityLatexString[0], luminosityLatexString[1])
        channelCanvas[channelIndex].Update()
        channelCanvas[channelIndex].SaveAs('data_'+channel+'.png')

    combinedCanvas = TCanvas('combinedCanvas','Combined Canvas',0,0,1500,800)
    combinedCanvas.cd()

    drawHistogram(combinedHistogram,0.0425, '4l', 0.03, luminosityLatexString[0],luminosityLatexString[1])

    combinedCanvas.Update()
    combinedCanvas.SaveAs('data_combined.png')

