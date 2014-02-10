from ROOT import *
gROOT.LoadMacro('atlasstyle/AtlasStyle.C')
gROOT.LoadMacro('atlasstyle/AtlasLabels.C')
import PlotHiggs
SetAtlasStyle()

deadCanvas = TCanvas('','',0,0,0,0)

higgs = PlotHiggs.PlotHiggs(36, 80, 170, 0.05, 1000)

mcJetBkgFiles = ['extraFiles/MC11c/ZPlusJetsForShapes/reduxbkg_tree_v2',
                 'extraFiles/MC12a/ZPlusJetsForShapes/reduxbkg_tree_v2']
##mcJetBkgFiles = ['data11', 'data12']
mcJetBkgHistogram = TH1F( 'mcJetBkgHistogram', 'MC Jet Background Histogram', higgs.nBins, higgs.lowerLimit, higgs.upperLimit )
higgs.setHistogram(mcJetBkgHistogram, mcJetBkgFiles, 'm4l_constrained', 'weight', ['tree'])
higgs.formatHistogram(mcJetBkgHistogram, kViolet)

higgs.drawHistogram(mcJetBkgHistogram, 'e')

##
##f = TFile(higgs.dir+mcJetBkgFiles[1]+'.root', 'read')
##h = TH1F('h', 'h', higgs.nBins, higgs.lowerLimit, higgs.upperLimit)
##t = f.Get('tree')
##t.Draw('m4l_constrained>>h', 'weight')
