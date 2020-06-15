##  Functions used with the Marc Mentat units

#   Imports
from py_mentat import py_send

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
    e_internal = list((set(e) | set(e_external)) - (set(e) & set(e_external)))

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

def view_bc() -> None:
    """Display all boundary conditions
    """

    py_send("*identify_applys")
    py_send("*redraw")

    return