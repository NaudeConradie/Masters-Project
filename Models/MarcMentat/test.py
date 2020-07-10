##  Test program

#   Imports
import importlib
import re
import numpy
import pandas

from evolve_soft_2d import classes, file_paths, log, plotting, utility
from evolve_soft_2d.evolve import lsystems
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
    x_e = 10
    y_e = 10
    #   The length of each side in mm
    x_s = 20
    y_s = 20
    #   The thickness of the unit boundary
    b = 2
    #   The number of increments per second to analyse
    n_steps = 5
    #   The text name of the table used for the applied displacement and load
    table_name = "ramp_input"
    #   The applied displacement and load
    app = [y_s/2, 0.025]
    #   The decision to add neighbouring grids
    neighbours = False

    #   Prepare the unit parameters
    temp = classes.template(case, x0, y0, x_e, y_e, x_s, y_s, b, classes.mold_star_15, n_steps, table_name, app, neighbours)
    
    v = lsystems.e_vocabulary

    g = [["F", "fF"]]

    a = lsystems.a_rot_dia_ndi

    n = 2

    l = lsystems.lsystem(v, g, a, n)

    print(l)

    e = lsystems.interpret_word(l.word)

    for i in e:
        
        print(i)

    return

main()