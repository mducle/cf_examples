from CrystalField import CrystalField, CrystalFieldFit, PhysicalProperties
import matplotlib.pyplot as plt

sus_a = Load('NdOs2Al10_sus_a.txt')
sus_b = Load('NdOs2Al10_sus_b.txt')
sus_c = Load('NdOs2Al10_sus_c.txt')

cf = CrystalField('Nd', 'C2v', 
    B20=0.19, B22=0.11, B40=-0.0004, B42=-0.002, B44=-0.012, B60=5.e-05, B62=0.00054, B64=-0.0006, B66=0.0008)

# Simultaneously fit data measured in a, b and c directions
cf.PhysicalProperty = [
     PhysicalProperties('susc', Hdir=[1,0,0], Inverse=True, Unit='cgs'),
     PhysicalProperties('susc', Hdir=[0,1,0], Inverse=True, Unit='cgs'),
     PhysicalProperties('susc', Hdir=[0,0,1], Inverse=True, Unit='cgs')]

fit = CrystalFieldFit(Model=cf, InputWorkspace=[sus_a, sus_b, sus_c], MaxIterations=100, Output='fit_susc')
fit.fit()

# Print fitted parameters and plot results
blm={}
for parname in ['B20','B22', 'B40', 'B42', 'B44','B60','B62','B64','B66']:
    blm[parname] = cf[parname]
    print parname+"="+str(cf[parname])
calc_a = mtd['fit_susc_Workspaces'][0]
calc_b = mtd['fit_susc_Workspaces'][1]
calc_c = mtd['fit_susc_Workspaces'][2]
plt.plot(calc_a.readX(1),calc_a.readY(1),'-k',label='$\chi^a$ Fit')
plt.plot(mtd['sus_a'].readX(0),mtd['sus_a'].readY(0),'ok',label='$\chi^a$ Data')
plt.plot(calc_b.readX(1),calc_b.readY(1),'-b',label='$\chi^b$ Fit')
plt.plot(mtd['sus_b'].readX(0),mtd['sus_b'].readY(0),'ob',label='$\chi^b$ Data')
plt.plot(calc_c.readX(1),calc_c.readY(1),'-r',label='$\chi^c$ Fit')
plt.plot(mtd['sus_c'].readX(0),mtd['sus_c'].readY(0),'or',label='$\chi^c$ Data')
plt.legend(loc='upper left')
plt.xlabel('Temperature (K)')
plt.ylabel('Inverse Susceptibility (mol/emu)')
plt.show()
