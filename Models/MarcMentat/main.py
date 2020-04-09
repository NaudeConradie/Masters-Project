##  Main program

#   Imports

from py_mentat import *
from py_post import *

from functions import *

################################################################################

#   Main function

def main(): 

    #   Initialisations
    
    #   Text name of the table used for the applied load
    table_name = "sin_input"

    #   Number of nodes per axis (one more than number of elements desired)
    x_n = 6
    y_n = 6
    x_e = x_n - 1
    y_e = y_n - 1

    #   Coordinates of initial position
    x0 = 0
    y0 = 0

    #   Number of increments per second to analyse
    n_steps = 20

    #   Magnitude of the applied load
    p_mag = 25

    #   Clear the workspace
    py_send("*new_model yes")

    #   Grid construction
    create_nodes(x0, y0, x_n, y_n)
    create_elements(x_n, y_n)

    #   A grid of ones is created reflecting the grid of elements created
    grid = create_grid(x_e, y_e)

    #   Find the internal elements
    e_internal = find_e_internal(x_e, y_e)

    #   Add the loads, boundary conditions, geometric properties and material
    # add_bc_fixed("x", "x", x0)
    add_bc_fixed("y", "y", y0)
    add_sin(table_name)
    add_bc_displacement("y", "y", 1, table_name, y_e)
    # add_load("x", p_mag, table_name, x_e, y_e, "x", -1, x_e)
    # add_load("y", p_mag, table_name, x_e, y_e, "y", -1, y_e)
    add_geom_prop()
    add_mat_mr()
    add_lcase(n_steps)

    #   Save the basic model
    save_bas_model()

    #   Random element removal
    rem = rem_el(e_internal)
    grid = rem_el_grid(grid, x_e, rem)

    #   Create the network of the current elements
    # (e_id, e_n_id) = find_e_n_ids()
    # e_net = create_e_net(e_id, e_n_id)

    #   Search for cluster
    (found_free, grid_label) = find_cluster(grid)

    #   Check if free clusters were found
    if found_free:

        #   Remove the free clusters
        (grid, rem_free) = rem_el_free_grid(grid, grid_label, x_e, y_e)
        rem_el_free(rem_free)

        #   Update the list of removed elements
        rem = append_rem(rem, rem_free)

    #   Convert the list of removed elements to a string for file naming purposes
    rem_l = list_to_str(rem)

    #   Display the boundary conditions
    view_bc()

    #   Add the job
    add_job()

    #   Save the altered model
    save_rem_model(rem_l)

    #   Run the job 
    run_job()

    #   Check the existence and validity of results
    run_success = check_out(rem_l)
    if run_success:

        #   Inspect the results
        res_val(rem_l, n_steps)

    return

if __name__ == '__main__':

    py_connect("", 40007)

    main()
    
    py_disconnect