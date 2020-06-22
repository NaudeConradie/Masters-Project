##  Main program

#   Imports
import importlib

from evolve_soft_2d import classes, file_paths, log, plotting, utility
from evolve_soft_2d.result import analyse, obtain
from evolve_soft_2d.unit import create, inspect, modify, rep_grid

from py_mentat import py_connect, py_disconnect

################################################################################

#   Main function

def main():

    #   Reload the modules
    importlib.reload(classes)
    importlib.reload(file_paths)
    importlib.reload(plotting)
    importlib.reload(utility)
    importlib.reload(analyse)
    importlib.reload(obtain)
    importlib.reload(create)
    importlib.reload(inspect)
    importlib.reload(modify)
    importlib.reload(rep_grid)

    #   Initialisations
    #   The template case identifier
    case = 1
    #   The initial coordinates
    x0 = 0
    y0 = 0
    #   The number of elements in each axis direction
    x_e = 5
    y_e = 5
    #   The length of each side in mm
    x_s = 20
    y_s = 20
    #   The thickness of the unit boundary
    b = 1
    #   The number of increments per second to analyse
    n_steps = 4
    #   The text name of the table used for the applied displacement and load
    table_name = "ramp_input"
    #   The applied displacement and load
    app = [y_s/2, 0.01]

    #   Prepare the unit parameters
    temp = classes.template(case, x0, y0, x_e, y_e, x_s, y_s, b, classes.mold_star_15, n_steps, table_name, app)

    #   Create the template
    if temp.case == 1:
        create.template_1(temp)
    elif temp.case == 2:
        create.template_2(temp)

    # #   Generate a number of units and save their results
    # fp_lu, fp_bu = create.gen_units(temp, 1)

    # #   Analyse the results
    # analyse.sel_best_u(temp, fp_lu, fp_bu, 1)

    # #   Reanalyse the best units
    # if temp.case == 1:
    #     create.template_1_test(fp_bu)

    create.neighbours(temp)

    #   View the boundary conditions of the template
    inspect.view_bc()

    return

if __name__ == "__main__":

    py_connect("", 40007)

    main()
    
    py_disconnect