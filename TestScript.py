from ROOT import *
gROOT.LoadMacro('atlasstyle/AtlasStyle.C')
gROOT.LoadMacro('atlasstyle/AtlasLabels.C')
##SetAtlasStyle()

channels = ['tree_incl_4mu','tree_incl_2mu2e','tree_incl_2e2mu','tree_incl_4e']

##h1 = TH1F('h1', 'h1', 20, -4, 4)

h2 = TH1F('h2', 'h2', 20, -4, 4)

f1 = TFile('C:/Users/ryanrp/Documents/CERN/analysis/ZZ_rpetersburg/rootFiles/data12.root','read')

for channelIndex, channel in enumerate(channels):
    h1 = TH1F('h1'+channel, 'h1', 20, -4, 4)
    t1 = f1.Get(channel)
    t1.Draw('phi>>h1'+channel, 'abs(weight)*(m4l_constrained<130 && m4l_constrained>115)')
    h2.Add(h1)

c2 = TCanvas('c2', 'c2', 0, 0, 1000, 800)
c2.cd()

h2.Draw()


##c1 = TCanvas('c1', 'c1', 0,0,1000, 800)
##c1.cd()
##
##h1.Draw('e')
##
##c1.Update()
