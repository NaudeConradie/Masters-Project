##  Test program

#   Imports
import importlib

from evolve_soft_2d import classes, file_paths, log, utility
from evolve_soft_2d.classes import template, mold_star_15
from evolve_soft_2d.result import analyse, obtain
from evolve_soft_2d.unit import create, inspect, modify, rep_grid

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
    case = 1

    temp = template(case, x0, y0, x_n, y_n, mold_star_15, n_steps, table_name, d_mag)

    fp_lu = file_paths.create_fp_file(temp, "_2020-05-19--15-14-11", "l")

    analyse.monte_carlo(temp, fp_lu)

    return

main()