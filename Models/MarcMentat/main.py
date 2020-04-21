##  Main program

#   Imports

from evolve_soft_2d import model, result, rep_grid, utility
from evolve_soft_2d.file_paths import fp_bm

from py_mentat import *
from py_post import *

################################################################################

#   Main function

def main():

    #   Initialisations
    
    #   Text name of the table used for the applied load
    table_name = "sin_input"

    #   Number of nodes per axis (one more than number of elements desired)
    x_n = 6
    y_n = 6

    #   Number of elements per axis
    x_e = x_n - 1
    y_e = y_n - 1
    n_e = [x_e, y_e]
    n_e_l = utility.list_to_str(n_e, "x")

    #   Coordinates of initial position
    x0 = 0
    y0 = 0

    #   Number of increments per second to analyse
    n_steps = 20

    #   Magnitude of the applied load and/or displacement
    #   p_mag = 25
    d_mag = 1

    #   File name of the base element
    fp_b = fp_bm + r'\grid_' + n_e_l + r'\grid_' + n_e_l + '.mud'

    #   Flag to be set if the base model needs to be regenerated
    regen_base = False

    #   Check if the base file already exists
    exists = utility.if_file_exist(fp_b)

    #   Open the base file if it exists
    if exists and not regen_base:
        model.open_model(n_e_l, "", "bm")

    #   Create the base file if it does not exist
    else:
        model.create_base_model(x0, y0, x_n, y_n, x_e, y_e, table_name, d_mag, n_steps, n_e_l)

    #   A grid of ones is created reflecting the grid of elements created
    grid = rep_grid.create_grid(x_e, y_e)

    #   Find the internal elements
    e_internal = model.find_e_internal(x_e, y_e)

    #   Random element removal
    rem = utility.sel_random(e_internal)
    model.rem_el(rem)
    grid = rep_grid.rem_el_grid(grid, x_e, rem)

    #   Search for cluster
    (found_free, grid_label) = rep_grid.find_cluster(grid)

    #   Check if free clusters were found
    if found_free:

        #   Remove the free clusters
        (grid, rem_free) = rep_grid.rem_el_free_grid(grid, grid_label, x_e, y_e)
        model.rem_el(rem_free)

        #   Update the list of removed elements
        rem = utility.add_sort_list(rem, rem_free)

    #   Convert the list of removed elements to a string for file naming purposes
    rem_l = utility.list_to_str(rem, "_")
    f_id = utility.gen_hash(rem_l)

    #   Display the boundary conditions
    model.view_bc()

    #   Add the job
    model.add_job()

    #   Save the altered model
    model.save_model(f_id, n_e_l, "m")

    #   Run the job 
    model.run_job()

    #   Check the existence and validity of results
    run_success = result.check_out(f_id, n_e_l)
    if run_success:

        #   Inspect the results
        result.res_val(f_id, n_e_l, n_steps)

    return

if __name__ == '__main__':

    py_connect("", 40007)

    main()
    
    py_disconnect