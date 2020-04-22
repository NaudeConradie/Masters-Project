##  Functions used with the representative grids

#   Imports

from evolve_soft_2d.log import m_log

from scipy.ndimage import measurements

################################################################################

#   Create a grid of ones representative of the model
#   Returns the representative grid

#   x_e: The number of elements in the x-direction
#   y_e: The number of elements in the y-direction
def create_grid(x_e, y_e):

    grid = [[1]*(x_e) for i in range(y_e)]

    return grid
 
################################################################################

#   Find all clusters of elements using the representative grid
#   Returns a grid with clusters incrementally labelled

#   grid:   Representative grid of ones
def find_cluster(grid):

    grid_label, cluster = measurements.label(grid)

    #   Check if more than one cluster is found
    if cluster > 1:

        #   Set flag
        found = True

        if cluster == 2:
            m_log.warning("%i free element cluster found!" % (cluster - 1))
        else:
            m_log.warning("%i free element clusters found!" % (cluster - 1))

    else:

        #   Set flag
        found = False

        m_log.info("No free element clusters found")

    return (found, grid_label)

################################################################################

#   Removes elements from the representative grid
#   Returns the grid with a zero in the place of the removed element

#   grid:   Representative grid of ones
#   x_e:    The number of elements in the x-direction
#   rem:    The element IDs of the elements to be removed
def rem_el_grid(grid, x_e, rem):

    #   Loop through the number of elements to be removed
    for i in range(0, len(rem)):

        #   Remove the element from the grid
        grid[x_e - (rem[i] - 1)//x_e - 1][rem[i]%x_e - 1] = 0

    return grid

################################################################################

#   Remove free element clusters from the representative grid
#   Returns the grid with zeros in place of the removed elements and a list of the removed elements

#   grid:       Representative grid of ones
#   grid_label: Representative grid with clusters incrementally labelled
#   x_e:        The number of elements in the x-direction
#   y_e:        The number of elements in the y-direction
def rem_el_free_grid(grid, grid_label, x_e, y_e):

    #   Initialisations
    rem_i = 1
    rem = []

    #   Loop through the elements in the x-direction
    for i in range(0, x_e):

        #   Loop through the elements in the y-direction
        for j in range(0, y_e):

            #   Check if the labelled grid has an element numbered greater than 1
            if grid_label[x_e - i - 1][j] > 1:

                #   Remove the element from the grid
                grid[x_e - (rem_i - 1)//x_e - 1][rem_i%x_e - 1] = 0

                #   Add the index of the element to the list of removed elements
                rem.append(rem_i)

            #   Increment the removed element counter
            rem_i = rem_i + 1

    return (grid, rem)