##  Functions used in main program

#   Imports

from py_mentat import *
from py_post import *

import csv
import time
import random
import os.path

from pathlib import Path
from pylab import *
from scipy.ndimage import measurements

################################################################################

#   Display all boundary conditions

def view_bc():

    py_send("*identify_applys")
    py_send("*redraw")

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
    print("Element ID|Networked Elements")
    print("-----------------------------")

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

        print("%-10i|%s" % (e_id[i], e_net[i]))

    return e_net

################################################################################

#   Create a grid of ones representative of the model
#   Returns the representative grid

#   x_e: The number of elements in the x-direction
#   y_e: The number of elements in the y-direction
def create_grid(x_e, y_e):

    grid = [[1]*(x_e) for i in range(y_e)]

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
    print("Element ID|Nodes")
    print("---------------------------")

    #   Loop through all elements
    for i in range(1, e_n + 1):

        #   Store the element ID
        e_id.append(py_get_int("element_id(%i)" % i))

        e_n_id.append([])

        #   Loop through all nodes in an element
        for j in range(1, 5):

            #   Store the node IDs
            e_n_id[i - 1].append(py_get_int("element_node_id(%i,%i)" % (e_id[i - 1], j)))

        print("%-10i|%s" % (e_id[i - 1], e_n_id[i - 1]))

    print("---------------------------")

    return (e_id, e_n_id)

################################################################################

#   Find all internal elements
#   Returns a list of internal elements

#   x_e: The number of elements in the x-direction
def find_e_internal(x_e, y_e):

    #   Initialisations
    e_internal = []

    #   Obtain the nummber of elements
    e_n = x_e * y_e

    #   Loop through all elements
    for i in range(1, e_n + 1):

        #   Check if element is not on the boundary
        if (i > x_e) and (i <= e_n - x_e) and (i % x_e != 0) and (i % x_e != 1):

            #   Add element to the list of internal elements
            e_internal.append(i)

    return e_internal
 
################################################################################

#   Find all clusters of elements using the representative grid
#   Returns a grid with clusters incrementally labelled

#   grid:   Representative grid of ones
def find_cluster(grid):

    grid_label, cluster = measurements.label(grid)

    if cluster > 1:

        print("Warning: Found %i free clusters!" % cluster)

    return grid_label

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

# Add a load to the right and top sides of the element

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

    #   Apply a pressure with an amplitude of 20 and the sinusoidal wave
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

#   Add a loadcase

#   n_steps:    The number of steps in the second of the loadcase
def add_lcase(n_steps):

    py_send("*new_loadcase")
    py_send("*loadcase_type struc:static")
    py_send("*loadcase_value nsteps %i" % n_steps)

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

    return

################################################################################

#   Run a job

def run_job():

    py_send("*update_job")
    py_send("*submit_job 1") 
    py_send("*monitor_job")

    return

################################################################################

#   Check if the updated .t16 output file exists

#   rem:    The element ID of the removed element
def check_t16(rem):

    rem_l = '_'.join(map(str, rem))

    #   File paths to the respective model and output file
    file_mud = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Models\MarcMentat\element_' + rem_l + '.mud'
    file_t16 = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Models\MarcMentat\element_' + rem_l + '_job.t16'

    #   Obtain the timestamp of the last time the model file was modified
    t_mud = os.path.getmtime(file_mud)

    #   Loop until the output file has been updated
    while 1:

        #   Check to see if the output file exists
        exist_t16 = os.path.exists(file_t16)

        if exist_t16:

            #   Check to see if the output file has been modified after the model file
            t_t16 = os.path.getmtime(file_t16)

            if t_t16 > t_mud:

                #   Exit the loop
                break
        
        #   Check the status only every 5 seconds so that the CPU is not constantly occupied
        time.sleep(5)

    return

################################################################################

#   Obtain maximum and minimum values from results

#   rem:        The element ID of the removed element
#   n_steps:    The number of steps in the second of the loadcase
def res_val(rem, n_steps):

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
    rem_l = '_'.join(map(str, rem))
    py_send("@main(results) @popup(modelplot_pm) *post_open element_%s_job.t16" % rem_l)

    #   Obtain the total number of nodes
    n_n = py_get_int("nnodes()")

    print("Number Of Nodes: %i" % n_n)
    print("-------------------")

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

        print("%s" % label[i])
        print("-----------------------------")
        print("Time|Node|Max   |Node|Min")
        print("-----------------------------")

        #   Loop through all steps of the post file
        for j in range(0, n_steps + 1):
            
            #   Obtain the current maximum and minimum values
            max_n_c = py_get_float("scalar_max_node()")
            max_v_c = py_get_float("scalar_1(%i)" % max_n_c)

            min_n_c = py_get_float("scalar_min_node()")
            min_v_c = py_get_float("scalar_1(%i)" % min_n_c)

            print("%4.2f|%4i|%6.3f|%4i|%7.3f" % (j/n_steps, max_n_c, max_v_c, min_n_c, min_v_c))

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

        print("-----------------------------")

    #   Rewind the post file
    py_send("*post_rewind")

    #   Write the results to csv files
    save_csv("max", "v", rem_l, max_v)
    save_csv("max", "n", rem_l, max_n)
    save_csv("max", "t", rem_l, max_t)
    save_csv("min", "v", rem_l, min_v)
    save_csv("min", "n", rem_l, min_n)
    save_csv("min", "t", rem_l, min_t)

    #   Print the minimum and maximum values while selecting the respective nodes
    print("Label                       |Time|Node|Max   |Time|Node|Min")
    print("---------------------------------------------------------------")

    for i in range(0, len(label)):

        print("%-28s|%4.2f|%4i|%6.3g|%4.2f|%4i|%7.3g" % (label[i], max_t[i], max_n[i], max_v[i], min_t[i], min_n[i], min_v[i]))

    print("---------------------------------------------------------------")

    return

################################################################################

#   Remove a random number of elements
#   Returns the element IDs that were removed

#   e_internal: The list of the internal elements in the grid
def rem_el(e_internal):

    # rem = []

    rem = [13, 17]

    # rem_n = randint(1, len(e_internal))

    # for i in range(0, rem_n):

    for i in range(0, len(rem)):
        
        # rem.append(random.choice(e_internal))

        py_send("*remove_elements %d #" % rem[i])

        # e_internal.remove(rem[i])

    rem.sort()

    return rem

################################################################################

#   Remove any free elements

#   e_id:   The element IDs
#   e_net:  The network of elements
def rem_el_free(e_id, e_net):

    #   Obtain the nummber of elements
    e_n = py_get_int("nelements()")

    #   Loop through all elements
    for i in range(0, e_n):

        #   Check if an element is connected to no other elements
        if len(e_net[i]) < 1:

            #   Remove the element
            py_send("*remove_elements %d #" % e_id[i])

            #   Print which element was removed
            print("Removed element %i" % e_id[i])
    
    return

################################################################################

#   Removes elements from the representative grid
#   Returns the grid with a zero in the place of the removed element

#   grid:   Representative grid of ones
#   x_e:    The number of elements in the x-direction
#   rem:    The element IDs of the element to be removed
def rem_el_grid(grid, x_e, rem):

    for i in range(0, len(rem)):

        grid[x_e - (rem[i] - 1)//x_e - 1][rem[i]%x_e - 1] = 0

    return grid

################################################################################

#   Remove free element clusters from the representative grid
#   Returns the grid with zeros in place of the removed elements and a list of the removed elements

#   grid:       Representative grid of ones
#   grid_label: Representative grid with clusters incrementally labelled
#   x_e:    The number of elements in the x-direction
#   y_e:    The number of elements in the y-direction
def rem_cl_grid(grid, grid_label, x_e, y_e):

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
                grid = rem_el_grid(grid, x_e, rem_i)

                #   Add the index of the element to the list of removed elements
                rem.append(rem_i)

            #   Increment the removed element counter
            rem_i = rem_i + 1

    return (grid, rem)

################################################################################

#   Save the basic model

def save_bas_model():

    py_send("*set_save_formatted off")
    py_send("*save_as_model element_basic.mud yes")

    return

################################################################################

#   Save a model referenced by the removed element

#   rem: The element ID of the removed element
def save_rem_model(rem):

    rem_l = '_'.join(map(str, rem))
    py_send("*set_save_formatted off")
    py_send("*save_as_model element_%s.mud yes" % rem_l)

    return

################################################################################

#   Write the results to .csv files

#   m:      Minimum or maximum
#   t:      Type of value
#   id:     ID of the results being written
#   data:   Data to be written
def save_csv(m, t, i, data):

    file_path = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Models\MarcMentat\Results'

    Path(file_path).mkdir(parents = True, exist_ok = True)

    file_name = m + "_" + t + "_" + i + ".csv"

    with open(file_path + "\\" + file_name, 'w') as f:

        wr = csv.writer(f)
        wr.writerow(data)

    return