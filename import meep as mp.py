import meep as mp
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
from meep.materials import SiO2,cSi,Al,aSi
wvl_min = 0.01 # units of μm
wvl_max = 0.07 # units of μm
nwvls = 21
wvls = np.linspace(wvl_min, wvl_max, nwvls)

Al_epsilon = np.array([Al.epsilon(1/w)[0][0] for w in wvls])

plt.subplot(1,2,1)
plt.plot(wvls,np.real(Al_epsilon),'bo-')
plt.xlabel('wavelength (μm)')
plt.ylabel('real(ε)')

plt.subplot(1,2,2)
plt.plot(wvls,np.imag(Al_epsilon),'ro-')
plt.xlabel('wavelength (μm)')
plt.ylabel('imag(ε)')

plt.suptitle('Al from Meep materials library')
plt.subplots_adjust(wspace=0.4)
plt.show()