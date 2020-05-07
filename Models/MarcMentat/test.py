##  Test program

#   Imports
import importlib

from evolve_soft_2d import classes, file_paths, log, utility
from evolve_soft_2d.classes import template
from evolve_soft_2d.unit import create, inspect, modify, rep_grid
from evolve_soft_2d.result import analyse, obtain

from py_mentat import py_connect, py_disconnect

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

    x_e = 5
    y_e = 5

    grid = rep_grid.create_grid(x_e, y_e)
    print(grid)

    rem = [7, 8, 13]

    grid_rem = rep_grid.rem_el_grid(template, rem)
    print(grid)
    print(grid_rem)

    return


main()