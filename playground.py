import dearpygui.dearpygui as dpg
import pyvista as pv
import numpy as np

reso = 20


# 创建球体
sphere = pv.Sphere(radius=1.0, center=(0, 0, 0), theta_resolution=reso,phi_resolution=reso)


# 创建立方体
cube = pv.Cube(center=(2, 0, 0))
cone = pv.Cone(center=(0,0,4),direction=(0, 0.0, 1),height=2.0,resolution=reso)

# 创建圆柱体
cylinder = pv.Cylinder(radius=0.5, height=2.0, center=(0, -3, 0),resolution=reso,direction=(0,1,0))


# 合并形状
combined = sphere + cube + cylinder



# 在z=0位置进行切片
slice_z = combined.slice(normal='z', origin=(0, 0, 0))


# 获取切片后顶点坐标
#vertices = slice_z.points

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=1600, height=600)


def sort_vertices(vertices):
    # 计算质心
    centroid = np.mean(vertices, axis=0)
    
    # 计算每个顶点相对于质心的角度
    def angle_from_centroid(vertex):
        return np.arctan2(vertex[1] - centroid[1], vertex[0] - centroid[0])
    
    # 对顶点按角度进行排序
    sorted_vertices = sorted(vertices, key=angle_from_centroid)
    return np.array(sorted_vertices)

def vista2dpg_sort(sliced_points, norm):
    if len(sliced_points) == 0:
        return np.array([[0],[0]])
    flatten  = np.delete(arr=sliced_points, obj= norm,axis= 1)
    sorted = sort_vertices(flatten)
        
    return sorted.transpose()

obj_list = [cylinder,cube,sphere,cone]


def update_plane(sender,app_data, user_data):
    slider_pos = dpg.get_value(sender)
    objs = user_data[0]
    parent = user_data[1]
    normal = user_data[2]
    project = user_data[3]
    dpg.delete_item(parent,children_only= True)
    origin = tuple(np.array(normal)*slider_pos)
    #print(origin)
    for i in objs:
        slice = i.slice(normal=normal, origin=origin).points
        sorted_points = vista2dpg_sort(slice,project).tolist()
        #print(sorted_points)
        dpg.add_area_series(parent=parent,x = sorted_points[0],y=sorted_points[1],fill=[255,50,100,255])
        










with dpg.window(label='main',width=-1,height=600):
    
    dpg.add_text("plot control")
    with dpg.group(horizontal= True):
        with dpg.group():
            with dpg.plot(label="XY Plane", height=400):
                dpg.add_plot_axis(dpg.mvXAxis, label="x",tag='xy_x')
                        
                with dpg.plot_axis(dpg.mvYAxis, label="y",tag='xy_y'):
                    parent_xy = dpg.last_item()
                    dpg.set_axis_limits('xy_x',ymin= -5,ymax=5)
                    dpg.set_axis_limits('xy_y',ymin= -5,ymax=5)

            slider = dpg.add_slider_float(width= 300,min_value=-5.,max_value=5.,default_value=0.0,callback=update_plane,user_data=[obj_list,parent_xy,(0,0,1),2])

        with dpg.group():

            with dpg.plot(label="YZ Plane", height=400):
                dpg.add_plot_axis(dpg.mvXAxis, label="y",tag='yz_x',)
                            
                with dpg.plot_axis(dpg.mvYAxis, label="z",tag='yz_y'):
                    parent_yz = dpg.last_item()
                    dpg.set_axis_limits('yz_x',ymin= -5,ymax=5)
                    dpg.set_axis_limits('yz_y',ymin= -5,ymax=5)

            slider = dpg.add_slider_float(width= 300,min_value=-5.,max_value=5.,default_value=0.0,callback=update_plane,user_data=[obj_list,parent_yz,(1,0,0),0])

        with dpg.group():

            with dpg.plot(label="XZ Plane", height=400):
                dpg.add_plot_axis(dpg.mvXAxis, label="x",tag='xz_x',)
                            
                with dpg.plot_axis(dpg.mvYAxis, label="z",tag='xz_y'):
                    parent_yz = dpg.last_item()
                    dpg.set_axis_limits('xz_x',ymin= -5,ymax=5)
                    dpg.set_axis_limits('xz_y',ymin= -5,ymax=5)

            slider = dpg.add_slider_float(width= 300,min_value=-5.,max_value=5.,default_value=0.0,callback=update_plane,user_data=[obj_list,parent_yz,(0,1,0),1])
    
    with dpg.subplots(2,2):
        for i in range(3):
            with dpg.plot(label="YZ Plane", height=400):
                dpg.add_plot_axis(dpg.mvXAxis, label="y",)


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()