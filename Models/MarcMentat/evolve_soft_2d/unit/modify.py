##  Functions used with the Marc Mentat units

#   Imports
from evolve_soft_2d import utility
from evolve_soft_2d.log import m_log

from py_mentat import py_send, py_get_int, py_get_float

import time

################################################################################

#   Open a unit

#   fp_id:  The complete file path of the path to be opened
#   f_id:   The file ID to be logged
def open_unit(fp_id, f_id):

    #   Open the unit
    py_send(r'*open_unit "{}"'.format(fp_id))

    m_log.info("Unit \"grid_{}.mud\" opened".format(f_id))

    return

################################################################################

#   Save a unit

#   fp_id:  The complete file path of the path to be opened
#   f_id:   The file ID to be logged
def save_unit(fp_id, f_id):

    #   Save the unit
    py_send("*set_save_formatted off")
    py_send(r'*save_as_unit "{}" yes'.format(fp_id))

    m_log.info("Unit \"grid_{}.mud\" saved".format(f_id))

    return

################################################################################

#   Create a 2D node grid on the XY-plane

#   x0:  The initial x-coordinate
#   y0:  The initial y-coordinate
#   x_n: The number of nodes in the x-direction
#   y_n: The number of nodes in the y-direction
def create_nodes(template):

    #   Initialisations
    y = template.y0
    z = 0

    #   Loop through the nodes in the y-direction
    for _ in range(0, template.y_n):

        #   Initialise the x-coordinate
        x = template.x0

        #   Loop through the nodes in the x-direction
        for _ in range(0, template.x_n):
            
            #   Add the node
            py_send("*add_nodes {} {} {}".format(x, y, z))

            #   Increment the x-coordinate
            x = x + 1

        #   Increment the y-coordinate
        y = y + 1

    return

################################################################################

#   Create an element grid on the node grid

#   x_n: The number of nodes in the x-direction
#   y_n: The number of nodes in the y-direction
def create_elements(template):

    #   Loop through the elements in the y-direction
    for i in range(1, template.y_n):

        #   Initialise the nodal coordinates
        n1 = (i - 1)*template.x_n + 1
        n2 = n1 + 1
        n3 = n2 + template.x_n
        n4 = n1 + template.x_n

        #   Loop through the elements in the x-direction
        for _ in range(1, template.x_n):

            #   Add the element
            py_send("*add_elements {} {} {} {}".format(n1, n2, n3, n4))

            #   Increment the nodal coordinates
            n1 = n1 + 1
            n2 = n2 + 1
            n3 = n3 + 1
            n4 = n4 + 1

    m_log.info("{}x{} element grid created".format(template.x_n - 1, template.y_n - 1))

    return

################################################################################

#   Add a ramp to a table

#   tab_nam:   The name of the table
def add_ramp(tab_nam):

    py_send("*new_md_table 1 1")
    py_send("*table_name {}".format(tab_nam))
    py_send("*set_md_table_type 1 \"time\"")
    py_send("*set_md_table_step_v 1 100")
    py_send("*set_md_table_step_f 1 100")
    py_send("*set_md_table_method_formula")

    #   The ramp function is defined according to y=x
    py_send("*md_table_formula v1")

    return

################################################################################

#   Add fixed displacement boundary conditions along a specified axis

#   label:      The label of the boundary condition
#   axis:       The axis of the boundary condition
#               "x" or "y"
#   d:          The magnitude of the applied displacement
#   tab_nam:   The name of the table defining the displacement function
#   coord:      The axis coordinate of the boundary condition
def add_bc_fd(label, axis, d, tab_nam, coord):

    #   Initialisation
    n_l = []

    #   Fetch the total number of nodes
    n_n = py_get_int("nnodes()")

    #   Apply the fixed boundary condition
    py_send("*new_apply")
    py_send("*apply_type fixed_displacement")
    py_send("*apply_name bc_fd_{}".format(label))
    py_send("*apply_dof {}".format(axis))
    py_send("*apply_dof_value {} {}".format(axis, d))
    
    if tab_nam != "":
        py_send("*apply_dof_table {} {}".format(axis, tab_nam))

    #   Loop through the number of nodes
    for i in range(1, n_n + 1):

        #   Fetch the relevant coordinate of the current node
        c = py_get_float("node_{}({})".format(axis, i))

        #   Check if the selected coordinate matches the desired coordinate
        if c == coord:

            #   Add the node to the list
            n_l.append(i)

    #   Apply the boundary condition to the selected nodes
    py_send("*add_apply_nodes ")

    #   Loop through the selected nodes
    for i in range(0, len(n_l)):
        py_send("{} ".format(n_l[i]))

    py_send("#")

    return

################################################################################

#   Add a load along a specified axis in a specified direction

#   label:      The label of the load
#   p:          The magnitude of the applied pressure
#   tab_nam:   The name of the table defining the load function
#   x_e:        The number of elements in the x-direction
#   y_e:        The number of elements in the y-direction
#   axis:       The axis of the load
#               "x" or "y"
#   direc:      The direction of the load with respect to the axis
#               1 for positive and -1 for negative
#   coord:      The axis coordinate of the load
def add_load(label, p, tab_nam, x_e, y_e, axis, direc, coord):

    py_send("*new_apply")
    py_send("*apply_type edge_load")
    py_send("*apply_name load_{}".format(label))

    #   Apply a pressure with the given magnitude and table
    py_send("*apply_dof p")
    py_send("*apply_dof_value p {}".format(p))
    py_send("*apply_dof_table p {}".format(tab_nam))

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
            py_send("{}:{} ".format(edges[i], s))
    elif axis == "y":
        for i in range(0, x_e):
            py_send("{}:{} ".format(edges[i], s))

    py_send("#")

    return

################################################################################

#   Add plane strain geometrical properties

def add_geom_prop():

    py_send("*geometry_type mech_planar_pstrain")
    py_send("*add_geometry_elements all_existing")

    return

################################################################################

#   Add a preliminary Ogden material unit

#   ogd_mat:    The Ogden material unit
def add_mat_ogden(ogd_mat):

    py_send("*new_mater standard")
    py_send("*mater_option general:state:solid")
    py_send("*mater_option general:skip_structural:off")
    py_send("*mater_name {}".format(ogd_mat.name))
    py_send("*mater_option structural:type:ogden")
    py_send("*mater_param structural:ogden_nterm 3")
    py_send("*mater_param structural:ogden_modulus_1 {}".format(ogd_mat.mu[0]))
    py_send("*mater_param structural:ogden_exp_1 {}".format(ogd_mat.alpha[0]))
    py_send("*mater_param structural:ogden_modulus_2 {}".format(ogd_mat.mu[1]))
    py_send("*mater_param structural:ogden_exp_2 {}".format(ogd_mat.alpha[1]))
    py_send("*mater_param structural:ogden_modulus_3 {}".format(ogd_mat.mu[2]))
    py_send("*mater_param structural:ogden_exp_3 {}".format(ogd_mat.alpha[2]))
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
    py_send("*loadcase_value nsteps {}".format(n_steps))

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
    py_send("*add_post_var von_mises")
    py_send("*add_post_var te_energy")

    return

################################################################################

#   Run a job

def run_job():

    t0 = time.time()

    py_send("*update_job")
    py_send("*submit_job 1") 
    py_send("*monitor_job")

    t1 = time.time()

    m_log.info("Job run in {:.3f}s".format(t1 - t0))

    return

################################################################################

#   Remove a selection of elements

#   rem:    The list of selected elements to be removed
def rem_el(rem):

    py_send("*remove_elements ")

    #   Loop through the number of elements to be removed
    for i in range(0, len(rem)):

        #   Remove the element from the grid
        py_send("{} ".format(rem[i]))

    py_send("#")

    rem_log = utility.list_to_str(rem, ",")
    m_log.info("Removed the following elements from the grid:")
    m_log.info(rem_log)

    return