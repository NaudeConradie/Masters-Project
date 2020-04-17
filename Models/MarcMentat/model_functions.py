##  Functions used with the Marc Mentat models

#   Imports

from utility_functions import *
from file_paths import *
from log_settings import m_log

from py_mentat import *
from py_post import *

import time

################################################################################

#   Open a model

#   s:  Identification string
#   f:  Folder to be opened from
def open_model(s, f):

    if f == "bm":
        fp_o = fp_bm + r'\grid_' + s + r'\grid_' + s + '.mud'

    elif f == "m":
        fp_o = fp_m + r'\grid_' + s + r'\grid_' + s + '.mud'

    py_send(r'*open_model "%s"' % fp_o)

    m_log.info("Existing model \"grid_%s.mud\" opened" % s)

    return

################################################################################

#   Save a model

#   s:  Identification string
#   f:  Folder to be saved in
def save_model(s, f):

    if f == "bm":
        make_folder(fp_bm + r'\grid_' + s)
        fp_s = fp_bm + r'\grid_' + s + r'\grid_' + s + '.mud'

    elif f == "m":
        make_folder(fp_m + r'\grid_' + s)
        fp_s = fp_m + r'\grid_' + s + r'\grid_' + s + '.mud'

    py_send("*set_save_formatted off")
    py_send(r'*save_as_model "%s" yes' % fp_s)

    m_log.info("Model \"grid_%s.mud\" saved" % s)

    return

################################################################################

#   Create a basic model from which elements may be removed

#   x0:         The initial x-coordinate
#   y0:         The initial y-coordinate
#   x_n:        The number of nodes in the x-direction
#   y_n:        The number of nodes in the y-direction
#   x_e:        The number of elements in the x-direction
#   y_e:        The number of elements in the y-direction
#   tab_name:   The name of the table
#   d:          The magnitude of the applied displacement
#   n_steps:    The number of steps in the second of the loadcase
#   n_e_l:      The number of elements as a string
def create_base_model(x0, y0, x_n, y_n, x_e, y_e, tab_name, d, n_steps, n_e_l):

    #   Clear the workspace
    py_send("*new_model yes")

    #   Grid construction
    create_nodes(x0, y0, x_n, y_n)
    create_elements(x_n, y_n)

    #   Add model properties
    add_bc_fixed("y", "y", y0)
    add_sin(tab_name)
    add_bc_displacement("y", "y", d, tab_name, y_e)
    add_geom_prop()
    add_mat_mr()
    add_contact_body()
    add_lcase(n_steps)

    #   Save the basic model
    save_model(n_e_l, "bm")

    return

################################################################################

#   Create a 2D node grid on the XY-plane

#   x0:  The initial x-coordinate
#   y0:  The initial y-coordinate
#   x_n: The number of nodes in the x-direction
#   y_n: The number of nodes in the y-direction
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

################################################################################

#   Create an element grid on the node grid

#   x_n: The number of nodes in the x-direction
#   y_n: The number of nodes in the y-direction
def create_elements(x_n, y_n):

    #   Incremental element additions
    for i in range(1, y_n):

        n1 = (i - 1)*x_n + 1
        n2 = n1 + 1
        n3 = n2 + x_n
        n4 = n1 + x_n

        for j in range(1, x_n):

            py_send("*add_elements %d %d %d %d" % (n1, n2, n3, n4))

            n1 = n1 + 1
            n2 = n2 + 1
            n3 = n3 + 1
            n4 = n4 + 1

    m_log.info("%ix%i element grid created" % (x_n - 1, y_n - 1))

    return

################################################################################

#   Find all internal elements
#   Returns a list of internal elements

#   x_e: The number of elements in the x-direction
#   y_e: The number of elements in the y-direction
def find_e_internal(x_e, y_e):

    #   Initialisations
    e_internal = []

    #   Obtain the number of elements
    e_n = x_e * y_e

    #   Loop through all elements
    for i in range(1, e_n + 1):

        #   Check if element is not on the boundary
        if (i > x_e) and (i <= e_n - x_e) and (i % x_e != 0) and (i % x_e != 1):

            #   Add element to the list of internal elements
            e_internal.append(i)

    m_log.info("%i internal elements found" % len(e_internal))

    return e_internal

################################################################################

#   Add a sinusoidal wave to a table

#   tab_name:   The name of the table
def add_sin(tab_name):

    py_send("*new_md_table 1 1")
    py_send("*table_name %s" % tab_name)
    py_send("*set_md_table_type 1 \"time\"")
    py_send("*set_md_table_step_v 1 100")
    py_send("*set_md_table_min_f 1 -1")
    py_send("*set_md_table_step_f 1 100")
    py_send("*set_md_table_method_formula")

    #   The sinusoidal function is defined to go through one full wavelength within 1 second
    py_send("*md_table_formula sin(2*pi*v1)")

    return

################################################################################

#   Add fixed boundary conditions along a specified axis

#   label:  The label of the boundary condition
#   axis:   The axis of the boundary condition
#           "x" or "y"
#   coord:  The axis coordinate of the boundary condition
def add_bc_fixed(label, axis, coord):

    #   Initialisation
    n_l = []

    #   Fetch the total number of nodes
    n_n = py_get_int("nnodes()")

    #   Apply the fixed boundary condition
    py_send("*new_apply")
    py_send("*apply_type fixed_displacement")
    py_send("*apply_name fix_%s" % label)
    py_send("*apply_dof x")
    py_send("*apply_dof y")
    py_send("*apply_dof z")

    #   Incrementally select the correct nodes
    for i in range(1, n_n + 1):

        c = py_get_float("node_%s(%i)" % (axis, i))

        if c == coord:

            n_l.append(i)

    #   Apply the boundary condition to the selected nodes
    py_send("*add_apply_nodes ")

    for i in range(0, len(n_l)):

        py_send("%i " % n_l[i])

    py_send("#")

    return

################################################################################

#   Add displacement boundary conditions along a specified axis

#   label:      The label of the boundary condition
#   axis:       The axis of the boundary condition
#               "x" or "y"
#   d:          The magnitude of the applied displacement
#   tab_name:   The name of the table defining the displacement function
#   coord:      The axis coordinate of the boundary condition
def add_bc_displacement(label, axis, d, tab_name, coord):

    #   Initialisation
    n_l = []

    #   Fetch the total number of nodes
    n_n = py_get_int("nnodes()")

    #   Apply the fixed boundary condition
    py_send("*new_apply")
    py_send("*apply_type fixed_displacement")
    py_send("*apply_name displace_%s" % label)
    py_send("*apply_dof %s" % axis)
    py_send("*apply_dof_value %s %i" % (axis, d))
    py_send("*apply_dof_table %s %s" % (axis, tab_name))

    #   Incrementally select the correct nodes
    for i in range(1, n_n + 1):

        c = py_get_float("node_%s(%i)" % (axis, i))

        if c == coord:

            n_l.append(i)

    #   Apply the boundary condition to the selected nodes
    py_send("*add_apply_nodes ")

    for i in range(0, len(n_l)):

        py_send("%i " % n_l[i])

    py_send("#")

    return

################################################################################

#   Add a load along a specified axis in a specified direction

#   label:      The label of the load
#   p:          The magnitude of the applied pressure
#   tab_name:   The name of the table defining the load function
#   x_e:        The number of elements in the x-direction
#   y_e:        The number of elements in the y-direction
#   axis:       The axis of the load
#               "x" or "y"
#   direc:      The direction of the load with respect to the axis
#               1 for positive and -1 for negative
#   coord:      The axis coordinate of the load
def add_load(label, p, tab_name, x_e, y_e, axis, direc, coord):

    py_send("*new_apply")
    py_send("*apply_type edge_load")
    py_send("*apply_name load_%s" % label)

    #   Apply a pressure with the given magnitude and table
    py_send("*apply_dof p")
    py_send("*apply_dof_value p %i" % p)
    py_send("*apply_dof_table p %s" % tab_name)

    #   Find the correct edges according to the specified axes and directions
    if (axis == "x") and (direc == -1):
        s = 1
        edges = [i*x_e - (x_e - coord) for i in range(1, y_e + 1)]
    elif (axis == "x") and (direc == 1):
        s = 3
        edges = [i*x_e - (x_e - coord) for i in range(1, y_e + 1)]
    elif (axis == "y") and (direc == -1):
        s = 2
        edges = [i + x_e*(coord - 1) for i in range(1, x_e + 1)]
    elif (axis == "y") and (direc == 1):
        s = 4
        edges = [i + x_e*(coord - 1) for i in range(1, x_e + 1)]
        
    #   Apply the load to the correct edges
    py_send("*add_apply_edges")

    if axis == "x":
        for i in range(0, y_e):
            py_send("%i:%i " % (edges[i], s))
    elif axis == "y":
        for i in range(0, x_e):
            py_send("%i:%i " % (edges[i], s))

    py_send("#")

    return

################################################################################

#   Add plane strain geometrical properties

def add_geom_prop():

    py_send("*geometry_type mech_planar_pstrain")
    py_send("*add_geometry_elements all_existing")

    return

################################################################################

#   Add an example Mooney-Rivlin material model

def add_mat_mr():

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

################################################################################

#   Add a preliminary Ogden material model

def add_mat_ogden():

    py_send("*new_mater standard")
    py_send("*mater_option general:state:solid")
    py_send("*mater_option general:skip_structural:off")
    py_send("*mater_name MoldStar15")
    py_send("*mater_option structural:type:ogden")
    py_send("*mater_param structural:ogden_nterm 3")
    py_send("*mater_param structural:ogden_modulus_1 -6.50266e-06")
    py_send("*mater_param structural:ogden_exp_1 -21.322")
    py_send("*mater_param structural:ogden_modulus_2 0.216863")
    py_send("*mater_param structural:ogden_exp_2 1.1797")
    py_send("*mater_param structural:ogden_modulus_3 0.00137158")
    py_send("*mater_param structural:ogden_exp_3 4.88396")
    py_send("*add_mater_elements all_existing")

    return

################################################################################

#   Add a contact body

def add_contact_body():

    py_send("*new_cbody mesh")
    py_send("*contact_option state:solid")
    py_send("*contact_option skip_structural:off")
    py_send("*add_contact_body_elements all_existing")
    
    return

################################################################################

#   Add a loadcase

#   n_steps:    The number of steps in the second of the loadcase
def add_lcase(n_steps):

    py_send("*new_loadcase")
    py_send("*loadcase_type struc:static")
    py_send("*loadcase_value nsteps %i" % n_steps)

    return

################################################################################

#   Add a job

def add_job():

    py_send("*prog_use_current_job on")
    py_send("*new_job structural")
    py_send("*job_name job")
    py_send("*add_job_loadcases lcase1")
    py_send("*job_option strain:large")
    py_send("*job_option follow:on")
    py_send("*add_post_tensor stress_g")
    py_send("*add_post_tensor strain")

    return

################################################################################

#   Run a job

def run_job():

    t0 = time.time()

    py_send("*update_job")
    py_send("*submit_job 1") 
    py_send("*monitor_job")

    t1 = time.time()

    m_log.info("Job run in %fs" % (t1 - t0))

    return

################################################################################

#   Remove a selection of elements

#   rem:    The list of selected elements to be removed
def rem_el(rem):

    #   Loop through the number of elements to be removed
    for i in range(0, len(rem)):

        #   Remove the element from the grid
        py_send("*remove_elements %d #" % rem[i])

    rem_log = list_to_str(rem, ",")

    m_log.info("Removed the following elements from the grid:")
    m_log.info(rem_log)

    return

################################################################################

#   Display all boundary conditions

def view_bc():

    py_send("*identify_applys")
    py_send("*redraw")

    return