##  Test program

#   Imports
import importlib
import re
import numpy
import pandas

from evolve_soft_2d import classes, file_paths, log, plotting, utility
from evolve_soft_2d.result import analyse, obtain
from evolve_soft_2d.unit import create, inspect, modify, rep_grid

from py_mentat import py_connect, py_disconnect

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
    #   Template case to be run
    case = 1
    #   Coordinates of initial position
    x0 = 0
    y0 = 0
    #   Number of nodes per axis (one more than number of elements desired)
    x_e = 5
    y_e = 5

    x_s = 20
    y_s = 20

    b = 1
    #   Number of increments per second to analyse
    n_steps = 4
    #   Text name of the table used for the applied load
    table_name = "ramp_input"
    #   Magnitude of the applied load and/or displacement
    #   p_mag = 25
    app = [y_s/2, 10]

    

    return

main()