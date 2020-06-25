#   Imports

from py_mentat import *
from py_post import *

#   Adding the plate

def add_plate(xs, ys, width, height):

    py_send("*set_curve_type line")
    py_send("*add_points")
    py_send("%f %f 0" % (xs, ys))
    py_send("%f %f 0" % (xs + width, ys))
    py_send("%f %f 0" % (xs + width, ys + height))
    py_send("%f %f 0" % (xs, ys + height))

    py_send("*set_curve_type line")
    py_send("*add_curves")
    py_send("1 2")
    py_send("2 3")
    py_send("3 4")
    py_send("4 1")

    py_send("*fill_view")

    return

def build_plate(xstart, ystart, width, height, diameter, spacing):

    f = diameter + spacing

    nx = int((width - spacing)/f)
    ny = int((height - spacing)/f)

    if (nx < 1 or ny < 1):

        print("The holes are too big.")

        return 1

    print("Creating the hole grid of ", nx, " by ", ny)

    add_plate(xstart, ystart, width, height)

    xs = 0.5*(width - f*(nx - 1)) + xstart
    ys = 0.5*(height - f*(ny - 1)) + ystart

    py_send("*set_curve_type circle_cr")
    py_send("*add_curves")

    r = diameter/2

    for i in range(0, ny):

        y = ys + i*f

        for j in range(0, nx):

            x = xs + j*f

            py_send("%f %f 0 %f" % (x, y, r))
    
    return 0

def check_tol(f1, f2, tol):

    if f1 == f2:

        return 1

    if f1 + tol < f2:

        if f1 - tol > f2:

            return 1

    return 0

def mesh_plate(width, height, diameter, spacing):

    py_send("*set_curve_div_type_fix_avgl")

    l = spacing/2

    py_send("*set_curve_div_avgl %f" % l)
    py_send("*apply_curve_divisions all_existing")
    py_send("*dt_planar_trimesh all_existing")

    return

def add_bc(xs, ys, width, height):

    py_send("*renumber_all")

    n = py_get_int("nnodes()")

#   Fixed boundary condition on the left-hand side

    py_send("*apply_type fixed_displacement")
    py_send("*apply_dof x")
    py_send("*apply_dof y")
    py_send("*apply_dof z")

    node_list = []

    for i in range(1, n + 1):

        str = "node_x(%d)" % i

        f = py_get_float(str)

        if check_tol(f, xs, 0.001):

            node_list.append(i)
        
    py_send("*add_apply_nodes")

    for i in range(0, len(node_list)):

        str = "%d" % node_list[i]

        py_send(str)

    py_send(" # ")

#   Add the edge load at the top

    py_send("*new_apply")
    py_send("*apply_type edge_load")
    py_send("*apply_value = p 1000")
    py_send("add_apply curves 3 #")

    return

def add_matl():

    py_send("*mater_option structural:type:elast_plast_iso")
    py_send("*mater_param structural:youngs_modulus 3e+7")
    py_send("*mater_param structural:poissons_ration 0.3")
    py_send("*add_mater_elements all_existing")

    return

def add_geom_prop():

    py_send("*geometry_type mech_planar_pstress")
    py_send("*geometry_value thick 0.75")
    py_send("*add_geometry_elements all_existing")

    return

def add_job():

    py_send("*loadcase_type static")
    py_send("*new_job structural")
    py_send("*job_option dimen:pstress")
    py_send("*add_post_tensor stress")
    py_send("*add_post_var von_mises")
    py_send("*element_type 6 all_existing")

    return

def main():

    xstart = 0
    ystart = 0

    width = py_get_float("width")
    height = py_get_float("height")
    diameter = py_get_float("diameter")
    spacing = py_get_float("spacing")

 #   xstart = -width/2
 #   ystart = -height/2

    build_plate(xstart, ystart, width, height, diameter, spacing)

    mesh_plate(width, height, diameter, spacing)

    add_bc(xstart, ystart, width, height)

    add_matl()

    add_geom_prop()

    add_job()

    py_send("save_as_model chap5.mfd yes")

    return

if __name__ == '__main__':

    py_connect("", 40007)
    main()
    py_disconnect()