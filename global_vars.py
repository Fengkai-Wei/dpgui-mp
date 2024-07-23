class dum_geo(object):
    def __init__(self,material=None,center = [0,0,0],eps_fun=None):
        self.material = material
        self.center = center
        self.eps_fun =eps_fun

class dum_cylinder(dum_geo):
    def __init__(self,material=None,center = [0.0,0.0,0.0],height=1.0,raidus=1.0,axis=[0.0,0.0,0.0],eps_fun=None):
        super().__init__(material,center,eps_fun)
        self.height = height
        self.radius = raidus
        self.axis = axis
        self.material = material
        self.center = center
        self.eps_fun =eps_fun

class dum_block(dum_geo):
    def __init__(self,material=None,center = [0.0,0.0,0.0],size=[0.0,0.0,0.0],eps_fun=None):
        super().__init__(material,center,eps_fun)
        self.size = size
        self.material = material
        self.center = center
        self.eps_fun = eps_fun
import meep as mp
from meep.materials import SiO2,cSi,Al
#a= dum_geo()
#print(a.center)
def init():
    global var_dict
    var_dict = {
        'material':{'c-Si':cSi,
                    'Al':Al,
                    'SiO2':SiO2,
                    'Air':mp.Medium(epsilon=1.0)},

        'structure':{
            #'Cylinder': dum_cylinder(),
            #'Block': dum_block(),
            'Cylinder': mp.Cylinder(radius=0.0,height=1.0),
            'Block': mp.Block(size=(0,0,0)),
                     }
                }
