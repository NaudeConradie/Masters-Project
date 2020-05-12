##  Main program

#   Imports
import importlib

from evolve_soft_2d import classes, file_paths, log, utility
from evolve_soft_2d.classes import template, mold_star_15
from evolve_soft_2d.result import analyse, obtain
from evolve_soft_2d.unit import create, inspect, modify, rep_grid

from py_mentat import py_connect, py_disconnect

################################################################################

#   Main function

def main():

    #   Reload the modules
    importlib.reload(classes)
    importlib.reload(file_paths)
    importlib.reload(utility)
    importlib.reload(analyse)
    importlib.reload(obtain)
    importlib.reload(create)
    importlib.reload(inspect)
    importlib.reload(modify)
    importlib.reload(rep_grid)

    #   Initialisations
    #   Text name of the table used for the applied load
    table_name = "ramp_input"
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
    d_mag = (y_n - 1)/2
    #   Template case to be run
    case = 2

    #   Prepare the unit parameters
    temp = template(case, x0, y0, x_n, y_n, mold_star_15, n_steps, table_name, d_mag)

    #   Flag to be set if the base unit needs to be regenerated
    regen_base = True

    #   Check if the template exists
    exists = utility.if_file_exist(temp.fp_t_f)

    #   Open the base file if it exists
    if exists and not regen_base:
        modify.open_model(temp.fp_t_f)

    #   Create the base file if it does not exist
    elif temp.case == 0:
        create.template_0(temp)
    elif temp.case == 1:
        create.template_1(temp)
    elif temp.case == 2:
        create.template_2(temp)

    #   Generate a number of units and save their results
    fp_u_m = create.gen_units(temp, 1)

    #   Analyse the results
    analyse.monte_carlo(temp, fp_u_m)

    #   View the boundary conditions of the template
    inspect.view_bc()

    return

if __name__ == "__main__":

    py_connect("", 40007)

    main()
    
    py_disconnect