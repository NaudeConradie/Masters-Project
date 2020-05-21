##  Functions used for obtaining and inspecting results

#   Imports
import linecache
import numpy

from evolve_soft_2d import plotting, utility
from evolve_soft_2d.file_paths import create_fp_file

################################################################################

def monte_carlo(
    template,
    fp_lu: str,
    ) -> None:
    """Monte Carlo analysis

    Parameters
    ----------
    template 
        The unit template parameters
    fp_lu : str
        The file path of the log file of units created during the last simulation
    """

    #   Initialisations
    c_e = []
    i_e = []

    #   Read the list of units created during the last simulation
    with open(fp_lu) as f:
        unit_l = f.readlines()
    unit_l = [i.rstrip() for i in unit_l]

    #   Loop through the list of units
    for i in range(0, len(unit_l)):

        #   Initialisations
        c_e.append([])
        i_e.append([])

        #   Create the file paths for the current unit results
        fp_r_c_e = create_fp_file(template, "Constraint Energy_" + unit_l[i], "r")
        fp_r_i_e = create_fp_file(template, "Internal Energy_" + unit_l[i], "r")

        #   Add the current unit's constraint and internal energies at the final stage of the simulation
        c_e[i] = linecache.getline(fp_r_c_e, template.n_steps + 1)
        i_e[i] = linecache.getline(fp_r_i_e, template.n_steps + 1)

    #   Prepare the constraint and internal energies for analysis
    c_e = [i.rstrip() for i in c_e]
    (c_e, c_e_f) = utility.list_to_float(c_e)
    i_e = [i.rstrip() for i in i_e]
    (i_e, i_e_f) = utility.list_to_float(i_e)

    #   Output a warning message if any models do not deliver results
    if c_e_f != 0: 
        print("Warning: {} models failed to deliver a constraint energy!".format(c_e_f))
    if i_e_f != 0:
        print("Warning: {} models failed to deliver an internal energy!".format(i_e_f))

    #   Plot the results
    plotting.histogram(c_e, "Constraint Energy", "Frequency", "Energy (J)")
    plotting.histogram(i_e, "Internal Energy", "Frequency", "Energy (J)", color = "r")

    return

################################################################################

def constraint_energy(
    template,
    l: str,
    ) -> None:
    """Calculate the constraint energy for a unit

    Parameters
    ----------
    template 
        The unit template parameters
    l : str
        The label for the results file
        Either a template or unit identifier
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

            #   Store the results from the results file in the displacement variable
            d = numpy.genfromtxt(fp_r_f, delimiter = ",")*1000

        elif i == 1:

            #   Store the results from the results file in the reaction force variable
            r = numpy.genfromtxt(fp_r_f, delimiter = ",")

    #   Decrement the node IDs of the external nodes by 1 to be used as array indices
    n_external_i = [i - 1 for i in template.n_external]

    #   Store only the external node values
    d_ex = d[:, n_external_i]
    r_ex = r[:, n_external_i]

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

def internal_energy(
    template,
    l: str,
    ) -> None:
    """Calculate the internal energy for a unit

    Parameters
    ----------
    template 
        The unit template parameters
    l : str
        The label for the results file
        Either a template or unit identifier
    """    
    
    #   The labels of the required results
    label = "Total Strain Energy Density"

    #   Create the file path of the results file
    fp_r_f = create_fp_file(template, label + "_" + l, "r")

    #   Store the results from the results file in the strain energy variable
    s = numpy.genfromtxt(fp_r_f, delimiter = ",")*1000

    #   Initialise the interna; energy array
    i_e = numpy.zeros(len(s))

    #   Loop through every step in the unit
    for i in range(0, len(s)):

        #   Loop through every external node
        for j in range(0, len(s[0])):

            #   Calculate the constraint energy for the current step
            i_e[i] = i_e[i] + s[i, j]

    #   Save the boundary energies to a .csv file
    save_numpy_array_to_csv(template, "Internal Energy_" + l, i_e)

    return

################################################################################

def save_numpy_array_to_csv(
    template,
    l: str,
    data: numpy.array,
    ) -> None:
    """Write the results to .csv files

    Parameters
    ----------
    template 
        The unit template parameters
    l : str
        The label of the data
    data : numpy.array
        The results to be stored
    """    
    
    #   Create the file path of the results file
    fp_r_f = create_fp_file(template, l, "r")

    #   Write the data to the results file
    numpy.savetxt(fp_r_f, data, delimiter = ",")

    print("{}.csv saved".format(l))

    return