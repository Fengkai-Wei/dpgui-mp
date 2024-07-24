import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import time
import global_vars
import numpy as np
import copy
from meep.geom import Medium,Vector3

import var_manage as vm
global_vars.init()
from  global_vars import var_dict, dum_geo,dum_block,dum_cylinder

def _help(message):
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("[!]", color=[0, 255, 0])
    with dpg.tooltip(t):
        dpg.add_text(message)




def reorder_obj(sender, app_data,user_data):
    target_pos = sender
    from_pos = user_data
    spacer_from_pos = from_pos - 2

    name = dpg.get_item_label(dpg.get_item_children(from_pos)[1][0])
    #name = dpg.get_item_label(item)

    real_object_row = dpg.table_row(parent="object list",before=target_pos)
    dpg.add_table_row(parent="object list",height=-1,before=target_pos)
    dpg.add_selectable(parent=dpg.last_item(),height=-1,drop_callback= lambda s, a :
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

            dpg.add_menu_item(label="Delete",callback=lambda: (vm.rm_var(key=dpg.get_item_label(shown_label),dict=var_dict['geometry']),print("dict del"), dpg.delete_item(last_row),print("row del"), dpg.delete_item(last_pop),print("popup del"),))
            dpg.add_menu_item(label="Edit",callback=obj_edit_func,user_data=shown_label)
            dpg.add_menu_item(label="more1")
            dpg.add_menu_item(label="more2")
    dpg.delete_item(from_pos)
    dpg.delete_item(spacer_from_pos)

    shown_list = dpg.get_item_children('object list')[1]
    list_order_label = []
    for i in shown_list:
        item =dpg.get_item_label(dpg.get_item_children(i)[1][0])
        if item != "":
            list_order_label.append(item)


    
    var_dict['geometry'] = {k: var_dict['geometry'][k] for k in list_order_label}
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
                material = dpg.add_combo(items=list(var_dict['material'].keys()),default_value='Empty')

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

                              



        #dpg.push_container_stack(dpg.add_menu(label="Themes"))
        #dpg.add_menu_item(label="Edit",callback=lambda: print("Edited!"))
        #dpg.add_menu_item(label=f"Delete ",callback=lambda: dpg.delete_item(dpg.get_item_parent(dpg.last_container())))
        #dpg.pop_container_stack()


def check_repeat(name, group):
    if name in group:
        new_name = name + '-copy'
        a = check_repeat(name=new_name,group=group)
        return a
    else:
        return name

def obj_add_func(sender,app_data,user_data):
    name = user_data[0]
    print(name)
    stru = user_data[1]
    material = user_data[2]
    if stru in var_dict['structure']:
        temp_geo_class = copy.deepcopy(var_dict['structure'][stru])
        print(temp_geo_class.__dict__)
        temp_geo_class.material = material
    if 'geometry' not in var_dict:
        var_dict.update({'geometry':{}})
    
    name = check_repeat(name=name, group=var_dict['geometry'])
    var_dict['geometry'].update({f'{name}':temp_geo_class})
    var_dict['geometry'][f'{name}'] = var_dict['geometry'].pop(f'{name}')
    print(var_dict['geometry'])
        
    

    spacer_row = dpg.table_row(parent="object list",height=-1,tag=f'{name} spacer row',before='spacer')
    real_object_row = dpg.table_row(parent="object list",label=f"{name} object row",before='spacer')
    with spacer_row:
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

            dpg.add_menu_item(label="Delete",callback=lambda: (vm.rm_var(key=dpg.get_item_label(shown_label),dict=var_dict['geometry']),print("dict del"), dpg.delete_item(last_row),print("row del"), dpg.delete_item(last_pop),print("popup del"),))
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

        vm.rm_var(key=str(old_val),dict=var_dict['geometry'])

        print(f"dict deleted: {var_dict['geometry']}")
        if new_val in var_dict['geometry']:
            new_val = check_repeat(name=new_val,group=var_dict['geometry'])
        else:
            pass
        material_key = dpg.get_value(combo_material)
        #print(material_key)
        if material_key == 'Empty':
            material_value = 'Empty'
        else:

            material_value = var_dict['material'][f'{material_key}']
        #print(material_value)
        listed_obj_ids = dpg.get_item_children(item='object list')[1]
        list_order_label = []
        for id in listed_obj_ids:
            select_id = id+1
            list_order_label.append(dpg.get_item_label(select_id))
        print(list_order_label)

        temp_geo.material = material_value
        var_dict['geometry'].update({new_val:temp_geo})
        dpg.set_item_label(item=label_in_list,label=new_val)
        var_dict['geometry'] = {k: var_dict['geometry'][k] for k in list_order_label}
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
                    default_value= name_label,)
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
                                    else:
                                        temp = source_val
                                    


                                    var_dict['geometry'][f'{name_label}'].__dict__[f'{key}'] = temp

                                    print(f"{key}:{var_dict['geometry'][f'{name_label}'].__dict__[f'{key}']}")
                                    print(var_dict['geometry'][f'{name_label}'].__dict__)


                                    
                                    #print(f'{attrs[0]}:{source_val[0:-1]}')
                                
                                    
                                print(attrs[1])
                                if isinstance(attrs[1], Vector3):
                                    #print(attrs[0])

                                    #txt=dpg.add_text("dummy",tag=f'dum_{attrs[0]}',show= True)
                                    
                                    

                                    coord = dpg.add_drag_floatx(tag=f'slider_{name_label}_{attrs[0]}', 
                                                                min_value=-100.0,
                                                                max_value=100.0,
                                                                default_value=list(default_val),
                                                                speed=10,
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

                                    obj_material = dpg.add_combo(items=list(var_dict['material'].keys()),default_value=default_val)
                                    _help("Won't be Updated automatically.")
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

main_window = dpg.window(
    label="main window",
    tag="main window",
    width=600,
    height=600, 
    pos=(300,0)
)
with main_window:
    title = dpg.add_text("Hello, this is main window")
    btn_obj = dpg.add_button(label="add object",callback=add_obj)


















dpg.create_viewport(title='MEEP_GUI', width=1440, height=900)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()


dpg.destroy_context()