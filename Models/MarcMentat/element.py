##  Main program

#   Imports

from py_mentat import *
from py_post import *

#   Tolerance checking function

def tol_check(f1, f2, tol):

    if f1 == f2:

        return 1

    if f1 + tol < f2:

        if f1 - tol > f2:

            return 1

    return 0

#   Create the node grid

def create_nodes(x0, y0, x_n, y_n):

    y = y0

    z = 0

    del_x = 1/x_n
    del_y = 1/y_n

    for i in range(0, y_n):

        x = x0

        for j in range(0, x_n):
            
            py_send("*add_nodes %f %f %f" % (x, y, z))

            x = x + del_x

        y = y + del_y

    return

#   Create the element grid

def create_elements(n, m):

    for i in range(1, m):

        n1 = (i - 1)*n + 1
        n2 = n1 + 1
        n3 = n2 + n
        n4 = n1 + n

        for j in range(1, n):

            py_send("*add_elements %d %d %d %d" % (n1, n2, n3, n4))

            n1 = n1 + 1
            n2 = n2 + 1
            n3 = n3 + 1
            n4 = n4 + 1

    return

#   Add sinusoidal wave to a table

def add_sin(table_name):

    py_send("*new_md_table 1 1")
    py_send("*table_name %s" % table_name)
    py_send("*set_md_table_step_v 1 100")
    py_send("*set_md_table_min_f 1 -1")
    py_send("*set_md_table_step_f 1 100")
    py_send("*set_md_table_method_formula")
    py_send("*md_table_formula sin(2*pi*v1)")

#   Add fixed boundary conditions to the left and bottom sides of the element

def add_bc_fixed(x_bc, y_bc, x_n, y_n):

    n_n = py_get_int("nnodes()")

    py_send("*apply_type fixed_displacement")
    py_send("*apply_name fix_dis")
    py_send("*apply_dof x")
    py_send("*apply_dof y")
    py_send("*apply_dof z")

    n_l = []

    for i in range(1, n_n + 1):

        x = py_get_float("node_x(%d)" % i)

        if tol_check(x, x_bc, 0.001):

            n_l.append(i)

        y = py_get_float("node_y(%d)" % i)

        if tol_check(y, y_bc, 0.001):

            n_l.append(i)

    py_send("*add_apply_nodes ")

    for i in range(0, len(n_l)):

        py_send("%d " % n_l[i])

    py_send(" # ")

    return

# Add the load to the right and top sides of the element

def add_load(table_name):

    py_send("*new_apply")
    py_send("*apply_type edge_load")
    py_send("*apply_name sin_load")
    py_send("*apply_dof p")
    py_send("*apply_dof_table p %s" % table_name)
    py_send("*add_apply_edges 21:2 22:2 23:2 24:2 25:2 5:1 10:1 15:1 20:1 25:1 #")

    return

#   Add a Mooney-Rivlin material

def add_mat():

    py_send("*new_mater standard")
    py_send("*mater_option general:state:solid")
    py_send("*mater_option general:skip_structural:off")
    py_send("*mater_name rubber")
    py_send("*mater_option structural:type:mooney")
    py_send("*mater_option structural:mooney_model:five_term")
    py_send("*mater_param structural:mooney_c10 20.3")
    py_send("*mater_param structural:mooney_c01 5.8")
    py_send("*add_mater_elements all_existing")

    return

#   Add plane strain geometrical properties

def add_geom_prop():

    py_send("*geometry_type mech_planar_pstrain")
    py_send("*add_geometry_elements all_existing")

    return

#   Add the job

def add_job():

    py_send("*loadcase_type static")
    py_send("*new_job structural")
    py_send("*job_option dimen:pstrain")
    py_send("*add_post_tensor stress")
    py_send("*add_post_var von_mises")
    py_send("*element_type 6 all_existing")

    return

#   Main function

def main():

#   *change_directory "C:\Users\19673418\Documents\Masters-Project\Models\MarcMentat"

    table_name = "sin_input"

    x_n = 6
    y_n = 6

    x0 = 0
    y0 = 0

    create_nodes(x0, y0, x_n, y_n)

    create_elements(x_n, y_n)

    add_bc_fixed(0, 0, x_n, y_n)

    add_sin(table_name)

    add_load(table_name)

    add_mat()

    add_geom_prop()

#   add_job()

    py_send("*identify_applys")
    py_send("*redraw")
    py_send("*fill_view")

#    py_send("save_as_model element_basic.mud yes")

    return

if __name__ == '__main__':

    py_connect("", 40007)

    main()

    py_disconnect


