
import pyvista as pv
import numpy as np

# 创建球体
sphere = pv.Sphere(radius=1.0, center=(0, 0, 0))

# 创建立方体
cube = pv.Cube(center=(2, 0, 0))

# 创建圆柱体
cylinder = pv.Cylinder(radius=0.5, height=2.0, center=(-2, 0, 0))

# 合并形状
combined = sphere + cube + cylinder

# 在z=0位置进行切片
slice_z = combined.slice(normal='z', origin=(0, 0, 0))


# 可视化原始组合体和切片
plotter = pv.Plotter(window_size=(300,300))
plotter.add_axes()

plotter.add_mesh(combined,color='red', show_edges=False)
plotter.camera_position = [(0.5, 0, 0), (0, 0, 0), (1, 1, 1)]
#img = plotter.screenshot()
plotter.show()


