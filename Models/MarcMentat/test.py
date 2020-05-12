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

    l = ['4.138759275223428995e+04', '2.704693719776506769e+05', '2.322056518865353428e+04', '3.101738482855314032e+03', '5.231738590075147840e+03', '2.315872224098487095e+03', '3.293072541513819597e+05', '2.050347791724815124e+03', '2.206723698873520334e+03', '6.929513897731169891e+03', '1.624649734903174394e+05', '1.138009162894073233e+04', '', '1.228096906493830465e+04', '5.514394529612689439e+03']

    (l_o, l_f) = utility.list_to_float(l)

    print(l_o)
    print(l_f)

    return


main()