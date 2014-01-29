from ROOT import *
gROOT.LoadMacro('atlasstyle/AtlasStyle.C')
gROOT.LoadMacro('atlasstyle/AtlasLabels.C')

class PlotHiggs():

    def __init__(self):
        #Setting global variables for histograms
        self.nBins = 34
        self.lowerLimit = 80
        self.upperLimit = 250
        self.titleOffset = 0.05
        self.maxY = 35

        self.channelTextSize = 0.0425
        self.channelLatexString = ['4#mu','2#mu2e','2e2#mu','4e']
        self.luminosityTextSize = 0.0325
        self.luminosityLatexStrings = ["#sqrt{s} = 7 TeV: #intLdt = 4.5 fb^{-1}",
                                      "#sqrt{s} = 8 TeV: #intLdt = 20.3 fb^{-1}"]
        self.dir = 'C:/Users/ryanrp/Documents/CERN/analysis/ZZ_rpetersburg/rootFiles/'
        self.channels = ['tree_incl_4mu','tree_incl_2mu2e','tree_incl_2e2mu','tree_incl_4e']
        
        
        
    def drawHistogram(self, histogram, option = 'E', leptonChannel = '4l', channelTextSize = 0.0425,
                      luminosityStringList = [], luminosityTextSize = 0.0325):
        # Draw the histogram with given option
        histogram.Draw(option)
        
        # Add titles to the histogram axes
        histogram.GetXaxis().SetTitle("m_{4l}[GeV]")
        histogram.GetYaxis().SetTitle("Events/2.5GeV")

##        self.drawLatex(leptonChannel, channelTextSize, luminosityStringList, luminosityTextSize, titleOffset)

    def setHistogram(self, histogram, rootFileNames):
        files = [TFile(self.dir+rootFileNames[0]+'.root','read'),
                 TFile(self.dir+rootFileNames[1]+'.root','read')]

        for yearIndex, fileName in enumerate(rootFileNames):
            for channelIndex, channel in enumerate(self.channels):
                currentHistogramName = fileName+'_'+channel
                currentHistogram = TH1F( currentHistogramName, currentHistogramName, self.nBins, self.lowerLimit, self.upperLimit )

                currentTree = files[yearIndex].Get(channel)
                currentTree.Draw('m4l_constrained>>'+currentHistogramName, 'weight')

                histogram.Add(currentHistogram)

    def setHistogramJets(self, jetHistogram, rootFileNames):
        jetFile = TFile("C:/Users/ryanrp/Documents/CERN/analysis/ZZ_rpetersburg/rootFiles/redBkg_smoothed.root", "read")

        eeHistogram = jetFile.Get('Reducible_bkg_1D_llee_0')
        mmHistogram = jetFile.Get('Reducible_bkg_1D_llmumu_0')

        normNumber = [[1.3,0.97,1.33,0.67],[0.13,0.52,0.107,0.52]]

        testCanvas = TCanvas('test','test',0,0,1000,800)
        testCanvas.Divide(4,2)

        for yearIndex, fileName in enumerate(rootFileNames):
            for channelIndex, channel in enumerate(self.channels):
                testCanvas.cd(4*yearIndex+channelIndex+1)
                print 4*yearIndex+channelIndex+1
                currentHistogramName = fileName+'_'+channel
                currentHistogram = TH1F( currentHistogramName, currentHistogramName, self.nBins, self.lowerLimit, self.upperLimit)
                for k in xrange(mmHistogram.GetNbinsX()):
                    if channelIndex%2 == 0:
                        currentHistogram.Fill(mmHistogram.GetBinCenter(k), mmHistogram.GetBinContent(k))
                    else:
                        currentHistogram.Fill(eeHistogram.GetBinCenter(k)+0.01, eeHistogram.GetBinContent(k))
                currentHistogram.Draw()
                currentHistogram.Scale(normNumber[yearIndex][channelIndex]/currentHistogram.Integral())
                jetHistogram.Add(currentHistogram)
        testCanvas.Update()
        testCanvas.SaveAs('test.png')
                        

    def formatHistogram(self, histogram, color):
        histogram.SetFillColor(color)
        histogram.SetLineWidth(0)

    def setMonteCarloStack(self, mcStack, mcList):
        for histogram in mcList:
            mcStack.Add(histogram)

        mcStack.SetMaximum(self.maxY)

    def drawCombinedHistogram(self, histogramList, histogramNames, histogramOptions):
        combinedCanvas = TCanvas('combinedCanvas', 'combinedCanvas', 0, 0, 1000, 800)
        combinedCanvas.cd()
        
        mcStack = THStack('mcStack','mcStack; m_{4l} [GeV]; Events/2.5GeV')
        self.setMonteCarloStack(mcStack, histogramList[1:])
        
        mcStack.Draw()
        histogramList[0].Draw('Esame')

        #Draw the legend
        legend = TLegend(0.7,0.75,0.9,0.9)
        for index, histogram in enumerate(histogramList):
            legend.AddEntry(histogram, histogramNames[index], histogramOptions[index])
        legend.SetFillColor(0)
        legend.SetBorderSize(0)
        legend.Draw()
        
        # Get the max y value on the graph
        gPad.Update()
        maxY = gPad.GetFrame().GetY2()
        
        # Draw latex titles
        latex = TLatex()
        latex.SetTextAlign(12)
        # Title designating the lepton channel
        latex.SetTextSize(self.channelTextSize)
        latex.DrawLatex(self.titleOffset*self.upperLimit+(1-self.titleOffset)*self.lowerLimit, self.maxY*0.9, "H #rightarrow ZZ^{(*)} #rightarrow 4l")
        # Title(s) designating the year(s) (luminosity)
        latex.SetTextSize(self.luminosityTextSize)
        for index,luminosityString in enumerate(self.luminosityLatexStrings):
            latex.DrawLatex(self.titleOffset*self.upperLimit+(1-self.titleOffset)*self.lowerLimit, self.maxY*(0.8-0.1*index), luminosityString)
        # Draw the Atlas Label
        ATLASLabel(self.titleOffset+0.13,0.875,'Work in Progress',1)

        combinedCanvas.Update()
        combinedCanvas.SaveAs('test_run.png')

    def run(self):
        SetAtlasStyle()

        histogramList = []
        
        dataFiles = ['data11','data12']
        dataHistogram = TH1F( 'dataHistogram', 'Data Histogram', self.nBins, self.lowerLimit, self.upperLimit )
        self.setHistogram(dataHistogram, dataFiles)

        mcJetBkgFiles = ['out_redBkg_Comb','out_redBkg_Comb']
        mcJetBkgHistogram = TH1F( 'mcJetBkgHistogram', 'MC Jet Background Histogram', self.nBins, self.lowerLimit, self.upperLimit)
        self.setHistogramJets(mcJetBkgHistogram, mcJetBkgFiles)
        self.formatHistogram(mcJetBkgHistogram, kViolet)

        mcZZBkgFiles = ['mc11_ZZComb','mc12_ZZComb']
        mcZZBkgHistogram = TH1F( 'mcZZBkgHistogram', 'MC ZZ Background Histogram', self.nBins, self.lowerLimit, self.upperLimit)
        self.setHistogram(mcZZBkgHistogram, mcZZBkgFiles)
        self.formatHistogram(mcZZBkgHistogram, kRed)

        mcSignalFiles = ['mc11_signalComb','mc12_signalComb']
        mcSignalHistogram = TH1F( 'mcSignalHistogram', 'MC Signal Histogram', self.nBins, self.lowerLimit, self.upperLimit )
        self.setHistogram(mcSignalHistogram, mcSignalFiles)
        self.formatHistogram(mcSignalHistogram, kCyan)

        histogramList = [dataHistogram, mcJetBkgHistogram, mcZZBkgHistogram, mcSignalHistogram]
        histogramNames = ['Experimental Data', 'MC Background Z+jets, t#bar{t}', 'MC Background ZZ^{(*)}', 'MC Signal (m_{H} = 125 GeV)']
        histogramOptions = ['pe','f','f','f']

        self.drawCombinedHistogram(histogramList,histogramNames, histogramOptions)


SetAtlasStyle()
if __name__ == '__main__':
    app = PlotHiggs()
    app.run()
