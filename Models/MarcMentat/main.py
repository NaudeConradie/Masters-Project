##  Main program

#   Imports
import importlib

from evolve_soft_2d import classes, file_paths, log, plotting, utility
from evolve_soft_2d.evolve import lsystems, cppns
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
    importlib.reload(lsystems)
    importlib.reload(cppns)
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
    x_e = 11
    y_e = 11
    #   The length of each side in mm
    x_s = 22
    y_s = 22
    #   The thickness of the unit boundary
    b = 2
    #   The number of increments per second to analyse
    n_steps = 20
    #   The text name of the table used for the applied displacement and load
    table_name = "ramp_input"
    #   The applied displacement and load
    app = [y_s/2, 0.02]
    #   The decision to add neighbouring grids
    neighbours = False

    #   L-system rule length
    l = 3

    #   CPPN parameters
    mod_n = 5
    hl_n = 10
    hl_s = 20
    scale = 1
    perc = 0.5
    c = [mod_n, hl_n, hl_s, scale, perc]

    #   Prepare the unit parameters
    temp = classes.template(case, x0, y0, x_e, y_e, x_s, y_s, b, classes.mold_star_15, n_steps, table_name, app, neighbours)

    #   Create the template
    if temp.case == 1:
        create.template_1(temp)
    elif temp.case == 2:
        create.template_2(temp)
    elif temp.case == 3:
        create.template_3(temp)
    elif temp.case == 4:
        create.template_4(temp)

    #   Generate a number of units and save their results
    fp_lu, fp_bu = create.gen_units(temp, 100, c = c)

    #   Analyse the results
    analyse.sel_best_u(temp, fp_lu, fp_bu, 50)

    #   Reanalyse the best units
    if temp.case == 1:
        create.template_1_test(fp_bu)
    elif temp.case == 2:
        create.template_2_test(fp_bu)

    #   View the boundary conditions of the template
    inspect.view_bc()

    return

if __name__ == "__main__":

    py_connect("", 40007)

    main()
    
    py_disconnect