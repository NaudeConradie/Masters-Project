##  Main program

#   Imports

from py_mentat import *
from py_post import *

import csv
import time
import random
import os.path

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

    time.sleep(1)
    py_send("*identify_applys")
    py_send("*redraw")
    py_send("*fill_view")
    time.sleep(1)

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
    py_send("*add_post_tensor stress_g")
    py_send("*add_post_tensor strain")

    return

###################################################################

#   Run a job

def run_job():

    py_send("*update_job")
    py_send("*submit_job 1") 
    py_send("*monitor_job")

    return

###################################################################

#   Check if the updated .t16 output file exists

def check_t16(rem):

    file_mud = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Models\MarcMentat\element_' + str(rem) + '.mud'
    file_t16 = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Models\MarcMentat\element_' + str(rem) + '_job_' + str(rem) + '.t16'

    t_mud = os.path.getmtime(file_mud)

    while 1:

        exist_t16 = os.path.exists(file_t16)

        if exist_t16:

            t_t16 = os.path.getmtime(file_t16)

            if t_t16 > t_mud:

                break
        
        time.sleep(5)

###################################################################

#   Open the results file and create gifs of the selected results

def res_gif(rem):

    py_send("*post_open_default")

    py_send("*post_contour_bands")
    
    py_send("*post_value Equivalent Von Mises Stress")
    py_send("*animation_name element_%d_evms" % rem)
    py_send("*gif_animation_make")
    time.sleep(5)
    py_send("*post_rewind")

    py_send("*post_value Total Strain Energy Density")
    py_send("*animation_name element_%d_tsed" % rem)
    py_send("*gif_animation_make")
    time.sleep(5)
    py_send("*post_rewind")

    py_send("*post_value Displacement")
    py_send("*animation_name element_%d_disp" % rem)
    py_send("*gif_animation_make")
    time.sleep(5)
    py_send("*post_rewind")

    return

###################################################################

#   Obtain maximum and minimum values from results

def res_val(rem):

    py_send("@main(results) @popup(modelplot_pm) *post_open element_%i_job_%i.t16" % (rem, rem))

    #   Initialisations
    max_label = []
    max_tensor = []
    max_n = []
    max_i =[]

    min_label = []
    min_tensor = []
    min_n = []
    min_i =[]

    label = []
    label.append("Displacement X")
    label.append("Displacement Y")
    label.append("Normal Global Stress Layer 1")
    label.append("Shear Global Stress Layer 1")
    label.append("Normal Total Strain")
    label.append("Shear Total Strain")

    #   Obtain the total number of nodes
    n_n = py_get_int("nnodes()")
    print("Number Of Nodes: %i" % n_n)

    for i in range(0, len(label)):

        max_tensor.append(0)
        max_n.append(0)
        max_i.append(0)

        min_tensor.append(0)
        min_n.append(0)
        min_i.append(0)

        py_send("*post_rewind")

        py_send("*post_value %s" % label[i])

        print("%s" % label[i])

        print("-----------------------------")
        print("Time|Node|Max   |Node|Min")
        print("-----------------------------")

        for j in range(0, 21):

            n_max = py_get_float("scalar_max_node()")
            t_max = py_get_float("scalar_1(%d)" % n_max)

            n_min = py_get_float("scalar_min_node()")
            t_min = py_get_float("scalar_1(%d)" % n_min)

            print("%4i|%4i|%6.3f|%4i|%7.3f" % (j, n_max, t_max, n_min, t_min))

            if t_max > max_tensor[i]:

                max_tensor[i] = t_max
                max_n[i] = n_max
                max_i[i] = j

            if t_min < min_tensor[i]:

                min_tensor[i] = t_min
                min_n[i] = n_min
                min_i[i] = j

            py_send("*post_next")

        print("-----------------------------")

    py_send("*post_rewind")

    # max_s_np = numpy.asarray(max_scalar)
    # numpy.savetxt("max_s.csv", max_s_np, delimiter=",")

    max_csv = "max_t_" + str(rem) + ".csv"

    with open(max_csv, 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(max_tensor)

    min_csv = "min_t_" + str(rem) + ".csv"

    with open(min_csv, 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(min_tensor)

    py_send("*unpost_nodes all_existing")
    py_send("*post_nodes")

    print("Label                       |Time|Node|Max   |Time|Node|Min")
    print("---------------------------------------------------------------")

    for i in range(0, len(label)):

        print("%-28s|%4i|%4i|%6.3g|%4i|%4i|%7.3g" % (label[i], max_i[i], max_n[i], max_tensor[i], min_i[i], min_n[i], min_tensor[i]))
        py_send("%i" % max_n[i])
        py_send("%i" % min_n[i])

    print("---------------------------------------------------------------")

    py_send("#")

    py_send("*post_numerics")

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