##  Functions used in main program

#   Imports

from py_mentat import *
from py_post import *

import csv
import time
import os.path
import re

import numpy as np

from pathlib import Path
from pylab import *
from scipy.ndimage import measurements

################################################################################

#   Wait for a specified time

#   t:  The time in seconds to wait
#   f:  The object being waited for
def wait(t, f):

    print("Waiting for %s..." % f)

    time.sleep(t)

    return

################################################################################

#   Wait until a specified file exists

#   file_name:  The name of the file to be waited for
#   label:      The label for the output message
#   t:          The time in seconds to wait per loop
def wait_file_exist(file_name, label, t):

    #   Loop until the file exists
    while 1:

        #   Check if the file exists
        exists = os.path.exists(file_name)

        #   Break out of the loop if the file exists
        if exists:
            print("%s file exists" % label)
            break

        #   Wait and check again
        else:
            wait(t, "%s file to be created..." % label)

    return

################################################################################

#   Wait until a specified file is updated

#   file_name:  The name of the file to be waited for
#   t0:         The time since which the file should have been updated
#   label:      The label for the output message
#   t:          The time in seconds to wait per loop
def wait_file_update(file_name, t0, label, t):

    #   Loop until the file has been updated
    while 1:

        #   See how recently the file has been updated
        t_mod = os.path.getmtime(file_name)

        #   Break out of the loop if the file has been updated since the given time
        if t_mod > t0:
            print("%s file updated" % label)
            break

        #   Wait and check again
        else:
            wait(t, "%s file to be updated..." % label)

    return

################################################################################

#   Check if a specified file exists
#   Returns whether or not it exists

#   file_name:  The name of the file to be waited for
#   label:      The label for the output message
def if_file_exist(file_name, label):

    #   Check if the file exists
    exists = os.path.exists(file_name)

    #   Indicate if the file exists or not
    if exists:
        print("%s file exists" % label)
    else:
        print("%s file does not exist" % label)

    return exists

################################################################################

#   Display all boundary conditions

def view_bc():

    py_send("*identify_applys")
    py_send("*redraw")

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

    #   Add the loads, boundary conditions, geometric properties and material
    add_bc_fixed("y", "y", y0)
    add_sin(tab_name)
    add_bc_displacement("y", "y", d, tab_name, y_e)
    add_geom_prop()
    add_mat_mr()
    add_contact_body()
    add_lcase(n_steps)

    #   Save the basic model
    save_model(n_e_l)

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

    print("%ix%i node grid created" % (x_n, y_n))

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

    print("%ix%i element grid created" % (x_n - 1, y_n - 1))

    return

################################################################################

#   Create an element network
#   Returns the element network

#   e_id:   The element IDs
#   e_n_id: The element node IDs
def create_e_net(e_id, e_n_id):

    #   Initialisations
    e_net = []

    #   Obtain the nummber of elements
    e_n = py_get_int("nelements()")

    #   Print the output    
    # print("Element ID|Networked Elements")
    # print("-----------------------------")

    #   Loop through all elements
    for i in range(0, e_n):

        e_net.append([])

        #   Loop through all previous elements
        for j in range(0, len(e_net) - 1):

            #   Check if the element is already in another element's network
            if e_id[i] in e_net[j]:

                #   Add that element to the new network
                e_net[i].append(e_id[j])

        #   Loop through all subsequent elements
        for j in range(i + 1, e_n):

            #   Obtain all shared nodes between selected elements
            n_share = [k for k in e_n_id[i] if k in e_n_id[j]]

            #   Check if the elements share 2 nodes
            if len(n_share) == 2:

                #   Add that element to the new network
                e_net[i].append(e_id[j])

        # print("%-10i|%s" % (e_id[i], e_net[i]))

    print("Element network created")

    return e_net

################################################################################

#   Create a grid of ones representative of the model
#   Returns the representative grid

#   x_e: The number of elements in the x-direction
#   y_e: The number of elements in the y-direction
def create_grid(x_e, y_e):

    grid = [[1]*(x_e) for i in range(y_e)]

    print("Representative grid created")

    return grid

################################################################################

#   Find all element IDs and their respective node IDs
#   Returns the element IDs and their respective node IDs

def find_e_n_ids():

    #   Initialisations
    e_id = []
    e_n_id = []

    #   Obtain the nummber of elements
    e_n = py_get_int("nelements()")

    #   Print the output
    # print("Element ID|Nodes")
    # print("---------------------------")

    #   Loop through all elements
    for i in range(1, e_n + 1):

        #   Store the element ID
        e_id.append(py_get_int("element_id(%i)" % i))

        e_n_id.append([])

        #   Loop through all nodes in an element
        for j in range(1, 5):

            #   Store the node IDs
            e_n_id[i - 1].append(py_get_int("element_node_id(%i,%i)" % (e_id[i - 1], j)))

    #     print("%-10i|%s" % (e_id[i - 1], e_n_id[i - 1]))

    # print("---------------------------")

    print("Element node IDs found")

    return (e_id, e_n_id)

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

    print("%i internal elements found" % len(e_internal))

    return e_internal
 
################################################################################

#   Find all clusters of elements using the representative grid
#   Returns a grid with clusters incrementally labelled

#   grid:   Representative grid of ones
def find_cluster(grid):

    grid_label, cluster = measurements.label(grid)

    #   Check if more than one cluster is found
    if cluster > 1:

        #   Set flag
        found = True

        if cluster == 2:
            print("Warning: %i free cluster found!" % (cluster - 1))
        else:
            print("Warning: %i free clusters found!" % (cluster - 1))

    else:

        #   Set flag
        found = False

        print("No free clusters found")

    return (found, grid_label)

################################################################################

#   Search a text file for the first occurrence of a given text string
#   Returns if the text was found and the entire line it was found in

#   file_name:  The name of the file to be searched through
#   find_text:  The text to be searched for
def search_text_file(file_name, find_text):

    #   Initialisations
    found_text = ""
    found = False

    #   Open the file to be read
    with open(file_name, "rt") as f:

        #   Loop through every line in the file until the text string
        for line in f:

            #   Check if the text is in the current line of the file
            if find_text.search(line) != None:

                #   Save the entire line of text containing the desired text
                found_text = line.rstrip("\n")

                #   Set the found flag to true
                found = True

                break

    return (found, found_text)

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

    print("Table \"%s\" added" % tab_name)

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

    print("Fixed boundary condition \"fix_%s\" added to the %s-axis at coordinate %i" % (label, axis, coord))

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

    print("Displacement boundary condition \"displace_%s\" of magnitude %i added to the %s-axis at coordinate %i" % (label, d, axis, coord))

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

    print("Load boundary condition \"load_%s\" of magnitude %i added to the %s-axis at coordinate %i in direction %i" % (label, p, axis, coord, direc))

    return

################################################################################

#   Add plane strain geometrical properties

def add_geom_prop():

    py_send("*geometry_type mech_planar_pstrain")
    py_send("*add_geometry_elements all_existing")

    print("Geometric properties added")

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

    print("Mooney-Rivlin material model added")

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

    print("Ogden material model added")

    return

################################################################################

#   Add a contact body

def add_contact_body():

    py_send("*new_cbody mesh")
    py_send("*contact_option state:solid")
    py_send("*contact_option skip_structural:off")
    py_send("*add_contact_body_elements all_existing")

    print("Contact body added")
    
    return

################################################################################

#   Add a loadcase

#   n_steps:    The number of steps in the second of the loadcase
def add_lcase(n_steps):

    py_send("*new_loadcase")
    py_send("*loadcase_type struc:static")
    py_send("*loadcase_value nsteps %i" % n_steps)

    print("Loadcase added")

    return

################################################################################

#   Add a job

#   rem:    The element ID of the removed element
def add_job():

    py_send("*prog_use_current_job on")
    py_send("*new_job structural")
    py_send("*job_name job")
    py_send("*add_job_loadcases lcase1")
    py_send("*job_option strain:large")
    py_send("*job_option follow:on")
    py_send("*add_post_tensor stress_g")
    py_send("*add_post_tensor strain")

    print("Job added")

    return

################################################################################

#   Run a job

def run_job():

    t0 = time.time()

    py_send("*update_job")
    py_send("*submit_job 1") 
    py_send("*monitor_job")

    t1 = time.time()

    print("Job run in %fs" % (t1 - t0))

    return

################################################################################

#   Check if the updated output files exist
#   Returns a flag based on the successful output of the model

#   rem_l:  String containing all removed elements
def check_out(rem_l):

    #   Initialisations
    t0 = time.time()
    success = False

    #   Time to wait for files
    t = 1

    #   Text to look for when searching the log files
    exit_n = re.compile("exit number", re.IGNORECASE)

    #   File paths to the respective model and output file
    file_mud = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Models\MarcMentat\element_' + rem_l + '.mud'
    file_log = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Models\MarcMentat\element_' + rem_l + '_job.log'
    file_t16 = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Models\MarcMentat\element_' + rem_l + '_job.t16'

    #   Obtain the timestamp of the last time the model file was modified
    t_mud = os.path.getmtime(file_mud)

    #   Wait until the log file exists and has been updated
    wait_file_exist(file_log, "log", t)
    wait_file_update(file_log, t_mud, "log", t)

    #   Loop until an exit number is detected
    while 1:

        #   Search the log file for an exit number
        (found, found_exit_n) = search_text_file(file_log, exit_n)

        #   Check if an exit number was found
        if found:

            #   Output the exit number
            print("Exit number found")
            print(found_exit_n)

            #   Exit the loop
            break

        #   Wait and check again
        else:
            wait(t, "exit number to be found")

    #   Check if the exit number indicates a successful run
    if found_exit_n.find("3004") != -1:

        #   Set the success flag
        success = True

        print("Model run successfully")

    #   Output a warning
    else:

        print("Warning: Model run unsuccessfully!")
        print("Check log file and exit number for details")

    #   Check if the model was run successfully
    if success:

        #   Wait until the t16 file exists and has been updated
        wait_file_exist(file_t16, "t16", t)
        wait_file_update(file_t16, t_mud, "t16", t)

        t1 = time.time()

        print("Results generated in approximately %fs" % (t1 - t0))
        
    return success

################################################################################

#   Obtain maximum and minimum values from results

#   rem:        The element IDs of the removed elements
#   n_steps:    The number of steps in the second of the loadcase
def res_val(rem_l, n_steps):

    #   Initialisations

    #   Empty lists for the values and their respective nodes and timestamps
    max_v = []
    max_n = []
    max_t = []
    min_v = []
    min_n = []
    min_t = []

    #   The labels of the desired results
    label = []
    label.append("Displacement X")
    label.append("Displacement Y")
    label.append("Normal Global Stress Layer 1")
    label.append("Shear Global Stress Layer 1")
    label.append("Normal Total Strain")
    label.append("Shear Total Strain")

    #   Open the results file
    py_send("@main(results) @popup(modelplot_pm) *post_open element_%s_job.t16" % rem_l)
    py_send("*post_numerics")

    #   Loop through all given labels
    for i in range(0, len(label)):

        #   Initialise lists for the current label
        max_v.append(0)
        max_n.append(0)
        max_t.append(0)

        min_v.append(0)
        min_n.append(0)
        min_t.append(0)

        #   Rewind the post file to the initial step
        py_send("*post_rewind")

        #   Set the post file to the current label
        py_send("*post_value %s" % label[i])

        # print("%s" % label[i])
        # print("-----------------------------")
        # print("Time|Node|Max   |Node|Min")
        # print("-----------------------------")

        #   Loop through all steps of the post file
        for j in range(0, n_steps + 1):
            
            #   Obtain the current maximum and minimum values
            max_n_c = py_get_float("scalar_max_node()")
            max_v_c = py_get_float("scalar_1(%i)" % max_n_c)

            min_n_c = py_get_float("scalar_min_node()")
            min_v_c = py_get_float("scalar_1(%i)" % min_n_c)

            # print("%4.2f|%4i|%6.3f|%4i|%7.3f" % (j/n_steps, max_n_c, max_v_c, min_n_c, min_v_c))

            #   Check if the current value is the overall maximum and minimum value
            if max_v_c > max_v[i]:

                max_v[i] = max_v_c
                max_n[i] = max_n_c
                max_t[i] = j/n_steps

            if min_v_c < min_v[i]:

                min_v[i] = min_v_c
                min_n[i] = min_n_c
                min_t[i] = j/n_steps

            #   Increment the post file
            py_send("*post_next")

        # print("-----------------------------")

    #   Rewind the post file
    py_send("*post_rewind")

    #   Write the results to csv files
    save_csv("max", "v", rem_l, max_v)
    save_csv("max", "n", rem_l, max_n)
    save_csv("max", "t", rem_l, max_t)
    save_csv("min", "v", rem_l, min_v)
    save_csv("min", "n", rem_l, min_n)
    save_csv("min", "t", rem_l, min_t)

    #   Print the minimum and maximum values
    print("---------------------------------------------------------------")
    print("Label                       |Time|Node|Max   |Time|Node|Min")
    print("---------------------------------------------------------------")

    for i in range(0, len(label)):

        print("%-28s|%4.2f|%4i|%6.3g|%4.2f|%4i|%7.3g" % (label[i], max_t[i], max_n[i], max_v[i], min_t[i], min_n[i], min_v[i]))

    print("---------------------------------------------------------------")

    print("Results analysed")

    return

################################################################################

#   Remove a random number of elements
#   Returns the element IDs that were removed

#   e_internal: The list of the internal elements in the grid
def rem_el(e_internal):

    #   Initialisations
    rem = []

    #   Generate a random number determining how many internal elements will be removed
    rem_n = np.random.randint(low = 1, high = len(e_internal))

    #   Loop through the number of elements to be removed
    for i in range(0, rem_n):
        
        #   Generate a random element ID from the list of internal elements
        rem.append(np.random.choice(np.asarray(e_internal)))

        #   Remove the element from the grid
        py_send("*remove_elements %d #" % rem[i])

        #   Remove the element ID from the list of internal elements to prevent the same ID from being selected more than once
        e_internal.remove(rem[i])

    #   Sort the list of removed element IDs
    rem.sort()

    print("Removed random internal elements")

    return rem

################################################################################

#   Remove any free elements

#   rem:    The list of free elements to be removed
def rem_el_free(rem):

    #   Loop through all elements to be removed
    for i in range(0, len(rem)):

        #   Remove the element
        py_send("*remove_elements %i #" % rem[i])

    print("Removed free clusters")

    return

################################################################################

#   Removes elements from the representative grid
#   Returns the grid with a zero in the place of the removed element

#   grid:   Representative grid of ones
#   x_e:    The number of elements in the x-direction
#   rem:    The element IDs of the elements to be removed
def rem_el_grid(grid, x_e, rem):

    #   Loop through the number of elements to be removed
    for i in range(0, len(rem)):

        #   Remove the element from the grid
        grid[x_e - (rem[i] - 1)//x_e - 1][rem[i]%x_e - 1] = 0
        
    print("Removed same random internal elements from representative grid")

    return grid

################################################################################

#   Remove free element clusters from the representative grid
#   Returns the grid with zeros in place of the removed elements and a list of the removed elements

#   grid:       Representative grid of ones
#   grid_label: Representative grid with clusters incrementally labelled
#   x_e:        The number of elements in the x-direction
#   y_e:        The number of elements in the y-direction
def rem_el_free_grid(grid, grid_label, x_e, y_e):

    #   Initialisations
    rem_i = 1
    rem = []

    #   Loop through the elements in the x-direction
    for i in range(0, x_e):

        #   Loop through the elements in the y-direction
        for j in range(0, y_e):

            #   Check if the labelled grid has an element numbered greater than 1
            if grid_label[x_e - i - 1][j] > 1:

                #   Remove the element from the grid
                grid[x_e - (rem_i - 1)//x_e - 1][rem_i%x_e - 1] = 0

                #   Add the index of the element to the list of removed elements
                rem.append(rem_i)

            #   Increment the removed element counter
            rem_i = rem_i + 1

    print("Removed free clusters from representative grid")

    return (grid, rem)

################################################################################

#   Append removed free elements to list of initially removed elements
#   Returns the complete and sorted list of removed elements

#   rem:        The element IDs of the original elements removed
#   rem_free:   The element IDs of the free elements removed
def append_rem(rem, rem_free):

    #   Append the newly removed element IDs to the originally removed IDs
    rem = rem + rem_free

    #   Sort the list of removed element IDs
    rem.sort()

    return rem

################################################################################

#   Convert a list into a string connected by a given symbol
#   Returns the string

#   l:  The list to be converted
#   c:  The symbol to be inserted between list items
def list_to_str(l, c):

    s = c.join(map(str, l))

    return s

################################################################################

#   Save a model

def save_model(l):

    py_send("*set_save_formatted off")
    py_send("*save_as_model element_%s.mud yes" % l)

    print("Model %s saved" % l)

    return

################################################################################

#   Write the results to .csv files

#   m:      Minimum or maximum
#   t:      Type of value
#   i:      ID of the results being written
#   data:   Data to be written
def save_csv(m, t, i, data):

    file_path = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Models\MarcMentat\Results'

    Path(file_path).mkdir(parents = True, exist_ok = True)

    file_name = m + "_" + t + "_" + i + ".csv"

    with open(file_path + "\\" + file_name, 'w') as f:

        wr = csv.writer(f)
        wr.writerow(data)

    print("%s saved" % file_name)

    return

################################################################################

#   Open a model

def open_model(l):

    py_send("*open_model \"element_%s.mud\"" % l)

    print("Model %s opened" % l)

    return