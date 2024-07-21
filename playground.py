import dearpygui.dearpygui as dpg
import pyvista as pv
import numpy as np

reso = 50


# 创建球体
sphere = pv.Sphere(radius=1.0, center=(0, 0, 0), theta_resolution=reso,phi_resolution=reso)


# 创建立方体
cube = pv.Cube(center=(2, 0, 0))

# 创建圆柱体
cylinder = pv.Cylinder(radius=0.5, height=2.0, center=(-2, 0, 0),resolution=reso)


# 合并形状
combined = sphere + cube + cylinder



# 在z=0位置进行切片
#slice_z = combined.slice(normal='z', origin=(0, 0, 0))


# 获取切片后顶点坐标
#vertices = slice_z.points

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=600)

with dpg.window(label='main',width=600,height=600):
    dpg.add_text("plot control")
    with dpg.group():
        with dpg.plot():
            dpg.add_plot_axis(dpg.mvXAxis, label="", no_tick_labels=True)
            with dpg.plot_axis(dpg.mvYAxis, label="", no_tick_labels=True):
                pass
        slider = dpg.add_slider_float(min_value=-5.,max_value=5.,default_value=0.)



dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()