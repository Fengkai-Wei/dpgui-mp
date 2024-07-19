import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

dpg.create_context()

def print_val(sender):
    print(dpg.get_value(sender))

def change_text(sender, app_data):
    if dpg.is_item_hovered("text item"):
        dpg.set_value("text item", f"Go away...")
    else:
        dpg.set_value("text item", f'Watch me!')


def button_cbk(sender, app_data, usr_data):
    print(f'Sender is:{sender}')
    print(f'App Data is:{app_data}')
    print(f'User Data is:{usr_data}')

with dpg.window(label="Example Window",width=500,height=400,pos=(500,0)):
    dpg.add_text("Hello, world")
    dpg.add_button(label="Save")
    dpg.add_input_text(label="string", default_value="Quick brown fox")
    dpg.add_slider_float(label="float", default_value=0.273, max_value=1)

with dpg.window(label="Example Window",width=500,height=400,):
    dpg.add_text("Hello, World 2.")
    dpg.add_button(label="Save")
    dpg.add_input_text(label="string", default_value="Quick brown fox")
    dpg.add_slider_float(label="float", default_value=0.555, max_value=1)

with dpg.window(label="Tutorial"):
    b0 = dpg.add_button(label="button 1")
    b1 = dpg.add_button(tag=100, label="Button 2")
    with dpg.group():
        dpg.add_button(label="Button 3")
        dpg.add_button(label="Button 4")
        with dpg.group() as group1:
            pass

    BIG_button = dpg.add_button(label="BIG BUTTON",callback=button_cbk,user_data="Some data")
    another_btn = dpg.add_button(label="another button")
    dpg.set_item_callback(another_btn,button_cbk)
    dpg.set_item_user_data(another_btn, "More data")

with dpg.window(width=500,height=400,pos=(0,400)):
    input_txt1 = dpg.add_input_text()
    input_txt2 = dpg.add_input_double(
        label="some float",
        default_value= 0.50,
        callback=print_val
    )

    slider_float1 = dpg.add_slider_float()
    slider_float2 = dpg.add_slider_float(
        label="another slider float",
        default_value= 6.55,
        callback=print_val
    )

    dpg.set_item_callback(input_txt1,print_val)
    dpg.set_item_callback(slider_float1,print_val)


with dpg.handler_registry():
    dpg.add_mouse_move_handler(callback=change_text)




with dpg.window(width=500, height=400,pos=(500,400)):
    dpg.add_text("Hover Me!", tag="text item")



dpg.add_button(label="Button 6", parent=group1)
dpg.add_button(label="Button 5", parent=group1)


def add_buttons():
    global new_button1, new_button2
    new_button1 = dpg.add_button(label="New Button", before="delete_button", tag="new_button1")
    new_button2 = dpg.add_button(label="New Button 2", parent="secondary_window", tag="new_button2")


def delete_buttons():
    dpg.delete_item("new_button1")
    dpg.delete_item("new_button2")


with dpg.window(label="Tutorial", pos=(200, 200)):
    dpg.add_button(label="Add Buttons", callback=add_buttons)
    dpg.add_button(label="Delete Buttons", callback=delete_buttons, tag="delete_button")

with dpg.window(label="Secondary Window", tag="secondary_window", pos=(100, 100)):
    pass
    
    





#demo.show_demo()
#dpg.show_item_registry()
dpg.create_viewport(title='It is a VIEWPORT', width=1600, height=900)

dpg.setup_dearpygui()
dpg.show_viewport()

while dpg.is_dearpygui_running():
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()
    #print("Ciallo～(∠・ω< )⌒★")
    dpg.render_dearpygui_frame()



dpg.destroy_context()