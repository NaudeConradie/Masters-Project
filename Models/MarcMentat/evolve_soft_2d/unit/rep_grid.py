##  Functions used with the representative grids

#   Imports
import numpy

from scipy.ndimage import measurements

from evolve_soft_2d.log import m_log

################################################################################

def create_grid(
    x_e: int,
    y_e: int,
    ) -> list:
    """Create a grid of ones representative of the unit

    Parameters
    ----------
    x_e : int
        The number of elements in the x-direction
    y_e : int
        The number of elements in the y-direction

    Returns
    -------
    list
        The representative grid
    """
    grid = [[1]*(x_e) for i in range(y_e)]

    return grid
 
################################################################################

def find_cluster(grid: list) -> [bool, list]:
    """Find all clusters of elements using the representative grid

    Parameters
    ----------
    grid : list
        The representative grid of ones

    Returns
    -------
    [bool, list]
        True if free clusters were found, false otherwise
        The grid with clusters incrementally labelled
    """

    grid_label, cluster = measurements.label(grid)

    #   Check if more than one cluster is found
    if cluster > 1:

        #   Set flag
        found = True

        if cluster == 2:
            m_log.warning("{} free element cluster found!".format(cluster - 1))
        else:
            m_log.warning("{} free element clusters found!".format(cluster - 1))

    else:

        #   Set flag
        found = False

    return found, grid_label

################################################################################

def rem_el_grid(
    template,
    rem: list,
    ) -> numpy.array:
    """Removes elements from the representative grid

    Parameters
    ----------
    template : class
        The unit template parameters
    rem : list
        The element IDs of the elements to be removed

    Returns
    -------
    numpy.array
        The grid with zeros in the places of the removed elements
    """

    #   Initialisations
    grid_rem = numpy.array(template.grid)

    #   Loop through the number of elements to be removed
    for i in range(0, len(rem)):

        #   Remove the element from the grid
        grid_rem[template.x_e - (rem[i] - 1)//template.x_e - 1][rem[i]%template.x_e - 1] = 0

    return grid_rem

################################################################################

def rem_el_free_grid(
    template,
    grid_label: list,
    ) -> [numpy.array, list]:
    """Remove free element clusters from the representative grid

    Parameters
    ----------
    template : class
        The unit template parameters
    grid_label : list
        Representative grid with clusters incrementally labelled

    Returns
    -------
    [numpy.array, list]
        The grid with zeros in place of the removed elements
        The list of removed elements
    """
    #   Initialisations
    rem_i = 1
    rem = []

    grid_rem = numpy.array(template.grid)

    #   Loop through the elements in the x-direction
    for i in range(0, template.x_e):

        #   Loop through the elements in the y-direction
        for j in range(0, template.y_e):

            #   Check if the labelled grid has an element numbered greater than 1
            if grid_label[template.x_e - i - 1][j] > 1:

                #   Remove the element from the grid
                grid_rem[template.x_e - (rem_i - 1)//template.x_e - 1][rem_i%template.x_e - 1] = 0

                #   Add the index of the element to the list of removed elements
                rem.append(rem_i)

            #   Increment the removed element counter
            rem_i = rem_i + 1

    return (grid_rem, rem)