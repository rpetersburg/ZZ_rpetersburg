from ROOT import *
gROOT.LoadMacro('atlasstyle/AtlasStyle.C')
import PlotHiggs
import math
SetAtlasStyle()

deadCanvas = TCanvas('','',0,0,0,0)

higgsObjects = [PlotHiggs.PlotHiggs(8, -math.pi, math.pi, 0.05, 18), PlotHiggs.PlotHiggs(8, -1, 1, 0.05, 16), PlotHiggs.PlotHiggs(8, -math.pi, math.pi, 0.05, 18), PlotHiggs.PlotHiggs(8, -1, 1, 0.05, 24), PlotHiggs.PlotHiggs(8, -1, 1, 0.05, 16)]
higgsM34 = PlotHiggs.PlotHiggs(9, 12, 57, 0.05, 25)
labels = [higgsM34.phiLabel, higgsM34.cosTheta1Label, higgsM34.phi1Label, higgsM34.cosTheta2Label, higgsM34.cosThetaStarLabel]
angles = ['phi', 'cth1', 'phi1', 'cth2', 'cthstr']
spins = ['0p','0m','1p','1m','2p','2m']
spinLabels = ["0^{+}", "0^{-}", '1^{+}', '1^{-}', "2^{+}", "2^{-}"]
ksTest = [[0 for j in xrange(len(spins))] for i in xrange(len(angles))]
chiTest = [[0 for j in xrange(len(spins))] for i in xrange(len(angles))]
weightFactor = [1, -1, -1, -1, -1, -1]

dataFiles = ['data11','data12']
mcJetBkgFiles = ['extraFiles/MC12a/ZPlusJetsForShapes/dataAngular_Monriond2013_2012',
                 'extraFiles/MC11c/ZPlusJetsForShapes/dataAngular_Monriond2013_2011']
mcZZBkgFiles = ['extraFiles/MC12a/PowhegPythia8_AU2CT10_ZZ*',
                'extraFiles/MC11c/PowhegPythia8_AU2CT10_ZZ*',
                'extraFiles/MC12a/Sherpa_CT10_llll_ZZ_EW6_noHiggs',
                'extraFiles/MC11c/Sherpa_CT10_llll_ZZ_EW6_noHiggs']

dataM34Histogram = TH1F( 'dataM34Histogram', 'Data M34 Histogram', higgsM34.nBins, higgsM34.lowerLimit, higgsM34.upperLimit )
higgsM34.setHistogramWithChain(dataM34Histogram, dataFiles, 'mZ2_constrained', '(m4l_constrained<130 && m4l_constrained>115)')

mcJetBkgM34Histogram = TH1F( 'mcJetBkgM34Histogram',  'MC Jet Background M34 Histogram', higgsM34.nBins, higgsM34.lowerLimit, higgsM34.upperLimit )
higgsM34.setHistogramWithChain( mcJetBkgM34Histogram, mcJetBkgFiles, 'M34', 'weight*(m4_unconstrained < 130 && m4_unconstrained > 115)', ['physics'], higgsM34.jetBkgNorm)
higgsM34.formatHistogram(mcJetBkgM34Histogram, kViolet)

mcZZBkgM34Histogram = TH1F( 'mcZZBkgM34Histogram', 'MC ZZ Bkg M34 Histogram', higgsM34.nBins, higgsM34.lowerLimit, higgsM34.upperLimit )
higgsM34.setHistogramWithChain( mcZZBkgM34Histogram, mcZZBkgFiles, 'mZ2_constrained', 'weight*(m4l_constrained < 130 && m4l_constrained > 115)', higgsM34.channels, higgsM34.zzBkgNorm)
higgsM34.formatHistogram(mcZZBkgM34Histogram, kRed)

mcCombinedM34Histogram = [0 for j in xrange(len(spins))]

for angleIndex, higgs in enumerate(higgsObjects):

    dataHistogram = TH1F( 'data'+angles[angleIndex]+'Histogram', 'Data '+angles[angleIndex]+' Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
    higgs.setHistogramWithChain(dataHistogram, dataFiles, angles[angleIndex], 'abs(weight)*(m4l_constrained<130 && m4l_constrained>115)')
    
    mcJetBkgHistogram = TH1F( 'mcJetBkg'+angles[angleIndex]+'Histogram', 'MC Jet Background '+angles[angleIndex]+' Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit)
    higgs.setHistogramWithChain(mcJetBkgHistogram, mcJetBkgFiles, angles[angleIndex], 'abs(weight)*(m4_unconstrained<130 && m4_unconstrained>115)', ['physics'], higgs.jetBkgNorm)
    higgs.formatHistogram(mcJetBkgHistogram, kViolet)

    mcZZBkgHistogram = TH1F( 'mcZZBkg'+angles[angleIndex]+'Histogram', 'MC ZZ Background '+angles[angleIndex]+' Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit)
    higgs.setHistogramWithChain(mcZZBkgHistogram, mcZZBkgFiles, angles[angleIndex], 'abs(weight)*(m4l_constrained<130 && m4l_constrained>115)', higgs.channels, higgs.zzBkgNorm)
    higgs.formatHistogram(mcZZBkgHistogram, kRed)

    for spinIndex, spin in enumerate(spins):
        # Set the MC signal histogram (different for each spin)
        
        parallel = False
        if spin == '0p':
            mcSignalFiles = ['extraFiles/MC12a/Signal/PowhegPythia8_AU2CT10_ggH125_ZZ4lep',
                             'extraFiles/MC11c/Signal/PowhegPythia_ggH125_ZZ4lep']
            mcSignalChannels = higgs.channels
        elif spin == '0m':
            mcSignalFiles = ['extraFiles/MC12a/JHUPythia8_AU2CTEQ6L1_ggH125_Spin'+spin+'_ZZ4lep']
            mcSignalChannels = higgs.channels+higgs.ggFChannels
        elif spin[0] == '1':
            mcSignalFiles = ['extraFiles/MC12a/JHUPythia8_AU2CTEQ6L1_qqH125_Spin'+spin+'_ZZ4lep']
            mcSignalChannels = higgs.channels+higgs.ggFChannels
        else:
            mcSignalFiles = ['extraFiles/MC12a/JHUPythia8_AU2CTEQ6L1_ggH125_Spin'+spin+'_ZZ4lep',
                             'extraFiles/MC12a/JHUPythia8_AU2CTEQ6L1_qqH125_Spin'+spin+'_ZZ4lep']
            mcSignalChannels = [higgs.channels,higgs.ggFChannels]
            parallel = True
            
        mcSignalHistogram = TH1F( 'mcSignalSpin'+spin+angles[angleIndex]+'Histogram', 'MC Signal Spin '+spin+angles[angleIndex]+' Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
        higgs.setHistogramWithChain(mcSignalHistogram, mcSignalFiles, angles[angleIndex], 'abs(weight)*(m4l_constrained<130 && m4l_constrained>115)', mcSignalChannels, higgs.higgsNorm, parallel)
        higgs.formatHistogram(mcSignalHistogram, kCyan)

        # Plot Data and MC spin
        
        histogramList = [dataHistogram, mcJetBkgHistogram, mcZZBkgHistogram, mcSignalHistogram]
        histogramNames = ['Experimental Data', 'MC Background Z+jets','MC Background ZZ^{(*)}', 'MC Signal (m_{H} = 125 GeV, J^{p} = '+spinLabels[spinIndex]+')']
        histogramOptions = ['pe','f','f','f']

        higgs.drawCombinedHistogram(histogramList,histogramNames, histogramOptions, 'combinedGraphs/Spin'+angles[angleIndex]+'/HiggsSpin'+spin+angles[angleIndex], labels[angleIndex])

        # Plot Data and MC m34
        if angleIndex == 0:
            mcSignalM34Histogram = TH1F( 'mcSignalM34Spin'+spin+'Histogram', 'MC Signal M34 Spin '+spin+' Histogram', higgsM34.nBins, higgsM34.lowerLimit, higgsM34.upperLimit )
            higgsM34.setHistogramWithChain(mcSignalM34Histogram, mcSignalFiles, 'mZ2_constrained', str(weightFactor[spinIndex])+'*weight*(m4l_constrained<130 && m4l_constrained>115)', higgsM34.channels, higgsM34.higgsNorm)
            higgsM34.formatHistogram(mcSignalM34Histogram, kCyan)

            mcCombinedM34Histogram[spinIndex] = TH1F( 'mcCombinedM34Spin'+spin+'Histogram', 'MC Combined M34 Spin '+spin+' Histogram', higgsM34.nBins, higgsM34.lowerLimit, higgsM34.upperLimit )
            higgsM34.combineHistograms( mcCombinedM34Histogram[spinIndex], [mcJetBkgM34Histogram, mcZZBkgM34Histogram, mcSignalM34Histogram] )
            
            histogramList = [dataM34Histogram, mcJetBkgM34Histogram, mcZZBkgM34Histogram, mcSignalM34Histogram]
            higgsM34.drawCombinedHistogram(histogramList, histogramNames, histogramOptions, 'combinedGraphs/SpinM34/HiggsM34Spin'+spin, higgsM34.m34Label)

        # Calculate statistical relation between MC and Data for each Spin and angle

        mcCombinedHistogram = TH1F( 'mcCombinedSpin'+spin+angles[angleIndex]+'Histogram', 'MC Combined Spin '+spin+angles[angleIndex]+' Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
        higgs.combineHistograms( mcCombinedHistogram, [mcJetBkgHistogram, mcZZBkgHistogram, mcSignalHistogram] )

        ksTest[angleIndex][spinIndex] = dataHistogram.KolmogorovTest(mcCombinedHistogram, '')
        chiTest[angleIndex][spinIndex] = dataHistogram.Chi2Test(mcCombinedHistogram, '')

combinedSumKS = [0 for j in xrange(len(spins))]
combinedSumChi= [0 for j in xrange(len(spins))]
# Print all relevant data for each spin
print 'Spin/Parity    \t',
for spin in spins:
    print spin + '\t',
print '\nKolmogorov Test',
for angleIndex, angle in enumerate(angles):
    print '\n'+angle+'     \t',
    for spinIndex in xrange(len(spins)):
        combinedSumKS[spinIndex] += ksTest[angleIndex][spinIndex]
        print str(round(1000*ksTest[angleIndex][spinIndex])/1000) + '\t',
print '\nM34            \t',
for spinIndex in xrange(len(spins)):
    # Calculate statistical relation between MC and Data for m34
    ksM34Test = dataM34Histogram.KolmogorovTest(mcCombinedM34Histogram[spinIndex], '')
    combinedSumKS[spinIndex] += ksM34Test
    print str(round(1000*ksM34Test)/1000) + '\t',
print '\nAverage        \t',
for spinIndex in xrange(len(spins)):
    print str(round(1000*combinedSumKS[spinIndex]/(len(angles)+1))/1000) + '\t',
print '\nChi^2 Test',
for angleIndex, angle in enumerate(angles):
    print '\n'+angle+'     \t',
    for spinIndex in xrange(len(spins)):
        combinedSumChi[spinIndex] += chiTest[angleIndex][spinIndex]
        print str(round(1000*chiTest[angleIndex][spinIndex])/1000) + '\t',
print '\nM34            \t',
for spinIndex in xrange(len(spins)):
    # Calculate statistical relation between MC and Data for m34
    chiM34Test = dataM34Histogram.Chi2Test(mcCombinedM34Histogram[spinIndex], '')
    combinedSumChi[spinIndex] += chiM34Test
    print str(round(1000*chiM34Test)/1000) + '\t',
print '\nAverage        \t',
for spinIndex in xrange(len(spins)):
    print str(round(1000*combinedSumChi[spinIndex]/(len(angles)+1))/1000) + '\t',
