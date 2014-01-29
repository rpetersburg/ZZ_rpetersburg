from ROOT import gROOT
gROOT.LoadMacro("atlasstyle/AtlasStyle.C")
gROOT.LoadMacro("atlasstyle/AtlasLabels.C")
from ROOT import *

class PlotData():

    def __init__(self):
        # Setting global variables for histograms
        self.nBins = 32
        self.lowerLimit = 80
        self.upperLimit = 250
        self.titleOffset = 0.35
        
    def drawHistogram(self, histogram, channelTextSize, leptonChannel, luminosityTextSize, luminosityString1,luminosityString2 = False):
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
        latex.DrawLatex(self.titleOffset*self.upperLimit+(1-self.titleOffset)*self.lowerLimit, maxY*0.83, "H #rightarrow ZZ^{(*)} #rightarrow " + leptonChannel)
        # Title(s) designating the year(s) (luminosity)
        latex.SetTextSize(luminosityTextSize)
        latex.DrawLatex(self.titleOffset*self.upperLimit+(1-self.titleOffset)*self.lowerLimit, maxY*0.7, luminosityString1)
        if luminosityString2:
            latex.DrawLatex(self.titleOffset*self.upperLimit+(1-self.titleOffset)*self.lowerLimit, maxY*0.6, luminosityString2)
        # Draw the Atlas Label
        ATLASLabel(.4,0.875,'Work in Progress',1)

    def plotData(self):
        SetAtlasStyle()

        # Lists of strings for channels and data years
        channels = ['tree_incl_4mu','tree_incl_2mu2e','tree_incl_2e2mu','tree_incl_4e']
        dataNames = ['data11','data12']

        # Reading Data Files
        dataDir = 'C:/Users/ryanrp/Documents/CERN/analysis/ZZ_rpetersburg/rootFiles/'
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

        combinedHistogram = TH1F('combinedHistogram', 'Combined Histogram', self.nBins, self.lowerLimit, self.upperLimit)

        # Create canvas and histogram for each channel
        for channelIndex,channel in enumerate(channels):
            channelCanvas.append(TCanvas(channel+'Canvas',channel+' Canvas',0,0,1500,800))
            channelHistograms.append(TH1F(channel+'Histogram',channel+' Histogram',self.nBins,self.lowerLimit,self.upperLimit))
            
        for yearIndex,dataName in enumerate(dataNames):
            # Create canvas and histogram for each year
            yearlyCanvas.append(TCanvas(dataName+'TotalCanvas',dataName+' Total Canvas',0,0,1500,800))
            yearlyHistograms.append(TH1F(dataNames[yearIndex],dataNames[yearIndex],self.nBins,self.lowerLimit,self.upperLimit))

            #Create canvas for individual channels within each year
            yearlyChannelCanvas.append(TCanvas(dataName+'ChannelCanvas',dataName+' Channel Canvas',0,0,1500,800))
            yearlyChannelCanvas[yearIndex].Divide(2,2)        

            # Draw and save histogram for each year and channel                      
            for channelIndex,channel in enumerate(channels):
                histogramName = dataName+'_'+channel
                yearlyChannelCanvas[yearIndex].cd(channelIndex+1)

                currentHistogram = TH1F(histogramName,histogramName,self.nBins,self.lowerLimit,self.upperLimit)

                # Find correct data tree and add it to the current histogram
                currentTree = dataFiles[yearIndex].Get(channel)
                currentTree.Draw('m4l_constrained>>'+histogramName, 'weight', 'E')

                self.drawHistogram(currentHistogram, 0.0425, channelLatexString[channelIndex], 0.04, luminosityLatexString[yearIndex])
                
                dataHistograms.append(currentHistogram) # List of all histograms for later reference

                channelHistograms[channelIndex].Add(currentHistogram) # Summing histograms with same channel
                yearlyHistograms[yearIndex].Add(currentHistogram) # Summing histograms within year
                combinedHistogram.Add(currentHistogram) # Summing all histograms

            yearlyChannelCanvas[yearIndex].SaveAs(dataNames[yearIndex]+'_channels.png')

            # Draw and save histogram for the yearly data
            yearlyCanvas[yearIndex].cd()
            self.drawHistogram(yearlyHistograms[yearIndex], 0.0425, '4l', 0.03, luminosityLatexString[yearIndex])
            #yearlyCanvas[yearIndex].Update()
            yearlyCanvas[yearIndex].SaveAs(dataName+'.png')

        # Draw and save histograms for each channel
        for channelIndex,channel in enumerate(channels):
            channelCanvas[channelIndex].cd()
            self.drawHistogram(channelHistograms[channelIndex], 0.0425, channelLatexString[channelIndex], 0.03, luminosityLatexString[0], luminosityLatexString[1])
            #channelCanvas[channelIndex].Update()
            channelCanvas[channelIndex].SaveAs('data_'+channel+'.png')

        # Draw and save the total combined histogram
        combinedCanvas = TCanvas('combinedCanvas','Combined Canvas',0,0,1500,800)
        combinedCanvas.cd()
        self.drawHistogram(combinedHistogram,0.0425, '4l', 0.03, luminosityLatexString[0],luminosityLatexString[1])
        #combinedCanvas.Update()
        combinedCanvas.SaveAs('data_combined.png')


if __name__ == '__main__':
    app = PlotData()
    app.plotData()
