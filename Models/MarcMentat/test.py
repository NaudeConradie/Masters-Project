##  Test program

#   Imports
from evolve_soft_2d.model import create, inspect
from evolve_soft_2d.result import analyse
from evolve_soft_2d import utility, file_paths

import math

def main():
    #   Initialisations
    #   Text name of the table used for the applied load
    table_name = "sin_input"
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
    d_mag = 1

    #   Template case to be run
    case = "0"

    (n_n, x_e, y_e, n_e_l, e_internal, n_external, fp_t_f, exists) = create.prep_template(x_n, y_n, case)

    m_id = "2a853a7cdfd80d15c74683cfa4136769"

    n_e_l = utility.list_to_str([x_e, y_e], "x")

    b_e = analyse.boundary_energy(n_e_l, case, m_id, n_external)

    print(b_e)

    return

main()