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
        self.binWidth = round(100*(self.upperLimit-self.lowerLimit)/self.nBins)/100

        self.channelTextSize = channelTextSize
        self.channelLatexString = ['4#mu','2#mu2e','2e2#mu','4e']
        self.luminosityTextSize = luminosityTextSize
        self.luminosityLatexStrings = ["#sqrt{s} = 7 TeV: #intLdt = 4.6 fb^{-1}",
                                      "#sqrt{s} = 8 TeV: #intLdt = 20.7 fb^{-1}"]
        self.dir = 'C:/Users/ryanrp/Documents/CERN/analysis/ZZ_rpetersburg/rootFiles/'
        self.channels = ['tree_incl_4mu','tree_incl_2mu2e','tree_incl_2e2mu','tree_incl_4e']
        self.ggFChannels = ['tree_ggF_4mu', 'tree_ggF_2mu2e', 'tree_ggF_2e2mu', 'tree_ggF_4e']
        
        self.axesLabel = '; m_{4l} [GeV]; Events/'+str(self.binWidth)+'GeV'
        self.m34Label = '; m_{34} [GeV]; Events/'+str(self.binWidth)+'GeV'
        self.phiLabel = '; #phi; Entries'
        self.cosTheta1Label = '; Cos(#theta_{1}); Entries'
        self.cosTheta2Label = '; Cos(#theta_{2}); Entries'
        self.cosThetaStarLabel = '; Cos(#theta*); Entries'
        self.phi1Label = '; #phi_{1}; Entries'

        self.jetBkgNorm = 3.92
        self.zzBkgNorm = 10.44
        self.higgsNorm = 17.35

        self.combinedCanvasNum = 0
        self.sameHistNameNum = 1

    def drawCombinedHistogram(self, histogramList, histogramNames, histogramOptions,
                              saveFileName = '', axesLabel = '', fitFunction = None):
        combinedCanvas = TCanvas('combinedCanvas'+str(self.combinedCanvasNum),
                                 'combinedCanvas'+axesLabel, 0, 0, 1000, 800)
        self.combinedCanvasNum += 1
        combinedCanvas.cd()

        # Create the stack of monte carlo data
        mcStack = THStack('mcStack','mcStack'+axesLabel)
        self.setMonteCarloStack(mcStack, histogramList[1:])

        # Draw the stack, experimental data, and possible fit function
        mcStack.Draw()
        histogramList[0].SetTitle(histogramList[0].GetTitle()+axesLabel)
        histogramList[0].Draw('Esame')
        if fitFunction:
            fitFunction.Draw('same')

        # Draw the legend
        legend = TLegend(0.6,0.65,0.9,0.9)
        for index, histogram in enumerate(histogramList):
            legend.AddEntry(histogram, histogramNames[index], histogramOptions[index])
        legend.SetFillColor(0)
        legend.SetBorderSize(0)
        legend.Draw()
        
        # Draw latex titles
        latex = TLatex()
        latex.SetTextAlign(12)
        # Title designating the lepton channel
        latex.SetTextSize(self.channelTextSize)
        latex.DrawLatex(self.titleOffset*self.upperLimit+(1-self.titleOffset)*self.lowerLimit,
                        self.maxY*0.9, "H #rightarrow ZZ^{(*)} #rightarrow 4l")
        # Title(s) designating the year(s) (luminosity)
        latex.SetTextSize(self.luminosityTextSize)
        for index,luminosityString in enumerate(self.luminosityLatexStrings):
            latex.DrawLatex(self.titleOffset*self.upperLimit+(1-self.titleOffset)*self.lowerLimit,
                            self.maxY*(0.8-0.1*index), luminosityString)
        # Draw the Atlas Label
        ATLASLabel(self.titleOffset+0.13,0.875,'Work in Progress',1)

        combinedCanvas.Update()
        if saveFileName:
            combinedCanvas.SaveAs(saveFileName+'.png')
            combinedCanvas.Close()
        
        
    def drawHistogram(self, histogram, option = 'e', leptonChannel = '4l',
                      luminosityYear = '', saveFileName = '', axesLabel = '',
                      fitFunction = None):
        canvas = TCanvas('combinedCanvas'+str(self.combinedCanvasNum),
                         'combinedCanvas'+axesLabel, 0, 0, 1000, 800)
        self.combinedCanvasNum += 1
        canvas.cd()
        
        # Draw the histogram with given option
        histogram.Draw(option)
        if fitFunction:
            fitFunction.Draw('same')

        histogram.SetTitle(histogram.GetTitle()+axesLabel)

        # Draw the legend
        legend = TLegend(0.7,0.85,0.9,0.9)
        legend.AddEntry(histogram, histogram.GetName(), option)
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
            canvas.Close()


    def setHistogram(self, histogram, rootFileNames, dataBranch = 'm4l_constrained',
                     weightBranch = 'weight', channels = ['tree_incl_4mu','tree_incl_2mu2e','tree_incl_2e2mu','tree_incl_4e'],
                     scale = []):
        if not channels:
            channels = self.channels
        files = []
        for yearIndex, fileName in enumerate(rootFileNames):
            files.append(TFile(self.dir+fileName+'.root','read'))
            for channelIndex, channel in enumerate(channels):
                currentHistogramName = fileName[-16:]+'_'+channel
                currentHistogram = TH1F( currentHistogramName, currentHistogramName,
                                         self.nBins, self.lowerLimit, self.upperLimit )
                
                currentTree = files[yearIndex].Get(channel)
                currentTree.Draw(dataBranch+'>>'+currentHistogramName, weightBranch, 'n')
                if scale:
                    currentHistogram.Scale(scale[yearIndex][channelIndex]/currentHistogram.Integral())                    
                
                histogram.Add(currentHistogram)
                
            
        histogram.SetMaximum(self.maxY)

    def setHistogramWithChain(self, histogram, rootFileNames, dataBranch = 'm4l_constained',
                              weightBranch = 'weight', channels = ['tree_incl_4mu','tree_incl_2mu2e','tree_incl_2e2mu','tree_incl_4e'],
                              scale = 0, parallel = False):
        chain = TChain(histogram.GetName()+'Chain', histogram.GetName()+' Chain')
        if parallel:
            for index, fileName in enumerate(rootFileNames):
                for channel in channels[index]:
                    chain.Add(self.dir+fileName+'.root/'+channel)
        else:
            for fileName in rootFileNames:
                for channel in channels:
                    chain.Add(self.dir+fileName+'.root/'+channel)
        chain.Draw(dataBranch+'>>'+histogram.GetName(), weightBranch, 'n')
        if scale:
            histogram.Scale(scale/histogram.Integral())
        histogram.SetMaximum(self.maxY)

    def combineHistograms(self, combinedHistogram, histogramList, multiplier = [1,1,1,1,1]):
        for index, histogram in enumerate(histogramList):
            combinedHistogram.Add(histogram, multiplier[index])
        combinedHistogram.SetMaximum(self.maxY)            

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
                if channelIndex%2 == 0:
                    for bn in xrange(mmHistogram.GetNbinsX()):
                        currentHistogram.Fill(mmHistogram.GetBinCenter(bn), mmHistogram.GetBinContent(bn))
                else:
                    for bn in xrange(mmHistogram.GetNbinsX()):
                        currentHistogram.Fill(eeHistogram.GetBinCenter(bn)+0.01, eeHistogram.GetBinContent(bn))
##                currentHistogram.Scale(normNumber[yearIndex][channelIndex]/currentHistogram.Integral())
                jetHistogram.Add(currentHistogram)
        jetHistogram.SetMaximum(self.maxY)

    def formatHistogram(self, histogram, color, scaleFactor = 0, lineWidth = 0):
        histogram.SetFillColor(color)
        if scaleFactor:
            histogram.Scale(scaleFactor/histogram.Integral())
        histogram.SetLineWidth(0)
        histogram.SetMaximum(self.maxY)


    def setMonteCarloStack(self, mcStack, mcList):
        for histogram in mcList:
            mcStack.Add(histogram)
        mcStack.SetMaximum(self.maxY)

    def fitHistogram(self, histogram, combinedFit, parameters = [],
                     fitFunctions = [], fittedFunctions = []):
        if fitFunctions:
            parameters = []
            for func in fitFunctions:
                # Set the parameters for each fit function
                histogram.Fit(func, 'nr+')
                # Extract the parameters from each fit function
                for index in xrange(func.GetNumberFreeParameters()):
                    parameters.append(func.GetParameter(index))

        if fittedFunctions:
            parameters = []
            for func in fittedFunctions:
                for index in xrange(func.GetNumberFreeParameters()):
                    parameters.append(func.GetParameter(index))

        # Set the parameters for the combined function
        for index, par in enumerate(parameters):
            combinedFit.SetParameter(index,par)

        if not fittedFunctions:
            histogram.Fit(combinedFit, 'nr+')
