import meep as mp
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['savefig.pad_inches'] = 0
cell_size = mp.Vector3(5,5,5)
#plt.switch_backend('agg')
# A hexagon is defined as a prism with six vertices centered on the origin
vertices = [mp.Vector3(-1,0),
            mp.Vector3(-0.5,math.sqrt(3)/2),
            mp.Vector3(0.5,math.sqrt(3)/2),
            mp.Vector3(1,0),
            mp.Vector3(0.5,-math.sqrt(3)/2),
            mp.Vector3(-0.5,-math.sqrt(3)/2)]

geometry = [mp.Prism(vertices, height=1.0, material=mp.Medium(index=10)),
            mp.Cone(radius=1.0, radius2=0.1, height=2.0, material=mp.Medium(index = 2.6))]


sources = [mp.Source(mp.ContinuousSource(frequency=0.15),
                     component=mp.Ez,
                     center=mp.Vector3(0,0,0))]
r = 1.0  # radius of sphere

wvl_min = 2*np.pi*r/10
wvl_max = 2*np.pi*r/2
dpml = 0.3*wvl_max
pml_layers = [mp.PML(thickness=dpml)]


sim = mp.Simulation(resolution=50,
                    cell_size=cell_size,
                    boundary_layers=pml_layers,
                    sources= sources,

                    geometry=geometry
                    )
mp.verbosity(0)
plt.close()
from matplotlib.transforms import Bbox
mpl.rcParams['figure.figsize'] = [2,2]
mpl.rcParams['figure.dpi'] = 150

#print(mp.simulation.Volume(size=(1,1,0)))
a = sim.plot2D(output_plane=mp.simulation.Volume(center=(0,0,0),size=(0,5,5)))
plt.rcParams['savefig.dpi'] = 50
from matplotlib._pylab_helpers import Gcf
plt.axis('off')
plt.tight_layout(pad = .0,w_pad = .0,h_pad=.0)
plt.autoscale(tight=True)


activefig = Gcf.get_all_fig_managers()[0]
a = activefig.canvas
a.draw()

w,h = a.get_width_height()
data = np.frombuffer(a.tostring_argb(),dtype=np.uint8).reshape(h,w,4)
buffer = np.roll(data,3,axis=2)

white_pixels = (buffer[..., 0] == 255) & (buffer[..., 1] == 255) & (buffer[..., 2] == 255)
buffer[white_pixels] = [0, 0, 0, 0] 


plt.imsave('testconvert.png',buffer)

plt.show()