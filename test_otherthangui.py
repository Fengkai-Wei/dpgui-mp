class dum_geo(object):
    def __init__(self,material,center,eps_fun=None):
        self.material = material
        self.center = center
        self.eps_fun =eps_fun

class dum_cylinder(dum_geo):
    def __init__(self,material,center,eps_fun,height,raidus,axis):
        super().__init__(material,center,eps_fun)
        self.height = height
        self.radius = raidus
        self.axis = axis
        self.material = material
        self.center = center
        self.eps_fun =eps_fun

class dum_block(dum_geo):
    def __init__(self,material,center,eps_fun,size):
        super().__init__(material,center,eps_fun)
        self.size = size
        self.material = material
        self.center = center
        self.eps_fun = eps_fun

b = dum_block(material=121,center=3232,eps_fun='w22w',size=123)
a = dum_geo(material=1212,center=1313)
print(a.eps_fun)