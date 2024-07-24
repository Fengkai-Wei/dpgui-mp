import dearpygui.dearpygui as dpg
import pyvista as pv
import pyvistaqt as pvqt
import numpy as np
import array
import os, shutil
import cairosvg

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
plotter =  pvqt.BackgroundPlotter(window_size=(500,500))
plotter.add_axes()

plotter.add_mesh(combined,color='red', show_edges=False)
plotter.camera_position = [(0.5, 0, 15), (0, 0, 0), (1, 1, 1)]
plotter.screenshot('texture.png')

def update_position(plotter = plotter):
    pos = dpg.get_value('slider')
    plotter.camera_position = [(0.5, 0, pos), (0, 0, 0), (1, 1, 1)]

    os.remove("texture.png")
    plotter.save_graphic('img.svg')
    cairosvg.svg2png(url='img.svg', write_to = 'texture.png')


    #width, height, channels, data = dpg.load_image("texture.png")
    #dpg.delete_item('img')
    #dpg.delete_item('img_reg')
    print('delete')
    #with dpg.texture_registry(show=False,tag = 'img_reg'):
        #dpg.add_raw_texture(width=width, height=height, default_value=data, tag="texture_tag")

    #dpg.add_image("texture_tag",tag='img',before='slider')




dpg.create_context()

width, height, channels, data = dpg.load_image("texture.png")

with dpg.texture_registry(show=False,tag = 'img_reg'):
    dpg.add_raw_texture(width=width, height=height, default_value=data, tag="texture_tag")

with dpg.window(label="Tutorial"):
    dpg.add_image("texture_tag",tag='img')
    dpg.add_slider_float(min_value=-10,max_value=40,default_value=15,callback=lambda: update_position(),tag='slider')


dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()