##  Main program

#   Imports

from py_mentat import *
from py_post import *

from functions import *

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

    #   Number of increments in the second
    n_steps = 20

    #   Magnitude of the sinusoidal pressure load
    p_mag = 25

    #   Grid construction
    create_nodes(x0, y0, x_n, y_n)

    create_elements(x_n, y_n)

    add_sin(table_name)

    add_bc_fixed(x0, y0, x_n, y_n)

    add_load(table_name, p_mag)

    add_geom_prop()

    add_mat_mr()

    add_lcase(n_steps)

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

    view_bc()

    save_rem_model(rem)

    add_job(rem)

    run_job()

    check_t16(rem)

    #res_gif(rem)

    res_val(rem, n_steps)

    return

if __name__ == '__main__':

    py_connect("", 40007)

    main()
    
    py_disconnect

