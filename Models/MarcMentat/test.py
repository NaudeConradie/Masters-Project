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
    x_n = 11
    y_n = 11
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
    
    grid = create_grid(x_e, y_e)

    rem = 82
    grid = rem_el_grid(grid, x_e, rem)
    rem = 83
    grid = rem_el_grid(grid, x_e, rem)
    rem = 84
    grid = rem_el_grid(grid, x_e, rem)
    rem = 85
    grid = rem_el_grid(grid, x_e, rem)
    rem = 86
    grid = rem_el_grid(grid, x_e, rem)
    rem = 87
    grid = rem_el_grid(grid, x_e, rem)
    rem = 88
    grid = rem_el_grid(grid, x_e, rem)
    rem = 89
    grid = rem_el_grid(grid, x_e, rem)
    rem = 72
    grid = rem_el_grid(grid, x_e, rem)
    rem = 74
    grid = rem_el_grid(grid, x_e, rem)
    rem = 77
    grid = rem_el_grid(grid, x_e, rem)
    rem = 79
    grid = rem_el_grid(grid, x_e, rem)
    rem = 62
    grid = rem_el_grid(grid, x_e, rem)
    rem = 64
    grid = rem_el_grid(grid, x_e, rem)
    rem = 67
    grid = rem_el_grid(grid, x_e, rem)
    rem = 68
    grid = rem_el_grid(grid, x_e, rem)
    rem = 69
    grid = rem_el_grid(grid, x_e, rem)
    rem = 52
    grid = rem_el_grid(grid, x_e, rem)
    rem = 53
    grid = rem_el_grid(grid, x_e, rem)
    rem = 54
    grid = rem_el_grid(grid, x_e, rem)
    rem = 57
    grid = rem_el_grid(grid, x_e, rem)
    rem = 59
    grid = rem_el_grid(grid, x_e, rem)
    rem = 42
    grid = rem_el_grid(grid, x_e, rem)
    rem = 43
    grid = rem_el_grid(grid, x_e, rem)
    rem = 45
    grid = rem_el_grid(grid, x_e, rem)
    rem = 46
    grid = rem_el_grid(grid, x_e, rem)
    rem = 47
    grid = rem_el_grid(grid, x_e, rem)
    rem = 48
    grid = rem_el_grid(grid, x_e, rem)
    rem = 49
    grid = rem_el_grid(grid, x_e, rem)
    
    find_cluster(grid)

    return

if __name__ == '__main__':

    py_connect("", 40007)

    main()
    
    py_disconnect