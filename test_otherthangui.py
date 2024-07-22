import pyvista as pv
import numpy as np
import time

reso = 15


# 创建球体
sphere = pv.Sphere(radius=1.0, center=(0, 0, 0), theta_resolution=reso,phi_resolution=reso)



# 创建立方体
cube = pv.Cube(center=(2, 0, 0))

# 创建圆柱体
cylinder = pv.Cylinder(radius=0.5, height=2.0, center=(-2, 0, 0),resolution=reso)

# 合并形状
combined = sphere + cube + cylinder

def sort_vertices(vertices):
    # 计算质心
    centroid = np.mean(vertices, axis=0)
    
    # 计算每个顶点相对于质心的角度
    def angle_from_centroid(vertex):
        return np.arctan2(vertex[1] - centroid[1], vertex[0] - centroid[0])
    
    # 对顶点按角度进行排序
    sorted_vertices = sorted(vertices, key=angle_from_centroid)
    return np.array(sorted_vertices)

def vista2dpg_plot(sliced_list :list, norm):

    sorted_list = []
    for sliced_points in sliced_list:
        flatten  = np.delete(arr=sliced_points, obj= norm,axis= 1)
        sorted = sort_vertices(flatten)
        
        sorted_list.append(sorted.transpose().tolist())
    return sorted_list
    
a = vista2dpg_plot([cylinder.slice(normal='z', origin=(0, 0, 0)).points],2)
print(a)