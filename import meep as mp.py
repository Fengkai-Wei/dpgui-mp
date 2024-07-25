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

sim = mp.Simulation(resolution=50,
                    cell_size=cell_size,
                    geometry=geometry)
print(mp.simulation.Volume(size=(1,1,0)))
a = sim.plot2D(output_plane=mp.simulation.Volume(size=(2,2,0)))
num = plt.get_fignums()
print(num)
data = a.get_images()[0].get_array().data
print(data)

