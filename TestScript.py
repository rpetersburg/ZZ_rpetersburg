from ROOT import *
import math

class Test:
    def __call__(self,x,y):
        return x,y

#Quadratic background function
def background(x, par):
  return par[0] + par[1]*x[0] + par[2]*x[0]*x[0];


#Lorentzian Peak function
def lorentzianPeak(x, par):
  return (0.5*par[0]*par[1]/math.pi) / max(math.e**-10,(x[0]-par[2])*(x[0]-par[2])+ .25*par[1]*par[1])

#Sum of background and peak function
def fitFunction(x, par):
  return background(x,par) + lorentzianPeak(x,par[3:])


#bevington exercise by P. Malzacher, modified by R. Brun
nBins = 60
data = [ 6, 1,10,12, 6,13,23,22,15,21,
23,26,36,25,27,35,40,44,66,81,
75,57,48,45,46,41,35,36,53,32,
40,37,38,31,36,44,42,37,32,32,
43,44,35,33,33,39,29,41,32,44,
26,39,29,35,32,21,21,15,25,15]
histo = TH1F("example_9_1","Lorentzian Peak on Quadratic Background",60,0,3)

for i in xrange(nBins):
  # we use these methods to explicitly set the content
  # and error instead of using the fill method.
  histo.SetBinContent(i+1,data[i])
  histo.SetBinError(i+1,math.sqrt(data[i]))

# create a TF1 with the range from 0 to 3 and 6 parameters
fitFcn = TF1("fitFcn",fitFunction,0,3,6)

# first try without starting values for the parameters
# this defaults to 1 for each param.
histo.Fit("fitFcn");
