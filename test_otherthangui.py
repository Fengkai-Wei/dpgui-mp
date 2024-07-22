import pyvista as pv
import numpy as np
import time

reso = 15


# 创建球体
#sphere = pv.Sphere(radius=1.0, center=(0, 0, 0), theta_resolution=reso,phi_resolution=reso)



# 创建立方体
cube = pv.Cube(center=(2, 0, 0))

# 创建圆柱体
#cylinder = pv.Cylinder(radius=0.5, height=2.0, center=(-2, 0, 0),resolution=reso)

# 合并形状
#combined = sphere + cube + cylinder



# 在z=0位置进行切片
#slice_z = combined.slice(normal='z', origin=(0, 0, 0))

# 获取切片后顶点坐标
#vertices = slice_z.points


"""# 打印顶点坐标
print("Slice at z=0 coordinates:")
print(vertices)"""

def pv2dpg_slice(norm, sliced_points):
    old_arr = np.array(sliced_points)
    new_arr = np.delete(old_arr, norm, 1)
    print(new_arr)
    print(new_arr.transpose())



pv2dpg_slice(norm = 2,sliced_points = cube.slice(normal='z', origin=(0, 0, 0)).points)