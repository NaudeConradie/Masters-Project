##  Test program

#   Imports

##  Main program

#   Imports

from model_functions import *
from result_functions import *
from rep_grid_functions import *
from utility_functions import *
from file_paths import fp

################################################################################

#   Main function

def main():

    #   Initialisations
    
    #   Text name of the table used for the applied load
    table_name = "sin_input"

    #   Number of nodes per axis (one more than number of elements desired)
    x_n = 6
    y_n = 6

    #   Number of elements per axis
    x_e = x_n - 1
    y_e = y_n - 1
    n_e = [x_e, y_e]
    n_e_l = list_to_str(n_e, "x")

    #   Coordinates of initial position
    x0 = 0
    y0 = 0

    #   Number of increments per second to analyse
    n_steps = 20

    #   Magnitude of the applied load and/or displacement
    #   p_mag = 25
    d_mag = 1

    py_send(r'*change_directory %s' % fp)

    create_base_model(x0, y0, x_n, y_n, x_e, y_e, table_name, d_mag, n_steps, n_e_l)

    return

