import dearpygui.dearpygui as dpg
dpg.create_context()


def add_win(sender):
    with dpg.window(label="dddddd"):
        dpg.add_button(label="exit",callback=hide_tag)

                   
def hide_tag(sender,app_data):
    
    if  dpg.get_item_configuration(dpg.get_item_parent(sender))['show']:
        dpg.hide_item(item=dpg.get_item_parent(sender))
        print('hide')
    else:
        pass

def show_tag(sender):
    
    if not dpg.get_item_configuration(100)['show']:
        dpg.show_item(item=100)
        print("show")
    else:
        print(dpg.get_item_configuration(100)['show'])
        pass


def debug(sender):
    dpg.show_debug()

def item_registry(sender):
    dpg.show_item_registry()



with dpg.window(label="show window",tag = 100,show=True):
    dpg.add_button(label="exit",callback=hide_tag)
    dpg.add_input_text(label="string", default_value="1111111111")


with dpg.window(label="Example Window",width=500,height=400,pos=(500,0),tag = 114,no_title_bar=True):
    dpg.add_text("Hello, world",tag='hw')
    #dpg.add_button(label="Save",callback=add_win)
    dpg.add_input_text(label="string", default_value="Quick brown fox")
    dpg.add_slider_float(label="float", default_value=0.273, max_value=1)
    dpg.add_button(label="show win",callback=show_tag)
    dpg.add_text(f"Hello, world")
    dpg.add_button(label="debug",callback=debug)
    dpg.add_button(label="item",callback=item_registry)

dpg.show_documentation()







dpg.create_viewport(title='It is a VIEWPORT', width=1440, height=900)

dpg.setup_dearpygui()
dpg.show_viewport()
while dpg.is_dearpygui_running():
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()


    dpg.render_dearpygui_frame()


dpg.destroy_context()