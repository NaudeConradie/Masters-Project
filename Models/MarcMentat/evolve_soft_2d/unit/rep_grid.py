##  Functions used with the representative grids

#   Imports
import numpy

from scipy.ndimage import measurements

from evolve_soft_2d.log import m_log
from evolve_soft_2d.unit import inspect

################################################################################

def create_grid(
    x: int,
    y: int,
    d: int,
    ) -> list:
    """Create a grid of digits

    Parameters
    ----------
    x : int
        The number of elements in the x-direction
    y : int
        The number of elements in the y-direction
    d : int
        The digit to create the grid of

    Returns
    -------
    list
        The representative grid
    """
    grid = [[d]*(x) for i in range(y)]

    if y == 1:

        grid = grid[0]

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
    template : template
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
    template : template
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
                grid_rem[template.x_e - (rem_i - 1)//template.x_e - 1, rem_i%template.x_e - 1] = 0

                #   Add the index of the element to the list of removed elements
                rem.append(rem_i)

            elif grid_label[template.x_e - i - 1][j] == 0:

                grid_rem[template.x_e - (rem_i - 1)//template.x_e - 1, rem_i%template.x_e - 1] = 0

            #   Increment the removed element counter
            rem_i = rem_i + 1

    return grid_rem, rem

################################################################################

def resize_grid(
    grid: list,
    x_b: int,
    y_b: int,
    ) -> list:
    """Resize a given 2D grid according to specified boundaries padded with zeroes and aligned to the bottom left

    Parameters
    ----------
    grid : list
        The grid to be resized
    x_b : int
        The x-boundary
    y_b : int
        The y-boundary

    Returns
    -------
    list
        The resized grid
    """    

    #   Initialisations
    x = len(grid[0])
    y = len(grid)
    grid_r = grid[:]

    #   Check if the grid's y-dimension is less than the y-boundary
    if y < y_b:

        #   Check if the grid's x-dimension is less than the x-boundary
        if x < x_b:

            #   Add the number of rows required
            grid_r = add_rows(grid_r, y_b, x, y)

            #   Add the number of columns required
            grid_r = add_cols(grid_r, x_b, x)

        #   Check if the grid's x-dimension is equal to the x-boundary
        elif x == x_b:

            #   Add the number of rows required
            grid_r = add_rows(grid_r, y_b, x, y)

        #   Check if the grid's x-dimension is greater than the x-boundary
        elif x > x_b:

            #   Add the number of rows required
            grid_r = add_rows(grid_r, y_b, x, y)

            #   Remove the number of columns required
            grid_r = rem_cols(grid_r, x_b, x)

    #   Check if the grid's y-dimension is equal to the y-boundary
    elif y == y_b:

        #   Check if the grid's x-dimension is less than the x-boundary
        if x < x_b:

            #   Add the number of columns required
            grid_r = add_cols(grid_r, x_b, x)

        #   Check if the grid's x-dimension is greater than the x-boundary
        elif x > x_b:

            #   Remove the number of columns required
            grid_r = rem_cols(grid_r, x_b, x)

    #   Check if the grid's y-dimension is greater than the y-boundary
    elif y > y_b:

        #   Check if the grid's x-dimension is less than the x-boundary
        if x < x_b:

            #   Remove the number of rows required
            grid_r = rem_rows(grid_r, y_b, y)

            #   Add the number of columns required
            grid_r = add_cols(grid_r, x_b, x)

        #   Check if the grid's x-dimension is equal to the x-boundary
        elif x == x_b:

            #   Remove the number of rows required
            grid_r = rem_rows(grid_r, y_b, y)

        #   Check if the grid's x-dimension is greater than the x-boundary
        elif x > x_b:

            #   Remove the number of rows required
            grid_r = rem_rows(grid_r, y_b, y)

            #   Remove the number of columns required
            grid_r = rem_cols(grid_r, x_b, x)

    return grid_r

################################################################################

def add_rows(
    grid: list,
    y_b: int,
    x: int,
    y: int,
    ) -> list:
    """Add rows of zeroes to a grid

    Parameters
    ----------
    grid : list
        The grid to which rows should be added
    y_b : int
        The y-boundary
    x : int
        The x-dimension of the grid
    y : int
        The y-dimension of the grid

    Returns
    -------
    list
        The grid with rows added
    """    

    #   Create a row of zeroes
    z = create_grid(x, 1, 0)

    #   Loop through the number of rows required to be added
    for _ in range(0, y_b - y):

        #   Copy the row of zeroes required to be added
        z_insert = z[:]

        #  Insert the row of zeroes at the start of the grid
        grid.insert(0, z_insert)  

    return grid

################################################################################

def add_cols(
    grid: list,
    x_b: int,
    x: int,
    ) -> list:
    """Add a column of zeroes to a grid

    Parameters
    ----------
    grid : list
        The grid to which columns should be added
    x_b : int
        The x-boundary
    x : int
        The x-dimension of the grid

    Returns
    -------
    list
        The grid with columns added
    """    

    #   Loop through the rows of the grid
    for i in grid:

        #   Loop through the number of columns required to be added
        for _ in range(0, x_b - x):

            #   Add a zero to the end of the row
            i.append(0)

    return grid

################################################################################

def rem_rows(
    grid: list,
    y_b: int,
    y: int,
    ) -> list:
    """Remove rows from a grid

    Parameters
    ----------
    grid : list
        The grid from which rows should be removed
    y_b : int
        The y-boundary
    y : int
        The y-dimension of the grid

    Returns
    -------
    list
        The grid with rows removed
    """    

    #   Loop through the number of rows to be removed
    for _ in range(0, y - y_b):

        #   Remove the first row from the grid
        grid.pop(0)

    return grid

################################################################################

def rem_cols(
    grid: list,
    x_b: int,
    x: int,
    ) -> list:
    """Remove rows from a grid

    Parameters
    ----------
    grid : list
        The grid from which columns should be removed
    x_b : int
        The x-boundary
    x : int
        The x-dimension of the grid

    Returns
    -------
    list
        The grid with columns removed
    """

    #   Loop through the rows of the grid
    for i in grid:

        #   Loop through the number of columns to be removed
        for _ in range(0, x - x_b):

            #   Remove the column at the end
            i.pop()

    return grid

################################################################################

def mirror_grid(
    grid: list,
    axis: str,
    ) -> list:

    grid_m = numpy.array(grid)

    if axis == "x":

        grid_m = numpy.flipud(grid_m)

    elif axis == "y":

        grid_m = numpy.fliplr(grid_m)

    elif axis == "d":

        #   Flip the grid across the vertical axis
        grid_m = numpy.fliplr(grid_m)

        #   Rotate the grid by 90 degrees anticlockwise
        grid_m = numpy.rot90(grid_m, 3)

    elif axis == "n":

        #   Flip the grid across the vertical axis
        grid_m = numpy.fliplr(grid_m)

        #   Rotate the grid by 90 degrees anticlockwise
        grid_m = numpy.rot90(grid_m)

    grid_m = grid_m.tolist()
    
    return grid_m

################################################################################

def mirror_neg_diag(
    grid: list,
    x_e: int,
    y_e: int,
    e_internal: list,
    ) -> list:
    """Mirror a grid across the negative diagonal

    Parameters
    ----------
    grid : list
        The grid to be mirrored
    x_e : int
        The x-dimension of the resulting grid
    y_e : int
        The y-dimension of the resulting grid
    e_internal: list
        The list of all internal elements

    Returns
    -------
    list
        The coordinates of the elements to be removed
    """    

    #   Resize the grid according to the required dimensions
    r = resize_grid(grid, x_e, y_e)

    #   Mirror the grid in the negative diagonal axis
    m = mirror_grid(r, "n")

    #   Convert the grids to numpy arrays
    r = numpy.array(r)
    m = numpy.array(m)

    #   Obtain the lower triangular grid including the diagonal
    l = numpy.tril(r)

    #   Obtain the upper triangular grid excluding the diagonal
    u = numpy.triu(m, 1)

    #   Add the lower and upper diagonal grids
    lu = l + u

    #   Convert the numpy array back to a list
    lu = lu.tolist()

    #   Obtain the element coordinates to be removed
    coord = inspect.find_e_coord(lu, e_internal)

    return coord

################################################################################

def rotate_neg_diag(
    grid: list,
    x_e: int,
    y_e: int,
    e_internal: list,
    ) -> list:
    """Rotate a grid across the negative diagonal

    Parameters
    ----------
    grid : list
        The grid to be mirrored
    x_e : int
        The x-dimension of the resulting grid
    y_e : int
        The y-dimension of the resulting grid
    e_internal: list
        The list of all internal elements

    Returns
    -------
    list
        The coordinates of the elements to be removed
    """    

    #   Resize the grid according to the required dimensions
    r = resize_grid(grid, x_e, y_e)

    #   Convert the grid to a numpy array
    r = numpy.array(r)

    #   Obtain the lower triangular grid including the diagonal
    l = numpy.tril(r)

    #   Rotate the grid by 90 degrees anticlockwise
    u = numpy.rot90(r, 2)

    #   Obtain the upper triangular grid excluding the diagonal
    u = numpy.triu(u, 1)

    #   Add the lower and upper diagonal grids
    lu = l + u

    #   Convert the numpy array back to a list
    lu = lu.tolist()

    #   Obtain the element coordinates to be removed
    coord = inspect.find_e_coord(lu, e_internal)

    return coord

################################################################################

def mirror_quarter(
    grid: list,
    x_e: int,
    y_e: int,
    e_internal: list,
    ) -> list:

    if x_e % 2 == 0:

        x = x_e/2

    else:

        x = x_e//2 + 1

    if y_e % 2 == 0:

        y = y_e/2 

    else:

        y = y_e//2 + 1

    bl = resize_grid(grid, x, y)

################################################################################