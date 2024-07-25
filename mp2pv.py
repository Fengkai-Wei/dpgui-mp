from meep.geom import GeometricObject, Sphere,Cylinder,Wedge,Cone,Block,Ellipsoid,Prism
import pyvista as pv
import numpy as np


def co_planar_checker(points):
    # Noticably, in creation of prisms, meep don't check the coplanar upon creation.
    # That is, if we run the code below:
    # mp.Prism(
    # vertices=[mp.Vector3(0,0,0),
    #          mp.Vector3(1,0,0),
    #          mp.Vector3(0,1,0),
    #          mp.Vector3(1,1,1),
    #          ],height= 1)
    # Meep accepts those points, although it's clear (1,1,1) doesn't lie on the xy plane.
    # Ensure there are at least 4 points to check for coplanarity
    if len(points) < 4:
        return True
    points = np.array(points)
    P1, P2, P3 = points[:3]
    v1 = P2 - P1
    v2 = P3 - P1
    n = np.cross(v1, v2)
    for P in points[3:]:
        v = P - P1
        if not np.isclose(np.dot(n, v), 0):
            return False

    return True


def create_prism(base_points, height, norm=True):
    # Ensure the base points form a closed loop


    # Calculate the normal vector of the base plane
    v1 = base_points[1] - base_points[0]
    v2 = base_points[2] - base_points[0]
    normal = np.cross(v1, v2)
    normal = normal / np.linalg.norm(normal)

    # If norm is False, reverse the normal direction
    if not norm:
        normal = -normal

    # Calculate the top points by translating the base points along the normal
    top_points = base_points + height * normal

    # Combine base and top points
    all_points = np.vstack([base_points, top_points])

    # Create faces
    num_base_points = len(base_points)  # The last point is a duplicate of the first point
    faces = []

    # Add the base face
    faces.append([num_base_points] + list(range(num_base_points)))

    # Add the top face
    faces.append([num_base_points] + list(range(num_base_points, 2 * num_base_points)))

    # Add the side faces
    for i in range(num_base_points):
        next_i = (i + 1) % num_base_points
        faces.append([4, i, next_i, next_i + num_base_points, i + num_base_points])

    # Flatten the faces list
    faces = np.hstack(faces)

    # Create the prism
    prism = pv.PolyData(all_points, faces)
    return prism

def create_fan_prism(center, radius, start_angle, end_angle, num_points, height, norm=True):
    angles = np.linspace(start_angle, end_angle, num_points)
    base_points = np.array([[center[0] + radius * np.cos(angle), 
                             center[1] + radius * np.sin(angle), 
                             center[2]] for angle in angles])
    base_points = np.vstack([center, base_points, center])  # Close the fan shape

    v1 = base_points[1] - base_points[0]
    v2 = base_points[2] - base_points[0]
    normal = np.cross(v1, v2)
    normal = normal / np.linalg.norm(normal)
    if not norm:
        normal = -normal
    top_points = base_points + height * normal
    all_points = np.vstack([base_points, top_points])
    num_base_points = len(base_points) - 1
    faces = []
    faces.append([num_base_points] + list(range(num_base_points)))
    faces.append([num_base_points] + list(range(num_base_points, 2 * num_base_points)))
    for i in range(num_base_points - 1):
        next_i = (i + 1) % num_base_points
        faces.append([4, i, next_i, next_i + num_base_points, i + num_base_points])
    faces = np.hstack(faces)
    prism = pv.PolyData(all_points, faces)
    return prism




def convert(mp_obj):
    class_obj = type(mp_obj).__name__
    center = np.array(mp_obj.center)
    if class_obj == 'Sphere':
        pv_obj = pv.Sphere(
            center=center,
            radius=mp_obj.radius
        )
    
    elif class_obj == 'Cylinder':
        pv_obj = pv.Cylinder(
            center = center,
            direction=np.array(mp_obj.axis),
            radius=mp_obj.radius,
            height=mp_obj.height
        )

    elif class_obj == 'Wedge':
        
        create_fan_prism
        

    elif class_obj == 'Cone':

        pv_obj = pv.Cylinder(
            center = center,
            direction=np.array(mp_obj.axi),
            radius=mp_obj.radius,
            height=mp_obj.height
        )
    elif class_obj == 'Block':
        e1 = np.array(mp_obj.e1)
        e2 = np.array(mp_obj.e2)
        e3 = np.array(mp_obj.e3)
        size = np.array(mp_obj.size)
        temp_cube = pv.Cube(
            center=center,
            x_length= size[0],
            y_length= size[1],
            z_length= size[2],
        )
        vertices = temp_cube.points
        transformation_matrix = np.array([e1, e2, e3]).T

        transformed_vertices = vertices @ transformation_matrix

        pv_obj = pv.PolyData(transformed_vertices, temp_cube.faces)

    
    elif class_obj == 'Ellipsoid':
        temp_ellipsoid = pv.ParametricEllipsoid(
            x_radius = mp_obj.x_length*0.5,
            y_radius = mp_obj.y_length*0.5,
            z_radius = mp_obj.z_length*0.5)
        pv_obj = temp_ellipsoid.translate(center)

    elif class_obj == 'Prism':
        axis = np.array(mp_obj.axis)
        pos_dir = np.array([0,0,1])
        pv_obj = create_prism(
            base_points=np.array(mp_obj.vertices),
            height= mp_obj.height,
            # Here the axis of prism is passed to create_prism function only for determination of norm direction.
            # The list of base points alone is sufficiently determine the surface and its two norms as long as base points are STRICTLY lie in one plane.
            # For compatiblity with Meep, the direction will be positive if axis points to upper half in the space.
            # Mathematically, if np.dot(axis, pos_dir) >= 0, then the norm is positive, otherwise negative.
            norm = True if np.dot(axis, pos_dir) >= 0 else False

        )

    return pv_obj
