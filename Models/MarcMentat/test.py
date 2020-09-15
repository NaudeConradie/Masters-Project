##  Test program

#   Imports
import importlib
import re
import numpy
import pandas

from evolve_soft_2d import classes, file_paths, log, plotting, utility
from evolve_soft_2d.evolve import cppns, lsystems
from evolve_soft_2d.result import analyse, obtain
from evolve_soft_2d.unit import create, inspect, modify, rep_grid

from py_mentat import py_connect, py_disconnect

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
    x_e = 15
    y_e = 15
    #   The length of each side in mm
    x_s = 30
    y_s = 30
    #   The thickness of the unit boundary
    b = 3
    #   The number of increments per second to analyse
    n_steps = 5
    #   The text name of the table used for the applied displacement and load
    table_name = "ramp_input"
    #   The applied displacement and load
    app = [y_s/2, 0.02]
    #   The decision to add neighbouring grids
    neighbours = False

    #   L-system parameters
    l_max = [8, 3, 6, 6]
    l_min = [0, 1, 2, 1]

#   CPPN parameters
    c_max = [6, 11, 33, 11, 101, 96]
    c_min = [1, 2, 5, 1, 1, 10]

    #   Prepare the unit parameters
    temp = classes.template(case, x0, y0, x_e, y_e, x_s, y_s, b, classes.mold_star_15, n_steps, table_name, app, neighbours)

    create.template_1(temp)

    pop_i = create.gen_units(temp, 3, l = [l_max, l_min])

    fp_lu, fp_bu = create.run_units(temp, pop_i, "l")

    analyse.sel_best_u(temp, fp_lu, fp_bu, 2)

    return

# main()