from CrystalField import CrystalField, CrystalFieldFit, Background, Function, ResolutionModel
from PyChop import PyChop2

# load the data
data_ws1 = Load('MER38435_10p22meV.txt')
data_ws2 = Load('MER38436_10p22meV.txt')

# Sets up a resolution function
merlin = PyChop2('MERLIN', 'G', 250.)
merlin.setEi(10.)
resmod = ResolutionModel(merlin.getResolution, xstart=-10, xend=9.0, accuracy=0.01)

Kelvin_to_meV = 1./11.6

# Parameters from https://doi.org/10.1016/0921-4526(91)90575-Y
lit_par = {'B20': -.27, 'B22': -.34, 'B40':1e-6, 'B42':0.04158, 'B44':0.01369, 'B60':0.112e-3, 'B62':0.4185e-3, 'B64':-0.555e-3, 'B66':0.588e-3} # K
for parameter in lit_par.keys():
      lit_par[parameter] *= Kelvin_to_meV

# Set up the crystal field model.
cf = CrystalField('Ho', 'D2', Temperature=[55,159], FWHM=0.3, **lit_par)
cf.PeakShape = 'Lorentzian'
cf.IntensityScaling = [0.2, 0.2]   # Scale factor if data is not in absolute units (mbarn/sr/f.u./meV), will be fitted.
cf.background = Background(peak=Function('Gaussian', Height=700, Sigma=0.4/2.3))
cf.ResolutionModel = [resmod, resmod]

# Runs the fit
fit = CrystalFieldFit(Model=cf, InputWorkspace=[data_ws3, data_ws4],MaxIterations=2000, Output='Fit_159K')
fit.fit()
