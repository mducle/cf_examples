from CrystalField import CrystalField, CrystalFieldFit

data_ws1 = Load('NdOs2Al10_5K35meV_Ecut_0to3ang_bp15V1.xye')

# Set up the crystal field model.
cf = CrystalField('Nd', 'C2v', Temperature=5, FWHM=1, 
    B20=0.19, B22=0.11, B40=-0.0004, B42=-0.002, B44=-0.012, B60=5.e-05, B62=0.00054, B64=-0.0006, B66=0.0008)
cf.PeakShape = 'Lorentzian'
cf.IntensityScaling = 2   # Scale factor if data is not in absolute units (mbarn/sr/f.u./meV), will be fitted.

# Runs the fit
fit = CrystalFieldFit(Model=cf, InputWorkspace=data_ws1,MaxIterations=200)
fit.fit()

# Plots the data and print fitted parameters
l=plotSpectrum('fit_Workspace',[0,1,2],error_bars=False)
l.activeLayer().setAxisScale(Layer.Left, 0, 100)
l.activeLayer().setAxisScale(Layer.Bottom, -10, 30)

for parnames in ['B20', 'B22','B40','B42', 'B44', 'B60','B62','B64','B66']:
    print parnames+' = '+str(fit.model[parnames])+' meV'

table = mtd['fit_Parameters']
print 'Cost function value = '+str(table.row(table.rowCount()-1)['Value'])
