from ROOT import *
gROOT.LoadMacro('atlasstyle/AtlasStyle.C')
gROOT.LoadMacro('atlasstyle/AtlasLabels.C')
import math

class PlotHiggs():

    def __init__(self, nBins = 34, lowerLimit = 80, upperLimit = 250, titleOffset = 0.05,
                 maxY = 35, channelTextSize = 0.0425, luminosityTextSize = 0.0325):
        #Setting global variables for histograms
        self.nBins = nBins
        self.lowerLimit = lowerLimit
        self.upperLimit = upperLimit
        self.titleOffset = titleOffset
        self.maxY = maxY

        self.channelTextSize = channelTextSize
        self.channelLatexString = ['4#mu','2#mu2e','2e2#mu','4e']
        self.luminosityTextSize = luminosityTextSize
        self.luminosityLatexStrings = ["#sqrt{s} = 7 TeV: #intLdt = 4.6 fb^{-1}",
                                      "#sqrt{s} = 8 TeV: #intLdt = 20.7 fb^{-1}"]
        self.dir = 'C:/Users/ryanrp/Documents/CERN/analysis/ZZ_rpetersburg/rootFiles/'
        self.channels = ['tree_incl_4mu','tree_incl_2mu2e','tree_incl_2e2mu','tree_incl_4e']


    def drawCombinedHistogram(self, histogramList, histogramNames, histogramOptions, saveFileName = False):
        combinedCanvas = TCanvas('combinedCanvas', 'combinedCanvas', 0, 0, 1000, 800)
        combinedCanvas.cd()

        # Create the stack of monte carlo data
        mcStack = THStack('mcStack','mcStack; m_{4l} [GeV]; Events/2.5GeV')
        self.setMonteCarloStack(mcStack, histogramList[1:])

        # Draw the stack and the experimental data
        mcStack.Draw()
        histogramList[0].Draw('Esame')

        # Draw the legend
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
        if saveFileName:
            combinedCanvas.SaveAs(saveFileName+'.png')        
        
        
    def drawHistogram(self, histogram, option = 'E', leptonChannel = '4l',
                      luminosityYear = False, saveFileName = False):
        canvas = TCanvas('combinedCanvas', 'combinedCanvas', 0, 0, 1000, 800)
        canvas.cd()
        
        # Draw the histogram with given option
        histogram.Draw(option)
        
        # Add titles to the histogram axes
        histogram.GetXaxis().SetTitle("m_{4l}[GeV]")
        histogram.GetYaxis().SetTitle("Events/2.5GeV")

        # Get the max y value on the graph
        gPad.Update()
        maxY = gPad.GetFrame().GetY2()

        # Draw latex titles
        latex = TLatex()
        latex.SetTextAlign(12)
        # Title designating the lepton channel
        latex.SetTextSize(self.channelTextSize)
        latex.DrawLatex(self.titleOffset*self.upperLimit+(1-self.titleOffset)*self.lowerLimit, maxY*0.85, "H #rightarrow ZZ^{(*)} #rightarrow 4l")
        # Title(s) designating the year(s) (luminosity)
        latex.SetTextSize(self.luminosityTextSize)
        if not luminosityYear:
            for index,luminosityString in enumerate(self.luminosityLatexStrings):
                latex.DrawLatex(self.titleOffset*self.upperLimit+(1-self.titleOffset)*self.lowerLimit, maxY*(0.75-0.1*index), luminosityString)
        else:
            if luminosityYear[-2:] == '12': index = 1
            else: index = 0
            latex.DrawLatex(self.titleOffset*self.upperLimit+(1-self.titleOffset)*self.lowerLimit, maxY*(0.75), luminosityLatexStrings[index])
        # Draw the Atlas Label
        ATLASLabel(self.titleOffset+0.13,0.875,'Work in Progress',1)

        canvas.Update()
        if saveFileName:
            canvas.SaveAs(saveFileName+'.png')
        

    def setHistogram(self, histogram, rootFileNames):
        files = []
        for yearIndex, fileName in enumerate(rootFileNames):
            files.append(TFile(self.dir+fileName+'.root','read'))
            for channelIndex, channel in enumerate(self.channels):
                currentHistogramName = fileName+'_'+channel
                currentHistogram = TH1F( currentHistogramName, currentHistogramName, self.nBins, self.lowerLimit, self.upperLimit )

                currentTree = files[yearIndex].Get(channel)
                currentTree.Draw('m4l_constrained>>'+currentHistogramName, 'weight')

                histogram.Add(currentHistogram)
        histogram.SetMaximum(self.maxY)
                

    def setHistogramJets(self, jetHistogram, rootFileNames):
        jetFile = TFile("C:/Users/ryanrp/Documents/CERN/analysis/ZZ_rpetersburg/rootFiles/redBkg_smoothed.root", "read")

        eeHistogram = jetFile.Get('Reducible_bkg_1D_llee_0')
        mmHistogram = jetFile.Get('Reducible_bkg_1D_llmumu_0')

        normNumber = [[1.3,0.97,1.33,0.67],[0.13,0.52,0.107,0.52]]

        testCanvas = TCanvas('test','test',0,0,1000,800)
        testCanvas.Divide(4,2)

        for yearIndex, fileName in enumerate(rootFileNames):
            for channelIndex, channel in enumerate(self.channels):
                currentHistogramName = fileName+'_'+channel
                currentHistogram = TH1F( currentHistogramName, currentHistogramName, self.nBins, self.lowerLimit, self.upperLimit)
                for k in xrange(mmHistogram.GetNbinsX()):
                    if channelIndex%2 == 0:
                        currentHistogram.Fill(mmHistogram.GetBinCenter(k), mmHistogram.GetBinContent(k))
                    else:
                        currentHistogram.Fill(eeHistogram.GetBinCenter(k)+0.01, eeHistogram.GetBinContent(k))
                currentHistogram.Scale(normNumber[yearIndex][channelIndex]/currentHistogram.Integral())
                jetHistogram.Add(currentHistogram)
                        

    def formatHistogram(self, histogram, color):
        histogram.SetFillColor(color)
        histogram.SetLineWidth(0)

    def setMonteCarloStack(self, mcStack, mcList):
        for histogram in mcList:
            mcStack.Add(histogram)
        mcStack.SetMaximum(self.maxY)


    def fitHistogram(self, histogram, combinedFit, parameters, fitFunctions = False):
        if fitFunctions:
            parameters = []
            for func in fitFunctions:
                # Set the parameters for each fit function
                histogram.Fit(func, 'nr+')
                # Extract the parameters from each fit function
                for index in xrange(func.GetNumberFreeParameters()):
                    parameters.append(func.GetParameters()[index])

        # Set the parameters for the combined function
        for index, par in enumerate(parameters):
            combinedFit.SetParameter(index,par)
        print parameters
        dataHistogram.Fit(combinedFit, 'r+', 'e')
