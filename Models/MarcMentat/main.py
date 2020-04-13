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
    x_n = 9
    y_n = 9

    #   Number of elements per axis
    x_e = x_n - 1
    y_e = y_n - 1
    n_e = [x_e, y_e]
    n_e_l = list_to_str(n_e, "x")

    #   Coordinates of initial position
    x0 = 0
    y0 = 0

    #   Number of increments per second to analyse
    n_steps = 20

    #   Magnitude of the applied load and/or displacement
    p_mag = 25
    d_mag = 1

    #   File name of the base element
    file_base = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Models\MarcMentat\element_' + n_e_l + '.mud'

    #   Flag to be set if the base model needs to be regenerated
    regen_base = False

    #   Check if the base file already exists
    exists = if_file_exist(file_base, "Base")

    #   Open the base file if it exists
    if exists and not regen_base:
        open_model(n_e_l)

    #   Create the base file if it does not exist
    else:
        create_base_model(x0, y0, x_n, y_n, x_e, y_e, table_name, d_mag, n_steps, n_e_l)

    #   A grid of ones is created reflecting the grid of elements created
    grid = create_grid(x_e, y_e)

    #   Find the internal elements
    e_internal = find_e_internal(x_e, y_e)

    #   Random element removal
    rem = rem_el(e_internal)
    grid = rem_el_grid(grid, x_e, rem)

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
    rem_l = list_to_str(rem, "_")

    #   Display the boundary conditions
    view_bc()

    #   Add the job
    add_job()

    #   Save the altered model
    save_model(rem_l)

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