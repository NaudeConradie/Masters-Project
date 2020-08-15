##  Functions used with the Marc Mentat units

#   Imports
from evolve_soft_2d import utility

from py_mentat import py_send, py_get_float

################################################################################

def find_e_internal(
    x_e: int,
    y_e: int,
    b: int,
    ) -> list:
    """Find all internal elements

    Parameters
    ----------
    x_e : int
        The number of elements in the x-direction
    y_e : int
        The number of elements in the y-direction
    b : int
        The boundary thickness

    Returns
    -------
    list
        The list of internal elements
    """

    #   Initialisations
    e_internal = []

    #   Determine the maximum boundary thickness
    b_max = max_b(x_e, y_e)

    #   Set the boundary thickness to within limits if it exceeds any
    b = utility.clean_int(b, b_max)

    #   Obtain the number of elements
    e_n = x_e * y_e

    #   Define a list of all elements
    e = [*range(1, e_n + 1)]

    #   Add the first and last rows of elements to the list of external elements
    e_external = [*range(1, x_e*b + 1)]
    e_external += [*range(e_n - x_e*b + 1, e_n + 1)]

    #   Loop through the internal rows of the elements
    for i in range(1, y_e - 2*b + 1):

        #   Loop through the number of boundary elements
        for j in range(1, b + 1):

            #   Add the left column elements to the list of external elements
            e_external.append((i + b - 1)*x_e + j)

            #   Add the right column elements to the list of external elements
            e_external.append((i + b)*x_e - j + 1)

    #   Determine the list of internal elements
    e_internal = utility.unique_list(e, e_external)

    #   Sort the list of internal elements
    e_internal.sort()

    return e_internal

################################################################################

def find_n_external(
    x_n: int,
    y_n:int,
    ) -> list:
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

def find_n_coord(n: list) -> [list, list]:
    """Find the coordinates of a list of nodes

    Parameters
    ----------
    n : list
        The list of nodes

    Returns
    -------
    [list, list]
        The x and y coordinates
    """

    x = []
    y = []

    for i in n:

        x.append(py_get_float("node_x({})".format(i)))
        y.append(py_get_float("node_y({})".format(i)))
        
    return x, y

################################################################################

def max_b(
    x_e: int,
    y_e: int,
    ) -> int:
    """Find the maximum boundary thickness

    Parameters
    ----------
    x_e : int
        The number of elements in the x-direction
    y_e : int
        The number of elements in the y-direction

    Returns
    -------
    int
        The maximum boundary thickness
    """

    #   Determine the shortest side of the unit
    min_s = min(x_e, y_e)

    #   Check if the shortest side has an odd number of elements
    if min_s % 2 == 1:

        #   Set the maximum boundary thickness
        b_max = min_s/2 - 0.5

    #   Check if the shortest side has an even number of elements
    else:

        #   Set the maximum boundary thickness
        b_max = min_s/2 - 1

    return b_max

################################################################################

def view_bc() -> None:
    """Display all boundary conditions
    """

    py_send("*identify_applys")
    py_send("*redraw")

    return