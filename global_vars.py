class dum_geo(object):
    def __init__(self,material=None,center = [0,0,0],eps_fun=None):
        self.material = material
        self.center = center
        self.eps_fun =eps_fun

class dum_cylinder(dum_geo):
    def __init__(self,material=None,center = [0,0,0],eps_fun=None,height=1,raidus=1,axis=[0,0,0]):
        super().__init__(material,center,eps_fun)
        self.height = height
        self.radius = raidus
        self.axis = axis
        self.material = material
        self.center = center
        self.eps_fun =eps_fun

class dum_block(dum_geo):
    def __init__(self,material=None,center = [0,0,0],eps_fun=None,size=[0,0,0]):
        super().__init__(material,center,eps_fun)
        self.size = size
        self.material = material
        self.center = center
        self.eps_fun = eps_fun

def init():
    global var_dict
    var_dict = {
        'material':{'Si':'Silicon','Al':'Aluminium','SiO2':'Silicon Dioxide'},
        'structure':{
            'Cylinder': dum_cylinder(),
            'Block': dum_block(),
                     }
                }
