import matplotlib.pyplot as plt
import dearpygui.dearpygui as dpg
import numpy as np
import meep as mp
import array
import math
import matplotlib as mpl
from matplotlib._pylab_helpers import Gcf
plt.rcParams['figure.figsize'] = [3,3]
plt.rcParams['figure.dpi'] = 50
def _help(message):
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("[!]", color=[0, 255, 0])
    
    with dpg.tooltip(t):
        dpg.add_text(message)



dpg.create_context()
dpg.create_viewport(title='Custom Title', width=1280, height=900)
mp.verbosity(0)


dpg.show_item_registry()




def update_plane(sender, norm, size):

    slider_pos = dpg.get_value(sender)

    norm = norm
    size = size

    center = norm*slider_pos
    center = np.array(sim.geometry_center) + center
    #print(center)
    center = tuple(center)

    temp = sim.plot2D(output_plane=mp.simulation.Volume(size=size,center = center))
    plt.axis('off')
    plt.tight_layout(pad=0.0,h_pad=0.0,w_pad=0.0)

    active_figure = Gcf.get_all_fig_managers()[0]


    active_figure.canvas.draw()
    w,h = active_figure.canvas.get_width_height()
    buffer = np.frombuffer(active_figure.canvas.tostring_argb(), dtype=np.uint8)
    plt.close('all')
    buffer = buffer.reshape(h, w, 4)
    buffer = np.roll(buffer, 3, axis=2)
    plt.imsave(fname='testconvert.png',arr=buffer)
    thres = 200
    
    white_pixels = (buffer[..., 0] >= thres) & (buffer[..., 1] >= thres) & (buffer[..., 2] >= thres)
    buffer[white_pixels] = [0, 0, 0, 0]
    

    buffer = array.array('f',buffer.flatten()/255)

    if np.dot(norm, np.array([0,0,1])) == 1.:
            raw_data_xy[:] = buffer

            pass
            """
            for i in range (300 * 300 * 4):

            # R
            if i % 4 == 0:
                raw_data_xy[i] = buffer[i]/255

            # G
            elif i % 4 == 1:
                raw_data_xy[i] = buffer[i]/255
            # B
            elif i % 4 == 2:
                raw_data_xy[i] = buffer[i]/255
            #A
            elif i % 4 == 3:
                raw_data_xy[i] = buffer[i]/255
            """
        
    elif np.dot(norm, np.array([1,0,0])) == 1.:
            raw_data_yz[:] = buffer
            """        
            for i in range (300 * 300 * 4):

                # R
                if i % 4 == 0:
                    raw_data_yz[i] = buffer[i]/255

                # G
                elif i % 4 == 1:
                    raw_data_yz[i] = buffer[i]/255
                # B
                elif i % 4 == 2:
                    raw_data_yz[i] = buffer[i]/255
                #A
                elif i % 4 == 3:
                    raw_data_yz[i] = buffer[i]/255
            """

    elif np.dot(norm, np.array([0,1,0])) == 1.:
            raw_data_xz[:] = buffer
            """        
            for i in range (300 * 300 * 4):

            # R
            if i % 4 == 0:
                raw_data_xz[i] = buffer[i]/255

            # G
            elif i % 4 == 1:
                raw_data_xz[i] = buffer[i]/255
            # B
            elif i % 4 == 2:
                raw_data_xz[i] = buffer[i]/255
            #A
            elif i % 4 == 3:
                raw_data_xz[i] = buffer[i]/255"""

        


cell_size = mp.Vector3(2,2,2)
from meep.materials import aSi
# A hexagon is defined as a prism with six vertices centered on the origin
vertices = [mp.Vector3(-1,0),
            mp.Vector3(-0.5,math.sqrt(3)/2),
            mp.Vector3(0.5,math.sqrt(3)/2),
            mp.Vector3(1,0),
            mp.Vector3(0.5,-math.sqrt(3)/2),
            mp.Vector3(-0.5,-math.sqrt(3)/2)]

geometry = [mp.Prism(vertices, height=1.0, material=mp.Medium(index=3.5)),
            mp.Cone(radius=1.0, radius2=0.1, height=2.0, material=mp.Medium(index=2.5)),
            mp.Block(size=(0.2,0.2,3),material = mp.Medium(epsilon= 0.9))
            ]


sources = [mp.Source(mp.ContinuousSource(frequency=0.15),
                     component=mp.Ez,
                     center=mp.Vector3(0,0,0),size=(0.1,0.1,0.1))]
r = 1.0  # radius of sphere

wvl_min = 2*np.pi*r/10
wvl_max = 2*np.pi*r/2
dpml = 0.05*wvl_max
pml_layers = [mp.PML(thickness=dpml)]


sim = mp.Simulation(resolution=50,
                    cell_size=cell_size,
                    boundary_layers=pml_layers,
                    sources= sources,

                    geometry=geometry,
                    )
mp.verbosity(0)

def texture_generator(x,y):
    temp_data = []
    for i in range(x*y):
        temp_data.append(255 / 255)
        temp_data.append(255 / 255)
        temp_data.append(255 / 255)
        temp_data.append(0 / 255)
    return temp_data


with dpg.window(label='main',width=1280,height=900) as win: 

    raw_data_xy = array.array('f',texture_generator(150,150))
    raw_data_yz = array.array('f',texture_generator(150,150))
    raw_data_xz = array.array('f',texture_generator(150,150))


    with dpg.texture_registry(show=False):
        dpg.add_raw_texture(width=150, height=150, default_value=raw_data_xy, format=dpg.mvFormat_Float_rgba, tag="texture_xy")
        dpg.add_raw_texture(width=150, height=150, default_value=raw_data_yz, format=dpg.mvFormat_Float_rgba, tag="texture_yz")
        dpg.add_raw_texture(width=150, height=150, default_value=raw_data_xz, format=dpg.mvFormat_Float_rgba, tag="texture_xz")
    with dpg.group(horizontal=True):
        with dpg.group():

            with dpg.group():
                with dpg.plot(label="Image Plot", height=400, width=400):
                    
                    dpg.add_plot_axis(dpg.mvXAxis, label="x axis")
                    with dpg.plot_axis(dpg.mvYAxis, label="y axis"):
                        
                        dpg.add_image_series(texture_tag="texture_xy",bounds_min=[-1,-1],bounds_max=[1,1])

                    dpg.add_drag_line(label="yz slice", color=[255, 0, 0, 255],tag='yz_slice_in_xy_plane')
                    dpg.configure_item(item='yz_slice_in_xy_plane', callback = lambda: (update_plane(sender='yz_slice_in_xy_plane', norm = np.array([1,0,0]), size = (0,2,2)),
                                                                                        dpg.set_value(item='yz_slice_in_xz_plane',value=dpg.get_value(item='yz_slice_in_xy_plane'))))
                    dpg.add_drag_line(label="xz slice", color=[255, 0, 0, 255],tag='xz_slice_in_xy_plane',vertical= False)
                    dpg.configure_item(item='xz_slice_in_xy_plane', callback = lambda: (update_plane(sender='xz_slice_in_xy_plane', norm = np.array([0,1,0]), size = (2,0,2)),
                                                                                        dpg.set_value(item='xz_slice_in_yz_plane',value=dpg.get_value(item='xz_slice_in_xy_plane'))))


            #slider = dpg.add_slider_float(width= 300,min_value=-2.,max_value=2.,default_value=0.0,callback=update_plane,user_data=[3.5*3.5,np.array([0,0,1]),(2,2,0)],label="z position")
        
        with dpg.group():
            with dpg.group():
                with dpg.plot(label="Image Plot", height=400, width=400):
                    dpg.add_plot_axis(dpg.mvXAxis, label="y axis")
                    with dpg.plot_axis(dpg.mvYAxis, label="z axis"):
                        dpg.add_image_series(texture_tag="texture_yz",bounds_min=[-1,-1],bounds_max=[1,1])
            
                    dpg.add_drag_line(label="xz slice", color=[255, 0, 0, 255],tag='xz_slice_in_yz_plane')
                    dpg.configure_item(item='xz_slice_in_yz_plane', callback = lambda: (update_plane(sender='xz_slice_in_yz_plane', norm = np.array([0,1,0]), size = (2,0,2)),
                                                                                        dpg.set_value(item='xz_slice_in_xy_plane',value=dpg.get_value(item='xz_slice_in_yz_plane'))))
                    dpg.add_drag_line(label="xy slice", color=[255, 0, 0, 255],tag='xy_slice_in_yz_plane',vertical= False)
                    dpg.configure_item(item='xy_slice_in_yz_plane', callback = lambda: (update_plane(sender='xy_slice_in_yz_plane', norm = np.array([0,0,1]), size = (2,2,0)),
                                                                                        dpg.set_value(item='xy_slice_in_xz_plane',value=dpg.get_value(item='xy_slice_in_yz_plane'))))

            #slider = dpg.add_slider_float(width= 300,min_value=-2.,max_value=2.,default_value=0.0,callback=update_plane,user_data=[3.5*3.5,np.array([1,0,0]),(0,2,2)],label='x position')


    with dpg.group(horizontal=True):
        with dpg.group():
            with dpg.group():
                with dpg.plot(label="Image Plot", height=400, width=400):
                    dpg.add_plot_axis(dpg.mvXAxis, label="x axis")
                    with dpg.plot_axis(dpg.mvYAxis, label="z axis"):
                        dpg.add_image_series(texture_tag="texture_xz",bounds_min=[-1,-1],bounds_max=[1,1])

                    dpg.add_drag_line(label="yz slice", color=[255, 0, 0, 255],tag='yz_slice_in_xz_plane')
                    dpg.configure_item(item='yz_slice_in_xz_plane', callback = lambda: (update_plane(sender='yz_slice_in_xz_plane', norm = np.array([1,0,0]), size = (0,2,2)),
                                                                                        dpg.set_value(item='yz_slice_in_xy_plane',value=dpg.get_value(item='yz_slice_in_xz_plane'))))
                    dpg.add_drag_line(label="xy slice", color=[255, 0, 0, 255],tag='xy_slice_in_xz_plane',vertical= False)
                    dpg.configure_item(item='xy_slice_in_xz_plane', callback = lambda: (update_plane(sender='xy_slice_in_xz_plane', norm = np.array([0,0,1]), size = (2,2,0)),
                                                                                        dpg.set_value(item='xy_slice_in_yz_plane',value=dpg.get_value(item='xy_slice_in_xz_plane'))))        


            #slider = dpg.add_slider_float(width= 300,min_value=-2.,max_value=2.,default_value=0.0,callback=update_plane,user_data=[3.5*3.5,np.array([0,1,0]),(2,0,2)],label='y position')

        dpg.add_button(label='3D view',callback=lambda: update_3d_plot())
        _help("DearPyGui have no 3D visualiser. 3D View is generated by Vispy.")
        

        
def update_3d_plot():
    sim.plot3D()
    plt.show()


with dpg.theme() as container_theme:


    with dpg.theme_component(dpg.mvPlot):
        dpg.add_theme_color(dpg.mvPlotCol_PlotBg, (255, 255, 255, 255), category=dpg.mvThemeCat_Plots)
        dpg.add_theme_color(dpg.mvPlotCol_XAxisGrid, (0, 0, 0, 150), category=dpg.mvThemeCat_Plots)
        dpg.add_theme_color(dpg.mvPlotCol_YAxisGrid, (0, 0, 0, 150), category=dpg.mvThemeCat_Plots)


dpg.bind_item_theme(win, container_theme)







dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()

dpg.destroy_context()