##  Test program

#   Used to quickly test changes to functions with an existing case open

#   Imports

from py_mentat import *
from py_post import *

from functions import *

################################################################################

#   Main function

def main():

    #   Initialisations
    #   Text name of the table used for the applied load
    table_name = "sin_input"
    #   Number of nodes per axis (one more than number of elements desired)
    x_n = 6
    y_n = 6
    x_e = x_n - 1
    y_e = y_n - 1
    #   Coordinates of initial position
    x0 = 0
    y0 = 0
    #   Number of increments per second to analyse
    n_steps = 20
    #   Magnitude of the applied load
    p_mag = 25

    #   !   CHANGE EVERY TIME MAIN IS RERUN   !   #
    rem = 19
    
    grid = create_grid(x_e, y_e)

    grid = rem_el_grid(grid, x_e, rem)

    print(grid)
    
    res_val(rem, n_steps)

    return

if __name__ == '__main__':

    py_connect("", 40007)

    main()
    
    py_disconnect