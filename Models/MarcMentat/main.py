##  Main program

#   Imports
import importlib

from evolve_soft_2d import classes, file_paths, log, utility
from evolve_soft_2d.classes import mat, template
from evolve_soft_2d.model import create, inspect, modify, rep_grid
from evolve_soft_2d.result import analyse, obtain

from py_mentat import py_connect, py_disconnect

################################################################################

#   Main function

def main():

    #   Reload the modules
    importlib.reload(classes)
    importlib.reload(file_paths)
    importlib.reload(utility)
    importlib.reload(create)
    importlib.reload(inspect)
    importlib.reload(modify)
    importlib.reload(rep_grid)
    importlib.reload(analyse)
    importlib.reload(obtain)

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
    #   Template case to be run
    case = 0

    #   Prepare the model parameters
    temp = template(case, x0, y0, x_n, y_n, n_steps, table_name, d_mag)

    #   Flag to be set if the base model needs to be regenerated
    regen_base = False

    #   Check if the template exists
    exists = utility.if_file_exist(temp.fp_t_f)

    #   Open the base file if it exists
    if exists and not regen_base:
        modify.open_model(temp.fp_t_f, str(temp.case) + "_" + temp.n_e_l)

    #   Create the base file if it does not exist
    elif temp.case == 0:
        create.template_0(temp)

    #   Generate a number of models and save their results
    t = create.gen_models(temp, 3)

    #   View the boundary conditions of the template
    inspect.view_bc()

    return

if __name__ == "__main__":

    py_connect("", 40007)

    main()
    
    py_disconnect