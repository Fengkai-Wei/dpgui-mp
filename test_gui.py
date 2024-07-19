import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

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
                        



        #dpg.push_container_stack(dpg.add_menu(label="Themes"))
        #dpg.add_menu_item(label="Edit",callback=lambda: print("Edited!"))
        #dpg.add_menu_item(label=f"Delete ",callback=lambda: dpg.delete_item(dpg.get_item_parent(dpg.last_container())))
        #dpg.pop_container_stack()



def obj_add_func(sender,app_data,user_data):

    print(user_data)
    with dpg.table_row(parent="object list",label="new_row"):
        last_row = dpg.last_item()
        dpg.add_selectable(label=f"{user_data}")
        shown_label = dpg.last_item()
        with dpg.popup(parent=dpg.last_item()):
            last_pop = dpg.last_container()
            #dpg.add_button(label=f"do it", callback=lambda: (dpg.delete_item(last_row),print("row del"), dpg.delete_item(last_pop),print("popup del")))

            dpg.add_menu_item(label="Delete",callback=lambda: (dpg.delete_item(last_row),print("row del"), dpg.delete_item(last_pop),print("popup del")))
            dpg.add_menu_item(label="Edit",callback=obj_edit_func,user_data=shown_label)
            dpg.add_menu_item(label="more1")
            dpg.add_menu_item(label="more2")

    dpg.delete_item(dpg.get_item_parent(sender))

def obj_edit_func(sender,app_data,user_data):
    object_edit_window = dpg.window(
        label = "add object",
        modal =True
    )
    def save(item, value):
        dpg.set_item_label(item=item,label=value)

    with object_edit_window:
        with dpg.group(horizontal=True):
            dpg.add_text("Name:")
            obj_name_input = dpg.add_input_text(
                label="",
                default_value=f"{dpg.get_item_label(user_data)}",)
        with dpg.group(horizontal=True):
            save_btn = dpg.add_button(
                label="Save",
                callback=lambda: (save(item=user_data,value=dpg.get_value(obj_name_input)),
                                  dpg.delete_item(dpg.last_root()))
            )
            apply_btn = dpg.add_button(
                label="Apply",
                callback=lambda: (save(item=user_data,value=dpg.get_value(obj_name_input))),

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
        callback=test_fun,
    )
    

    with object_list_table:
        dpg.add_table_column(label="Object list")

def add_obj(sender,app_data,user_data):

    object_add_window = dpg.window(
        label = "add object",
        modal =True
    )
    with object_add_window:
        with dpg.group(horizontal=True):
            dpg.add_text("Name:")
            obj_name_input = dpg.add_input_text(
                label="",
                default_value="new object",

            )
        dpg.add_button(label="add",callback=lambda: obj_add_func(sender=dpg.last_item(),app_data=None, user_data= dpg.get_value(obj_name_input)))
        



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