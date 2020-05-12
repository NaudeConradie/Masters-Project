##  Functions used for obtaining and inspecting results

#   Imports
from evolve_soft_2d import utility
from evolve_soft_2d.file_paths import create_fp_r_f, create_fp_r_f_da

import linecache
import numpy
import matplotlib.pyplot as plot

################################################################################

def monte_carlo(template, fp_u_m) -> None:
    """Monte Carlo analysis

    Parameters
    ----------
    template : class
        The unit template parameters
    fp_u_m : str
        The file path of the log file of units created during the last simulation
    """

    #   Initialisations
    b_e = []

    #   Read the list of units created during the last simulation
    with open(fp_u_m) as f:
        unit_l = f.readlines()
    unit_l = [i.rstrip() for i in unit_l]

    #   Loop through the list of units
    for i in range(0, len(unit_l)):
        b_e.append([])

        #   Create the file path for the current unit
        fp_r_f = create_fp_r_f_da(template, "Boundary Energy", unit_l[i])

        #   Add the current unit's boundary energy at the final stage of the simulation
        b_e[i] = linecache.getline(fp_r_f, template.n_steps + 1)

    #   Prepare the boundary energy for analysis
    b_e = [i.rstrip() for i in b_e]
    (b_e, b_e_f) = utility.list_to_float(b_e)

    #   Plot the results
    plot.hist(b_e, bins = 20)
    plot.show()

    return

################################################################################

def boundary_energy(unit) -> None:
    """Calculate the boundary energy for a unit

    Parameters
    ----------
    unit : class
        The unit parameters
    """

    #   The labels of the required results
    label = []
    label.append("Displacement")
    label.append("Reaction Force")

    #   Loop through all the labels
    for i in range(0, len(label)):

        #   Create the file path of the results file
        fp_r_f = create_fp_r_f(unit, label[i])

        #   Determine which variable to store the results in
        if i == 0:

            #   Store the results from the results file in the correct variable
            d = numpy.genfromtxt(fp_r_f, delimiter = ",")

        elif i == 1:

            #   Store the results from the results file in the correct variable
            r = numpy.genfromtxt(fp_r_f, delimiter = ",")

    #   Decrement the node IDs of the external nodes by 1 to be used as array indices
    n_external_i = [i - 1 for i in unit.template.n_external]

    #   Store only the external node values
    d_ex_mm = d[:, n_external_i]
    r_ex = r[:, n_external_i]

    #   Convert from mm to m
    d_ex = d_ex_mm*1000

    #   Initialise the boundary energy array
    b_e = numpy.zeros(len(d_ex))

    #   Loop through every step in the unit
    for i in range(0, len(d_ex)):

        #   Loop through every external node
        for j in range(0, len(d_ex[0])):

            #   Calculate the boundary energy for the current step
            b_e[i] = b_e[i] + d_ex[i, j]*r_ex[i, j]

    #   Save the boundary energies to a .csv file
    save_numpy_array_to_csv(unit, "Boundary Energy", b_e)

    return

################################################################################

def save_numpy_array_to_csv(unit, t, data) -> None:
    """Write the results to .csv files

    Parameters
    ----------
    unit : class
        The unit parameters
    t : str
        The type of data to be stored
    data : numpy.array
        The results to be stored
    """
    #   Create the file path of the results file
    fp_r_csv = create_fp_r_f(unit, t)

    #   Write the data to the results file
    numpy.savetxt(fp_r_csv, data, delimiter = ",")

    print("{}_{}.csv saved".format(t, unit.u_id))

    return