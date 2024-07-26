import meep as mp
import numpy as np
import math
import matplotlib.pyplot as plt
cell_size = mp.Vector3(2,2,2)

# A hexagon is defined as a prism with six vertices centered on the origin
vertices = [mp.Vector3(-1,0),
            mp.Vector3(-0.5,math.sqrt(3)/2),
            mp.Vector3(0.5,math.sqrt(3)/2),
            mp.Vector3(1,0),
            mp.Vector3(0.5,-math.sqrt(3)/2),
            mp.Vector3(-0.5,-math.sqrt(3)/2)]

geometry = [mp.Prism(vertices, height=1.0, material=mp.Medium(index=3.5)),
            mp.Cone(radius=1.0, radius2=0.1, height=2.0, material=mp.air)]


sources = [mp.Source(mp.ContinuousSource(frequency=0.15),
                     component=mp.Ez,
                     center=mp.Vector3(0,0,0))]
r = 1.0  # radius of sphere

wvl_min = 2*np.pi*r/10
wvl_max = 2*np.pi*r/2
dpml = 0.5*wvl_max
pml_layers = [mp.PML(thickness=dpml)]


sim = mp.Simulation(resolution=50,
                    cell_size=cell_size,
                    boundary_layers=pml_layers,
                    sources= sources,

                    geometry=geometry)
mp.verbosity(0)



print(mp.simulation.Volume(size=(1,1,0)))
a = sim.plot2D(output_plane=mp.simulation.Volume(center=(0.5,0,0),size=(0,2,2)))
#plt.show()
class dum:
    def __init__(self,dpi):
        self.dpi = dpi
dummmy = dum(480)


fig = plt.gcf().get_figure().figimage(X=None).make_image(renderer=dummmy)

print(fig)