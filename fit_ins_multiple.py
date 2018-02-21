from CrystalField import CrystalField, CrystalFieldFit

data_ws1=Load('cecuga3Mlacuga3_15meV5K0to2p5angbp2V1.xye')
data_ws2=Load('cecuga3Mlacuga3fp824_15meV50K0to2p5angbp2V1.xye')
data_ws3=Load('cecuga3Mlacuga3fp824_15meV100K0to2p5angbp2V1.xye')

# Set up the crystal field model for multiple spectra.
# This is indicated by the number of elements in the list of temperatures. 
# Optionally other parameters like FWHM and IntensityScaling can be lists if these initial parameters for each
#    spectra should differ.
cf = CrystalField('Ce', 'C4v', Temperature=[5,50,100], FWHM=[1,1,1], B20=0.0633, B40=0.01097, B44=0.09985)
cf.PeakShape = 'Lorentzian'
cf.IntensityScaling = [2, 2, 2]   # Scale factor if data is not in absolute units (mbarn/sr/f.u./meV), will be fitted.

# Runs the fit
fit = CrystalFieldFit(Model=cf, InputWorkspace=[data_ws1, data_ws2, data_ws3], MaxIterations=200)
fit.fit()

# Plots the data and print fitted parameters
l=plotSpectrum('fit_Workspace_0', [0,1,2], error_bars=False)
l.activeLayer().setAxisScale(Layer.Left, 0, 20)
l.activeLayer().setAxisScale(Layer.Bottom, -10, 15)
l=plotSpectrum('fit_Workspace_1', [0,1,2], error_bars=False)
l.activeLayer().setAxisScale(Layer.Left, 0, 20)
l.activeLayer().setAxisScale(Layer.Bottom, -10, 15)
l=plotSpectrum('fit_Workspace_2', [0,1,2], error_bars=False)
l.activeLayer().setAxisScale(Layer.Left, 0, 20)
l.activeLayer().setAxisScale(Layer.Bottom, -10, 15)

# Prints output parameters and cost function.
for parnames in ['B20', 'B40','B44']:
    print parnames+' = '+str(fit.model[parnames])+' meV'
table = mtd['fit_Parameters']
print 'Cost function value = '+str(table.row(table.rowCount()-1)['Value'])
