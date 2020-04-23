##  Functions used with the Marc Mentat models

#   Imports
from evolve_soft_2d.log import m_log

from py_mentat import py_send

################################################################################

#   Find all internal elements
#   Returns a list of internal elements

#   x_e: The number of elements in the x-direction
#   y_e: The number of elements in the y-direction
def find_e_internal(x_e, y_e):

    #   Initialisations
    e_internal = []

    #   Obtain the number of elements
    e_n = x_e * y_e

    #   Loop through all elements
    for i in range(1, e_n + 1):

        #   Check if element is not on the boundary
        if (i > x_e) and (i <= e_n - x_e) and (i % x_e != 0) and (i % x_e != 1):

            #   Add element to the list of internal elements
            e_internal.append(i)

    m_log.info("%i internal elements found" % len(e_internal))

    return e_internal

################################################################################

#   Find all external nodes
#   Returns a list of external nodes

#   x_n: The number of nodes in the x-direction
#   y_n: The number of nodes in the y-direction
def find_n_external(x_n, y_n, n_n):

    #   Initialisations
    n_external = []

    #   Loop through all nodes
    for i in range(1, n_n + 1):

        #   Check if the node is on the boundary
        if (i <= x_n) or (i > n_n - x_n) or (i % x_n == 0) or (i % x_n == 1):

            #   Add the node to the list of external nodes
            n_external.append(i)

    m_log.info("%i external nodes found" % len(n_external))

    return n_external

################################################################################

#   Display all boundary conditions

def view_bc():

    py_send("*identify_applys")
    py_send("*redraw")

    return