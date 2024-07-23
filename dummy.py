import numpy as np
import meep as mp
from meep.geom import Vector3
from meep.materials import Al,SiO2
c = mp.Block(size=(4,2,2))
a = mp.Cylinder(radius=0.02,material = Al)
b = mp.Cylinder(material=mp.Medium(index= 2.0),
                        center=mp.Vector3(),
                        radius=0.05,
                        height=mp.inf)
print(Vector3([0,0,0]))