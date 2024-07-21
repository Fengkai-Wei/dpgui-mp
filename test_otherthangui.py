import pyvista as pv
import numpy as np
import time

reso = 50
start_time = time.time()

# 创建球体
sphere = pv.Sphere(radius=1.0, center=(0, 0, 0), theta_resolution=reso,phi_resolution=reso)

time_sphere = time.time()

# 创建立方体
cube = pv.Cube(center=(2, 0, 0))
time_cube = time.time()
# 创建圆柱体
cylinder = pv.Cylinder(radius=0.5, height=2.0, center=(-2, 0, 0),resolution=reso)
time_cylinder = time.time()

# 合并形状
combined = sphere + cube + cylinder
time_combine = time.time()


# 在z=0位置进行切片
slice_z = combined.slice(normal='z', origin=(0, 0, 0))
slice_time = time.time()

# 获取切片后顶点坐标
vertices = slice_z.points

get_ver_time = time.time()

print(f'resolution = {reso}')
print(f'create sphere : {time_sphere - start_time}')
print(f'create cube : {time_cube - time_sphere}')
print(f'create cylinder : {time_cylinder - time_cube}')
print(f'combine shape: {time_combine - time_cylinder}')
print(f'create slice : {slice_time - time_combine}')
print(f'get vertices : {get_ver_time - slice_time}')

"""# 打印顶点坐标
print("Slice at z=0 coordinates:")
print(vertices)"""

# 可视化原始组合体和切片
plotter = pv.Plotter(shape=(1, 2))

# 添加原始组合体
plotter.subplot(0, 0)
plotter.add_mesh(combined, color='white', show_edges=True, opacity=0.5)
plotter.add_text('Combined Shape', font_size=10)

# 添加切片
plotter.subplot(0, 1)
plotter.add_mesh(slice_z, color='red', show_edges=True)
plotter.add_text('Slice at z=0', font_size=10)

# 显示结果
plotter.show()