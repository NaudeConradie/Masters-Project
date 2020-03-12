##  Main program

#   Imports

from py_mentat import *
from py_post import *

import random

###################################################################

#   Tolerance checking function
#   Returns a 1 if the values are within the specified tolerance

#   v1:  The first value to be compared
#   v2:  The second value to be compared
#   tol: The specified tolerance
def tol_check(v1, v2, tol):

    if v1 == v2:

        return 1

    if v1 + tol < v2:

        if v1 - tol > v2:

            return 1

    return 0

###################################################################

#   Reformat the viewing window for visibility

def re_win():

    py_send("*identify_applys")
    py_send("*redraw")
    py_send("*fill_view")

###################################################################

#   Create a 2D node grid on the XY-plane

#   x0:  The initial x-coordinate
#   y0:  The initial y-coordinate
#   x_n: The number of nodes in the x-axis
#   y_n: The number of nodes in the y-axis
def create_nodes(x0, y0, x_n, y_n):

    #   Initialisations
    y = y0
    z = 0

    #   Incremental node additions
    for i in range(0, y_n):

        x = x0

        for j in range(0, x_n):
            
            py_send("*add_nodes %f %f %f" % (x, y, z))

            x = x + 1

        y = y + 1

    return

###################################################################

#   Create an element grid on the node grid

#   n: The number of nodes in the x-direction
#   m: The number of nodes in the y-direction
def create_elements(n, m):

    #   Incremental element additions
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

###################################################################

#   Add a sinusoidal wave to a table

#   table_name: The name of the table
def add_sin(table_name):

    py_send("*new_md_table 1 1")
    py_send("*table_name %s" % table_name)
    py_send("*set_md_table_type 1 \"time\"")
    py_send("*set_md_table_step_v 1 100")
    py_send("*set_md_table_min_f 1 -1")
    py_send("*set_md_table_step_f 1 100")
    py_send("*set_md_table_method_formula")

    #   The sinusoidal function is defined to go through one full wavelength within 1 second
    py_send("*md_table_formula sin(2*pi*v1)")

    return

###################################################################

#   Add fixed boundary conditions to the left and bottom sides of the grid

#   x_bc: The x-coordinates along which the boundary condition should be applied
#   y_bc: The y-coordinates along which the boundary condition should be applied
#   x_n:  The number of nodes in the x-direction
#   y_n:  The number of nodes in the y-direction
def add_bc_fixed(x_bc, y_bc, x_n, y_n):

    #   Initialisation
    n_l = []

    #   Fetch the total number of nodes
    n_n = py_get_int("nnodes()")

    #   Apply the fixed boundary condition
    py_send("*apply_type fixed_displacement")
    py_send("*apply_name fix_dis")
    py_send("*apply_dof x")
    py_send("*apply_dof y")
    py_send("*apply_dof z")

    #   Incrementally select the correct nodes
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

    py_send("#")

    return

###################################################################

# Add a load to the right and top sides of the element

#   table_name: The name of the table containing the sinusoidal function
def add_load(table_name):

    py_send("*new_apply")
    py_send("*apply_type edge_load")
    py_send("*apply_name sin_load")

    #   Apply a pressure with an amplitude of 20 and the sinusoidal wave
    py_send("*apply_dof p")
    py_send("*apply_dof_value p 20")
    py_send("*apply_dof_table p %s" % table_name)

    #   Hardcoded list of correct edges
    py_send("*add_apply_edges 21:2 22:2 23:2 24:2 25:2 5:1 10:1 15:1 20:1 25:1 #")

    return

###################################################################

#   Add plane strain geometrical properties

def add_geom_prop():

    py_send("*geometry_type mech_planar_pstrain")
    py_send("*add_geometry_elements all_existing")

    return

###################################################################

#   Add an example Mooney-Rivlin material

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

###################################################################

#   Add a loadcase

def add_lcase():

    py_send("*new_loadcase")
    py_send("*loadcase_type struc:static")
    py_send("*loadcase_value nsteps 20")

    return

###################################################################

#   Add a job

def add_job(rem):

    py_send("*prog_use_current_job on")
    py_send("*new_job structural")
    py_send("*job_name job_%d" % rem)
    py_send("*add_job_loadcases lcase1")
    py_send("*job_option strain:large")
    py_send("*job_option follow:on")
    py_send("*add_post_var von_mises")
    py_send("*add_post_var te_energy")

    return

###################################################################

#   Run a job

def run_job():

    py_send("*update_job")
    py_send("*submit_job 1") 
    py_send("*monitor_job")

    return

###################################################################

#   Open the results file and create gifs of the selected results

def res_gif(rem):

    py_send("*post_open_default")

    py_send("*post_contour_bands")
    
    py_send("*post_value Equivalent Von Mises Stress")
    py_send("*animation_name element_%d_evms" % rem)
    py_send("*gif_animation_make")

    py_send("*post_value Total Strain Energy Density")
    py_send("*animation_name element_%d_tsed" % rem)
    py_send("*gif_animation_make")

    py_send("*post_value Displacement")
    py_send("*animation_name element_%d_disp" % rem)
    py_send("*gif_animation_make")

    return

###################################################################

#   Obtain maximum values from results

def res_max():

    n_n = py_get_int("nnodes()")

    label = []
    label.append("Displacement x")
    label.append("Displacement x")


    return

###################################################################

#   Remove a random element
#   Returns the element ID that was removed

#   intern_el: The list of the internal elements in the grid
def rem_el(intern_el):

    rem = random.choice(intern_el)

    py_send("*remove_elements %d #" % rem)

    return rem

###################################################################

#   Save the basic model

def save_bas_model():

    py_send("*set_save_formatted off")
    py_send("*save_as_model element_basic.mud yes")

    return

###################################################################

#   Save a model referenced by the removed element

#   rem: The element ID of the removed element
def save_rem_model(rem):

    py_send("*set_save_formatted off")
    py_send("*save_as_model element_%d.mud yes" % rem)

    return

###################################################################

#   Main function

def main():

    #   Clear the workspace
    py_send("*new_model yes")

    #   Initialisations
    table_name = "sin_input"

    #   6 nodes for 5 elements
    x_n = 6
    y_n = 6

    #   Start at the origin
    x0 = 0
    y0 = 0

    #   Hardcoded list of internal elements
    intern_el = [7, 8, 9, 12, 13, 14, 17, 18, 19]

    #   Grid construction
    create_nodes(x0, y0, x_n, y_n)

    create_elements(x_n, y_n)

    add_sin(table_name)

    add_bc_fixed(x0, y0, x_n, y_n)

    add_load(table_name)

    add_geom_prop()

    add_mat()

    add_lcase()

    save_bas_model()

    #   Element removal

    # for i in range(1, len(intern_el) + 1):

    #     py_send("*open_model element_basic.mud")
        
    #     rem = rem_el(intern_el)

    #     re_win()

    #     save_rem_model(rem)

    #     add_job(rem)

    #     run_job()

    #     intern_el.remove(rem)

    rem = rem_el(intern_el)

    re_win()

    save_rem_model(rem)

    add_job(rem)

    run_job()

    res_gif(rem)

    return

if __name__ == '__main__':

    py_connect("", 40007)

    main()

    py_disconnect