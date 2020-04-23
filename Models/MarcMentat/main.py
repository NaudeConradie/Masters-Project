##  Main program

#   Imports
from evolve_soft_2d import result, utility
from evolve_soft_2d.model import create, inspect, modify, rep_grid

from py_mentat import py_connect, py_disconnect

################################################################################

#   Main function

def main():

    #   Initialisations
    #   Text name of the table used for the applied load
    table_name = "sin_input"
    #   Number of nodes per axis (one more than number of elements desired)
    x_n = 6
    y_n = 6
    #   Coordinates of initial position
    x0 = 0
    y0 = 0
    #   Number of increments per second to analyse
    n_steps = 4
    #   Magnitude of the applied load and/or displacement
    #   p_mag = 25
    d_mag = 1

    #   Flag to be set if the base model needs to be regenerated
    regen_base = False

    #   Template case to be run
    case = "0"

    #   Prepare the model parameters
    (n_n, x_e, y_e, n_e_l, fp_t_f, exists) = create.prep_template(x_n, y_n, case)

    #   Open the base file if it exists
    if exists and not regen_base:
        modify.open_model(fp_t_f, n_e_l + '_' + case)

    #   Create the base file if it does not exist
    elif case == "0":
        create.template_0(x0, y0, x_n, y_n, y_e, table_name, d_mag, n_steps, n_e_l, fp_t_f)

    #   Create a representative grid of ones
    grid = rep_grid.create_grid(x_e, y_e)

    #   Find all internal elements
    e_internal = inspect.find_e_internal(x_e, y_e)

    #   Generate a number of models and save their results
    create.gen_models(n_n, x_e, y_e, e_internal, n_steps, grid, n_e_l, case, fp_t_f, 5)

    #   View the boundary conditions of the template
    inspect.view_bc()

    return

if __name__ == '__main__':

    py_connect("", 40007)

    main()
    
    py_disconnect