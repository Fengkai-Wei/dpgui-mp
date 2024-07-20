import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import time
import vars

import var_manage as vm
vars.init()
from  vars import var_dict




dpg.create_context()

dpg.show_item_registry()

def test_fun(sender,app_data,user_data):
    print(user_data)
    #print(f"Hello, I am item: {dpg.get_item_pos(sender)}")
    with dpg.table_row(parent="object list",label="new_row"):
        last_row = dpg.last_item()
        dpg.add_selectable(label=f"{user_data}")
        with dpg.popup(parent=dpg.last_item()):
            last_pop = dpg.last_container()
            dpg.add_text("delete")
            dpg.add_button(label=f"do it", callback=lambda: (dpg.delete_item(last_row),print("row del"), dpg.delete_item(last_pop),print("popup del")))
            dpg.push_container_stack(dpg.add_menu(label="Tools"))
            dpg.add_menu_item(label="Show Logger")
            dpg.add_menu_item(label="Show About")
            dpg.pop_container_stack()

def add_obj(sender,app_data,user_data):

    object_add_window = dpg.window(
        label = "add object",
    )
    
    with object_add_window:
        dpg.configure_item(dpg.last_root(),on_close=lambda: dpg.delete_item(dpg.last_root()))
        with dpg.group(horizontal=True):
            with dpg.group(horizontal=False):
                dpg.add_text("Name:")
                dpg.add_text("Strucutre:")
                dpg.add_text("Material:")
            with dpg.group(horizontal=False):
                obj_name_input = dpg.add_input_text(
                    label="",
                    default_value="new object",

            )
                stru = dpg.add_combo(items=["cat","dog"],default_value=None)
                material = dpg.add_combo(items=["Silicon","Al"],default_value=None)

                def check_structure(stru,input):
                    last_win = dpg.last_root()
                    if stru == "None":
                        dpg.delete_item(last_win)
                        
                        
                        with dpg.window(
                            
                            label="No structure alert",
                            modal=True
                        ):
                            dpg.add_text('The strcuture is not specified! Unable to create geometric object.'),

                            dpg.add_button(
                                label="Back",
                                callback=lambda: (dpg.delete_item(dpg.last_container()),
                                                  
                                                  )

                            )
                        
                    else:
                        
                        print(dpg.get_value(input))
                        obj_add_func(sender=dpg.last_item(),
                                     app_data=None,
                                     user_data= dpg.get_value(input)
                                     )
                        dpg.delete_item(last_win)
                        
        

        dpg.add_button(label="add",callback=lambda: check_structure(stru=dpg.get_value(stru),input=obj_name_input) )
                              



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
    name = user_data
    print(name)
    mat = 'dummy'
    dumpos = [0,0,0]
    obj = [dumpos, dumpos,mat]
    if 'geometry' not in var_dict:
        var_dict.update({'geometry':{}})
    
    name = check_repeat(name=name, group=var_dict['geometry'])
    var_dict['geometry'].update({f'{name}':obj})
        

    with dpg.table_row(parent="object list",label="new_row"):
        last_row = dpg.last_item()
        dpg.add_selectable(label=f"{name}")
        shown_label = dpg.last_item()
        with dpg.popup(parent=dpg.last_item()):
            last_pop = dpg.last_container()
            #dpg.add_button(label=f"do it", callback=lambda: (dpg.delete_item(last_row),print("row del"), dpg.delete_item(last_pop),print("popup del")))

            dpg.add_menu_item(label="Delete",callback=lambda: (vm.rm_var(key=dpg.get_item_label(shown_label),dict=var_dict['geometry']),print("dict del"), dpg.delete_item(last_row),print("row del"), dpg.delete_item(last_pop),print("popup del"),))
            dpg.add_menu_item(label="Edit",callback=obj_edit_func,user_data=shown_label)
            dpg.add_menu_item(label="more1")
            dpg.add_menu_item(label="more2")


def obj_edit_func(sender,app_data,user_data):
    name = user_data
    obj='dummy'
    object_edit_window = dpg.window(
        label = "edit object",
        modal =True,
    )
    last_win = object_edit_window

    def save(item, value):
        old_val = value[0]
        new_val = value[1]
        print(var_dict['geometry'])
        vm.rm_var(key=str(old_val),dict=var_dict['geometry'])
        if new_val in var_dict['geometry']:
            new_val = check_repeat(name=new_val,group=var_dict['geometry'])
        else:
            pass

        var_dict['geometry'].update({new_val:obj})
        dpg.set_item_label(item=item,label=new_val)
        print(var_dict['geometry'])

    with object_edit_window:
        dpg.configure_item(dpg.last_root(), on_close=lambda: dpg.delete_item(dpg.last_root()))
        with dpg.group(horizontal=True):
            dpg.add_text("Name:")
            obj_name_input = dpg.add_input_text(
                label="",
                default_value=f"{dpg.get_item_label(name)}",)

        with dpg.group(horizontal=True):
            save_btn = dpg.add_button(
                label="Save",
                callback=lambda: (save(item=name,value=[dpg.get_item_label(name), dpg.get_value(obj_name_input)]),
                                  dpg.delete_item(dpg.last_root()))
            )
            apply_btn = dpg.add_button(
                label="Apply",
                callback=lambda: (save(item=name,value=[dpg.get_item_label(name), dpg.get_value(obj_name_input)]),
                                  ),

            )
    




object_window = dpg.window(
    label="object window",
    tag="object window",
    width=300,
    height=600
)


object_list_table = dpg.table(
    label="object list",
    tag="object list",
    row_background=True,borders_innerH=True, borders_outerH=True, borders_innerV=True,borders_outerV=True

)


with object_window:
    title = dpg.add_text("Hello, this is object list!")
    btn1 = dpg.add_button(
        label= "add something!",
        tag="add objects",
        callback=add_obj,
    )
    

    with object_list_table:
        dpg.add_table_column(label="Object list")





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
    height=600
)
with main_window:
    title = dpg.add_text("Hello, this is main window")
    btn_obj = dpg.add_button(label="add object",callback=add_obj)

















dpg.create_viewport(title='MEEP_GUI', width=1440, height=900)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()


dpg.destroy_context()