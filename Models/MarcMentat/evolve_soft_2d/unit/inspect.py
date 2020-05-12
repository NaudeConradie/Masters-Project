##  Functions used with the Marc Mentat units

#   Imports
from py_mentat import py_send

################################################################################

def find_e_internal(x_e, y_e) -> list:
    """Find all internal elements

    Parameters
    ----------
    x_e : int
        The number of elements in the x-direction
    y_e : int
        The number of elements in the y-direction

    Returns
    -------
    list
        The list of internal elements
    """

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

    return e_internal

################################################################################

def find_n_external(x_n, y_n) -> list:
    """Find all external nodes

    Parameters
    ----------
    x_n : int
        The number of nodes in the x-direction
    y_n : int
        The number of nodes in the y-direction

    Returns
    -------
    list
        The list of external nodes
    """

    #   Initialisations
    n_external = []

    #   Obtain the number of nodes
    n_n = x_n * y_n

    #   Loop through all nodes
    for i in range(1, n_n + 1):

        #   Check if the node is on the boundary
        if (i <= x_n) or (i > n_n - x_n) or (i % x_n == 0) or (i % x_n == 1):

            #   Add the node to the list of external nodes
            n_external.append(i)

    return n_external

################################################################################

def view_bc() -> None:
    """Display all boundary conditions
    """

    py_send("*identify_applys")
    py_send("*redraw")

    return