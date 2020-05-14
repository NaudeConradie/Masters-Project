##  Functions used for obtaining and inspecting results

#   Imports
import linecache
import numpy
import matplotlib.pyplot as plot

from evolve_soft_2d import utility
from evolve_soft_2d.file_paths import create_fp_file

################################################################################

def monte_carlo(template, fp_lu) -> None:
    """Monte Carlo analysis

    Parameters
    ----------
    template : class
        The unit template parameters
    fp_u_m : str
        The file path of the log file of units created during the last simulation
    """

    #   Initialisations
    c_e = []

    #   Read the list of units created during the last simulation
    with open(fp_lu) as f:
        unit_l = f.readlines()
    unit_l = [i.rstrip() for i in unit_l]

    #   Loop through the list of units
    for i in range(0, len(unit_l)):
        c_e.append([])

        #   Create the file path for the current unit
        fp_r_f = create_fp_file(template, "Constraint Energy_" + unit_l[i], "r")

        #   Add the current unit's constraint energy at the final stage of the simulation
        c_e[i] = linecache.getline(fp_r_f, template.n_steps + 1)

    #   Prepare the constraint energy for analysis
    c_e = [i.rstrip() for i in c_e]
    (c_e, c_e_f) = utility.list_to_float(c_e)

    #   Plot the results
    plot.hist(c_e, bins = 20)
    plot.show()

    return

################################################################################

def constraint_energy(template, l) -> None:
    """Calculate the constraint energy for a unit

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
        fp_r_f = create_fp_file(template, label[i] + "_" + l, "r")

        #   Determine which variable to store the results in
        if i == 0:

            #   Store the results from the results file in the correct variable
            d = numpy.genfromtxt(fp_r_f, delimiter = ",")

        elif i == 1:

            #   Store the results from the results file in the correct variable
            r = numpy.genfromtxt(fp_r_f, delimiter = ",")

    #   Decrement the node IDs of the external nodes by 1 to be used as array indices
    n_external_i = [i - 1 for i in template.n_external]

    #   Store only the external node values
    d_ex_mm = d[:, n_external_i]
    r_ex = r[:, n_external_i]

    #   Convert from mm to m
    d_ex = d_ex_mm*1000

    #   Initialise the constraint energy array
    c_e = numpy.zeros(len(d_ex))

    #   Loop through every step in the unit
    for i in range(0, len(d_ex)):

        #   Loop through every external node
        for j in range(0, len(d_ex[0])):

            #   Calculate the constraint energy for the current step
            c_e[i] = c_e[i] + d_ex[i, j]*r_ex[i, j]

    #   Save the boundary energies to a .csv file
    save_numpy_array_to_csv(template, "Constraint Energy_" + l, c_e)

    return

################################################################################

def save_numpy_array_to_csv(template, l, data) -> None:
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
    fp_r_f = create_fp_file(template, l, "r")

    #   Write the data to the results file
    numpy.savetxt(fp_r_f, data, delimiter = ",")

    print("{}.csv saved".format(l))

    return