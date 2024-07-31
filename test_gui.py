import dearpygui.dearpygui as dpg
import global_vars
import numpy as np
import copy
from meep.geom import Medium,Vector3
import meep as mp
import array
import matplotlib.pyplot as plt
import gc
mp.verbosity(0)
from matplotlib._pylab_helpers import Gcf
plt.rcParams['figure.figsize'] = [3,3]
plt.rcParams['figure.dpi'] = 50
fig_resolution = 150

fdtd_resolution = 50

import var_manage as vm
global_vars.init()
from  global_vars import var_dict

def _help(message):
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("[!]", color=[0, 255, 0])
    with dpg.tooltip(t):
        dpg.add_text(message)

def update_sim_obj(updates):
    for attr,value in updates.items():
        if hasattr(var_dict['current_sim'],attr):
            setattr(var_dict['current_sim'], attr, value)



def reorder_obj(sender, app_data,user_data):
    target_pos = sender
    from_pos = user_data
    spacer_from_pos = from_pos - 2
    popup_from_pos = from_pos + 4

    name = dpg.get_item_label(dpg.get_item_children(from_pos)[1][0])
    #name = dpg.get_item_label(item)   

    spacer_row = dpg.table_row(parent="object list",height=-1,label=f'{name} spacer row',before=target_pos,)

    real_object_row = dpg.table_row(parent="object list",label=f'{name} object row',before=target_pos)
    with spacer_row:
        spacer_self = dpg.last_item()
        dpg.add_selectable(height=-1,drop_callback= lambda s, a :
                           reorder_obj(sender=dpg.get_item_parent(s), app_data=None, user_data= a)
                           )
    
    with real_object_row:
        last_row = dpg.last_item()
        dpg.add_selectable(label=f"{name}")
        shown_label = dpg.last_item()
        with dpg.drag_payload(parent=dpg.last_item(),drag_data=last_row):
            dpg.add_text(f"{name}")

        
        with dpg.popup(parent=shown_label):
            last_pop = dpg.last_container()
            #dpg.add_button(label=f"do it", callback=lambda: (dpg.delete_item(last_row),print("row del"), dpg.delete_item(last_pop),print("popup del")))

            dpg.add_menu_item(label="Delete",callback=lambda: (vm.rm_var(key=dpg.get_item_label(shown_label),
                                                                        dict=var_dict['geometry']),#print("dict del"),
                                                                        dpg.delete_item(last_row),#print("row del"),
                                                                        dpg.delete_item(last_pop),#print("popup del"),
                                                                        dpg.delete_item(spacer_self),
                                                                        update_all_geo(),
                                                                        update_all_view()
                                                                        ))
            dpg.add_menu_item(label="Edit",callback=obj_edit_func,user_data=shown_label)
            dpg.add_menu_item(label="more1")
            dpg.add_menu_item(label="more2")
    dpg.delete_item(from_pos)
    dpg.delete_item(popup_from_pos)
    dpg.delete_item(spacer_from_pos)

    shown_list = dpg.get_item_children('object list')[1]
    list_order_label = []
    for i in shown_list:
        item =dpg.get_item_label(dpg.get_item_children(i)[1][0])
        if item != "":
            list_order_label.append(item)


    
    var_dict['geometry'] = {k: var_dict['geometry'][k] for k in list_order_label}
    update_all_geo()
    update_all_view()
    print(f"dict new: {var_dict['geometry']}")





def add_obj(sender,app_data,user_data):

    object_add_window = dpg.window(
        label = "Main Window Add Object",
        width=400,
        modal=True,
        pos=(300,0)
    )
    
    with object_add_window:
        dpg.configure_item(dpg.last_root(),on_close=lambda: dpg.delete_item(dpg.last_root()))
        with dpg.group(horizontal=True):
            with dpg.group(horizontal=False):
                dpg.add_text("Name:")
                dpg.add_text("Strucutre:")
                dpg.add_text("Material:")
            with dpg.group(horizontal=False,width=200):
                obj_name_input = dpg.add_input_text(
                    label="",
                    default_value="new object",

            )
                def dum_print(sender,app_data,user_data):
                    main_add = user_data[0]
                    no_stru = user_data[1]
                    dpg.configure_item(main_add,enabled = True)
                    dpg.hide_item(no_stru)
                with dpg.group():
                    stru = dpg.add_combo(items=list(var_dict['structure'].keys()),default_value='REQUIRED',callback=dum_print,user_data=['main_add','no_stru_alert'])
                    _help(
                        "The structure of an object (e.g. Cylinder)\n"
                        "*MUST* be specified before creation of object.")
                material = dpg.add_combo(items=list(var_dict['material'].keys()),default_value='Air')

                def input_prepare(stru,input,mat):
                    last_win = dpg.last_root()
                        
                    print(dpg.get_value(input))
                    obj_add_func(sender=dpg.last_item(),
                                app_data=None,
                                user_data= [dpg.get_value(input),stru,mat]
                                )
                    dpg.delete_item(last_win)
                        
        no_structure_alert = dpg.tooltip(parent="main_add",tag='no_stru_alert')
        #print(dpg.get_value(stru), obj_name_input,dpg.get_value(material))
        dpg.add_button(label="add",tag='main_add',
                       callback=lambda: input_prepare(stru=dpg.get_value(stru),input=obj_name_input,mat=dpg.get_value(material)),
                       enabled= False,)
        
        with no_structure_alert:
            dpg.add_text('Structure must be specified.')

        # Update geometry 



def check_repeat(name, group):
    if name in group:
        new_name = name + '-c'
        a = check_repeat(name=new_name,group=group)
        return a
    else:
        return name
def update_all_geo():
    geo_obj_list= list(var_dict['geometry'].values())
    update_sim_obj({'geometry':geo_obj_list})

def obj_add_func(sender,app_data,user_data):
    name = user_data[0]
    print(name)
    stru = user_data[1]
    material = user_data[2]
    if stru in var_dict['structure']:
        temp_geo_class = copy.deepcopy(var_dict['structure'][stru])
        print(temp_geo_class.__dict__)
        temp_geo_class.material = var_dict['material'][material]
    if 'geometry' not in var_dict:
        var_dict.update({'geometry':{}})
    
    name = check_repeat(name=name, group=var_dict['geometry'])
    var_dict['geometry'].update({f'{name}':temp_geo_class})
    var_dict['geometry'][f'{name}'] = var_dict['geometry'].pop(f'{name}')
    print(var_dict['geometry'])

    update_all_geo()
    update_all_view()
    print(f"list after addition: {var_dict['current_sim'].geometry}")
        
    

    spacer_row = dpg.table_row(parent="object list",height=-1,tag=f'{name} spacer row',before='spacer')
    real_object_row = dpg.table_row(parent="object list",label=f"{name} object row",before='spacer')
    with spacer_row:
        spacer_self = dpg.last_item()
        dpg.add_selectable(height=-1,drop_callback= lambda s, a :
                           reorder_obj(sender=dpg.get_item_parent(s), app_data=None, user_data= a)
                           )
    with real_object_row:
        last_row = dpg.last_item()
        dpg.add_selectable(label=f"{name}")
        shown_label = dpg.last_item()
        with dpg.drag_payload(parent=dpg.last_item(),drag_data=last_row):
            dpg.add_text(f"{name}")

        
        with dpg.popup(parent=shown_label):
            last_pop = dpg.last_container()
            #dpg.add_button(label=f"do it", callback=lambda: (dpg.delete_item(last_row),print("row del"), dpg.delete_item(last_pop),print("popup del")))

            dpg.add_menu_item(label="Delete",callback=lambda: (vm.rm_var(key=dpg.get_item_label(shown_label),dict=var_dict['geometry']),print("dict del"),
                                                               dpg.delete_item(last_row),print("row del"),
                                                               dpg.delete_item(last_pop),print("popup del"),
                                                               dpg.delete_item(spacer_self),
                                                               update_all_geo(),update_all_view()
                                                               ))
            dpg.add_menu_item(label="Edit",callback=obj_edit_func,user_data=shown_label)
            dpg.add_menu_item(label="more1")
            dpg.add_menu_item(label="more2")

    
    



def reverse_dict(from_dict, find_val):
    key = next((k for k, v in from_dict.items() if v == find_val), None)
    return key







def obj_edit_func(sender,app_data,user_data):
    name = user_data
    name_label = dpg.get_item_label(name)

    if name_label in var_dict['geometry']:
        #print('i am in!')
        temp_geo = var_dict['geometry'][name_label]
    attr_dict = temp_geo.__dict__
    stru = type(var_dict['geometry'][name_label]).__name__

    print(f'new stru: {stru}')

    



    object_edit_window = dpg.window(
        label = "edit object",
        modal =True,
    )
    last_win = object_edit_window

    def save(item, value):
        label_in_list = item[0]
        combo_material = item[1]
        old_val = value[0]
        new_val = value[1]
        #print(f'old val: {old_val}, new val: {new_val}')

        temp_name_list = copy.deepcopy(var_dict['geometry'])
        del temp_name_list[old_val]
        gc.collect()

        #print(f"dict deleted: {var_dict['geometry']}")
        if new_val in temp_name_list:
            new_val = check_repeat(name=new_val,group=temp_name_list)
        else:
            pass
        material_key = dpg.get_value(combo_material)
        #print(material_key)
        if material_key == 'Empty':
            material_value = mp.air
        else:
            material_value = var_dict['material'][f'{material_key}']
        #print(material_value)

        """        
        listed_obj_ids = dpg.get_item_children(item='object list')[1]
        list_order_label = []
        for id in listed_obj_ids:
            select_id = id+1
            list_order_label.append(dpg.get_item_label(select_id))
        print(list_order_label)
        """

        temp_geo.material = material_value
        var_dict['geometry'].update({new_val:temp_geo})
        dpg.set_item_label(item=label_in_list,label=new_val)
        #var_dict['geometry'] = {k: var_dict['geometry'][k] for k in list_order_label}
        print(f"dict new: {var_dict['geometry']}")



    with object_edit_window:
        dpg.configure_item(dpg.last_root(), on_close=lambda: dpg.delete_item(dpg.last_root()))
        with dpg.group(horizontal=True):
            with dpg.group():
                dpg.add_text("Name:")
                
                #dpg.add_text("Material:")
                dpg.add_text("Structure:")


            with dpg.group():
                obj_name_input = dpg.add_input_text(
                    label="",
                    default_value= name_label,
                    )
                _help("Won't be updated automatically.")
                
                #obj_material = dpg.add_combo(items=list(var_dict['material'].keys()),default_value=temp_geo.material)
                obj_structure = dpg.add_text(
                    default_value=f"{stru}")
                print(temp_geo.material)
                
        with dpg.child_window(height = 300,width=500):
            
            with dpg.group(horizontal=True):
                keys = dpg.group()
                values = dpg.group()
                with keys:
                    for attrs in list(attr_dict.items()):
                        if attrs[0][0] == '_':
                            temp = attrs[0][1:]
                        else:
                            temp = attrs[0]
                        dpg.add_text(f"{temp}")

                with values:
                    with dpg.group():
                        for attrs in list(attr_dict.items()):
                                default_val = var_dict['geometry'][f'{name_label}'].__dict__[f'{attrs[0]}']
                                #print(f'{attrs[0]}')
                                def update(sender,app_data,user_data):
                                    #item = user_data[0]
                                    type = user_data[0]
                                    key = user_data[1]

                                    source_val = dpg.get_value(sender)
                                    #dpg.set_value(item=item,value=source_val[0:-1])
                                    if type == '3d':
                                        temp = source_val[0:-1]
                                        temp = Vector3(x= temp[0],
                                                       y= temp[1],
                                                       z= temp[2])
                                    elif sender == 'obj combo edit':
                                        temp =var_dict['material'][source_val]
                                        
                                    else:
                                        temp = source_val
                                    


                                    var_dict['geometry'][f'{name_label}'].__dict__[f'{key}'] = temp

                                    print(f"{key}:{var_dict['geometry'][f'{name_label}'].__dict__[f'{key}']}")
                                    print(var_dict['geometry'][f'{name_label}'].__dict__)
                                    update_all_geo()
                                    update_all_view()


                                    
                                    #print(f'{attrs[0]}:{source_val[0:-1]}')
                                
                                    
                                print(attrs[1])
                                if isinstance(attrs[1], Vector3):
                                    #print(attrs[0])

                                    #txt=dpg.add_text("dummy",tag=f'dum_{attrs[0]}',show= True)
                                    
                                    

                                    coord = dpg.add_drag_floatx(tag=f'slider_{name_label}_{attrs[0]}', 
                                                                min_value=-10,
                                                                max_value=10.0,
                                                                default_value=list(default_val),
                                                                size=3,
                                                                callback= update, user_data=['3d',attrs[0]])
                                            
                                    
                                    


                                elif isinstance(attrs[1], float):

                                    number = dpg.add_input_float(tag=f"{name_label}_{attrs[0]}",
                                                                 default_value=default_val,
                                                                 min_value=0.0,
                                                                 min_clamped = True,
                                                                 step=0.01,
                                                                 callback=update, user_data=[None,attrs[0]])
                                    #print("1")
                                elif attrs[0] == 'material':
                                    if default_val != 'Empty':
                                        default_val = reverse_dict(from_dict=var_dict['material'],find_val=default_val)
                                        print(default_val)
                                    else:
                                        default_val = 'Empty'

                                    obj_material = dpg.add_combo(items=list(var_dict['material'].keys()),default_value=default_val,
                                                                 callback=update,user_data=[None,attrs[0]],tag='obj combo edit')
                                    _help("Empty material will be saved as Air.")
                                else:
                                    dpg.add_text("TBD")              
                        #dpg.add_text(f"{attrs[1]}")
        def update_geometry():

            pass


        with dpg.group(horizontal=True):
            save_btn = dpg.add_button(
                label="Save",
                callback=lambda: (save(item=[name,obj_material],value=[dpg.get_item_label(name), dpg.get_value(obj_name_input),dpg.get_value(obj_material)]),
                                  dpg.delete_item(dpg.last_root()))
            )
            apply_btn = dpg.add_button(
                label="Apply",
                callback=lambda: (save(item=[name,obj_material],value=[dpg.get_item_label(name), dpg.get_value(obj_name_input),dpg.get_value(obj_material)]),
                                  ),

            )
    


dpg.create_context()

dpg.show_item_registry()




object_window = dpg.window(
    label="object window",
    tag="object window",
    width=300,
    height=600
)


object_list_table = dpg.table(
    label="object list",
    tag="object list",
    row_background=False,borders_innerH=True, borders_outerH=False, borders_innerV=False,borders_outerV=False,header_row=False

)


with object_window:
    title = dpg.add_text("Hello, this is object list!")
    btn1 = dpg.add_button(
        label= "add something!",
        tag="add objects",
        callback=add_obj,
    )
    
    with dpg.child_window():
        with object_list_table:
            dpg.add_table_column()
            with dpg.table_row(height=-1,tag='spacer'):
                dpg.add_selectable(drop_callback= lambda s, a :reorder_obj(sender=dpg.get_item_parent(s), app_data=None, user_data= a),height=-1)

        


def update_3d_plot():
    
    with dpg.window(
        no_title_bar= True,
        no_resize= True,
        no_close= True,
        modal= True,
        pos = (600,400),
        no_move= True,
        width=-1,
        height=-1,
        tag="temp_waiting",
        ):
        with dpg.group(horizontal=True):
            dpg.add_loading_indicator(label="Waiting...")
            dpg.add_text(default_value="VisPy Visualisation")
    var_dict['current_sim'].plot3D(frequency = var_dict['frequency'])
    plt.show()
    plt.close('all')
    dpg.delete_item('temp_waiting')


"""
source_window = dpg.window(
    label="source window",
    tag="source window",
    width=300,
    height=600,
    pos=(300,0)
)


source_list_table = dpg.table(
    label="source list",
    tag="source list",
    row_background=True,borders_innerH=True, borders_outerH=True, borders_innerV=True,borders_outerV=True

)


with source_window:
    title = dpg.add_text("Hello, this is source list!")
    btn1 = dpg.add_button(
        label= "add something!",
        tag="add source",
        callback=test_fun,
    )
    

    with source_list_table:
        dpg.add_table_column(label="Source list")

        
"""
view_window = dpg.window(
    label="view window",
    tag = "view window",


    pos=(300,50)
)


def update_plane(sender, norm, size):

    slider_pos = dpg.get_value(sender)

    norm = norm
    size = size

    center = norm*slider_pos
    center = np.array(var_dict['current_sim'].geometry_center) + center

    center = tuple(center)
    sim = var_dict['current_sim']
    sim.plot2D(output_plane=mp.simulation.Volume(size=size,center = center))
    plt.axis('off')
    plt.tight_layout(pad=0.0,h_pad=0.0,w_pad=0.0)

    active_figure = Gcf.get_all_fig_managers()[0]


    active_figure.canvas.draw()
    w,h = active_figure.canvas.get_width_height()
    buffer = np.frombuffer(active_figure.canvas.tostring_argb(), dtype=np.uint8)
    plt.close('all')
    buffer = buffer.reshape(h, w, 4)
    buffer = np.roll(buffer, 3, axis=2)
    antialiasing_thres = 200
    white_pixels = (buffer[..., 0] >= antialiasing_thres) & (buffer[..., 1] >= antialiasing_thres) & (buffer[..., 2] >= antialiasing_thres)
    buffer[white_pixels] = [0, 0, 0, 0]
    buffer = array.array('f',buffer.flatten()/255)

    if np.dot(norm, np.array([0,0,1])) == 1.:
            raw_data_xy[:] = buffer

    elif np.dot(norm, np.array([1,0,0])) == 1.:
            raw_data_yz[:] = buffer

    elif np.dot(norm, np.array([0,1,0])) == 1.:
            raw_data_xz[:] = buffer

def update_all_view():
    cell_size = var_dict['current_sim'].cell_size
    xspan = cell_size[0]
    yspan = cell_size[1]
    zspan = cell_size[2]
    update_plane(sender='yz_slice_in_xy_plane', norm = np.array([1,0,0]), size = (0,yspan,zspan))
    update_plane(sender='xy_slice_in_yz_plane', norm = np.array([0,0,1]), size = (xspan,yspan,0))
    update_plane(sender='xz_slice_in_xy_plane', norm = np.array([0,1,0]), size = (xspan,0,zspan))



def texture_generator(x,y):
    temp_data = []
    for i in range(x*y):
        temp_data.append(255 / 255)
        temp_data.append(255 / 255)
        temp_data.append(255 / 255)
        temp_data.append(0 / 255)
    return temp_data



with dpg.theme() as container_theme:


    with dpg.theme_component(dpg.mvPlot):
        dpg.add_theme_color(dpg.mvPlotCol_PlotBg, (255, 255, 255, 255), category=dpg.mvThemeCat_Plots)
        dpg.add_theme_color(dpg.mvPlotCol_XAxisGrid, (0, 0, 0, 150), category=dpg.mvThemeCat_Plots)
        dpg.add_theme_color(dpg.mvPlotCol_YAxisGrid, (0, 0, 0, 150), category=dpg.mvThemeCat_Plots)



with view_window as view:
        
    raw_data_xy = array.array('f',texture_generator(fig_resolution,fig_resolution))
    raw_data_yz = array.array('f',texture_generator(fig_resolution,fig_resolution))
    raw_data_xz = array.array('f',texture_generator(fig_resolution,fig_resolution))

    with dpg.texture_registry(show=False):
        dpg.add_raw_texture(width=fig_resolution, height=fig_resolution, default_value=raw_data_xy, format=dpg.mvFormat_Float_rgba, tag="texture_xy")
        dpg.add_raw_texture(width=fig_resolution, height=fig_resolution, default_value=raw_data_yz, format=dpg.mvFormat_Float_rgba, tag="texture_yz")
        dpg.add_raw_texture(width=fig_resolution, height=fig_resolution, default_value=raw_data_xz, format=dpg.mvFormat_Float_rgba, tag="texture_xz")
    with dpg.group():
        center = var_dict['current_sim'].geometry_center
        size = var_dict['current_sim'].cell_size

        x_max = center[0] + size[0]*0.5
        x_min = center[0] - size[0]*0.5
        y_max = center[1] + size[1]*0.5
        y_min = center[1] - size[1]*0.5
        z_max = center[2] + size[2]*0.5
        z_min = center[2] - size[2]*0.5

        with dpg.group(horizontal= True):
            with dpg.plot(label="XY Plane",height = 400,width=400):
                dpg.add_plot_axis(dpg.mvXAxis, label="x axis",tag='xy_x')
                dpg.set_axis_limits(axis='xy_x', ymax=x_max, ymin=x_min)
                with dpg.plot_axis(dpg.mvYAxis, label="y axis",tag='xy_y'):
                    dpg.set_axis_limits(axis='xy_y', ymax=y_max, ymin=y_min)
                    dpg.add_image_series(texture_tag="texture_xy",bounds_min=[-1,-1],bounds_max=[1,1])

                dpg.add_drag_line(label="yz slice", color=[255, 0, 0, 255],tag='yz_slice_in_xy_plane')
                dpg.add_drag_line(label="xz slice", color=[255, 0, 0, 255],tag='xz_slice_in_xy_plane',vertical= False)

            with dpg.plot(label="YZ Plane",height = 400,width=400):
                dpg.add_plot_axis(dpg.mvXAxis, label="y axis",tag='yz_y')
                dpg.set_axis_limits(axis='yz_y', ymax=y_max, ymin=y_min)
                with dpg.plot_axis(dpg.mvYAxis, label="z axis",tag='yz_z'):
                    dpg.set_axis_limits(axis='yz_z', ymax=z_max, ymin=z_min)
                    dpg.add_image_series(texture_tag="texture_yz",bounds_min=[-1,-1],bounds_max=[1,1])

                dpg.add_drag_line(label="xz slice", color=[255, 0, 0, 255],tag='xz_slice_in_yz_plane')
                dpg.add_drag_line(label="xy slice", color=[255, 0, 0, 255],tag='xy_slice_in_yz_plane',vertical= False)

        with dpg.group(horizontal= True):
            with dpg.plot(label="XZ Plane", height=400, width=400):
                dpg.add_plot_axis(dpg.mvXAxis, label="x axis",tag='xz_x')
                dpg.set_axis_limits(axis='xz_x', ymax=x_max, ymin=x_min)
                with dpg.plot_axis(dpg.mvYAxis, label="z axis",tag='xz_z'):
                    dpg.set_axis_limits(axis='xz_z', ymax=z_max, ymin=z_min)
                    dpg.add_image_series(texture_tag="texture_xz",bounds_min=[-1,-1],bounds_max=[1,1])

                dpg.add_drag_line(label="yz slice", color=[255, 0, 0, 255],tag='yz_slice_in_xz_plane')
                dpg.add_drag_line(label="xy slice", color=[255, 0, 0, 255],tag='xy_slice_in_xz_plane',vertical= False)
            dpg.add_button(label='3D view',callback=lambda: update_3d_plot())
            _help("DearPyGui have no 3D visualiser. 3D View is generated by Vispy.")


dpg.bind_item_theme(view, container_theme)              

main_window = dpg.window(
    label="main window",
    tag="main window",
    width=625,
    height=100, 
    pos=(300,0)
)
with main_window:
    title = dpg.add_text("Hello, this is main window")
    btn_obj = dpg.add_button(label="add object",callback=add_obj)
    dpg.add_button(label='get geometry',callback = lambda: update_sim_obj())


















dpg.create_viewport(title='MEEP_GUI', width=1440, height=900)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()


dpg.destroy_context()