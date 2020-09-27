##  Test program

#   Imports
import importlib
import re
import numpy
import pandas

from evolve_soft_2d import classes, file_paths, log, plotting, utility
from evolve_soft_2d.evolve import cppns, gen_alg, lsystems
from evolve_soft_2d.result import analyse, obtain
from evolve_soft_2d.unit import create, inspect, modify, rep_grid

from py_mentat import py_connect, py_disconnect

def main():

    #   Reload the modules
    importlib.reload(classes)
    importlib.reload(file_paths)
    importlib.reload(plotting)
    importlib.reload(utility)
    importlib.reload(cppns)
    importlib.reload(gen_alg)
    importlib.reload(lsystems)
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
    e_s = 2
    #   The thickness of the unit boundary
    b = 2
    #   The number of increments per second to analyse
    n_steps = 5
    #   The text name of the table used for the applied displacement and load
    table_name = "ramp_input"
    #   The applied displacement and load
    app = [y_e*e_s/2, 0.025]
    #   The decision to add neighbouring grids
    neighbours = False

    meth = "r"

    #   Prepare the unit parameters
    temp = classes.template(case, x0, y0, x_e, y_e, e_s, b, classes.mold_star_15, n_steps, table_name, app, neighbours)

    # create.temp_create(temp)

    t = "_2020-09-27--10-40-13"

    fp_lu = file_paths.create_fp_file(temp, t, "l")
    fp_lu_rank = file_paths.create_fp_file(temp, t + "_ranked", "l")

    analyse.rank_u(temp, fp_lu, fp_lu_rank)

    return

main()