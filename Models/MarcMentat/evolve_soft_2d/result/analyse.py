##  Functions used for obtaining and inspecting results

#   Imports
import linecache
import numpy
import pandas

from evolve_soft_2d import plotting, utility
from evolve_soft_2d.file_paths import create_fp_file
from evolve_soft_2d.result import obtain

################################################################################

def sel_best_u(
    template,
    fp_lu: str,
    fp_bu: str,
    sel: int,
    ) -> None:
    """Monte Carlo analysis

    Parameters
    ----------
    template
        The unit template parameters
    fp_lu : str
        The file path of the log file of units created during the last simulation
    fp_bu : str
        The file path of the log file of the best units created during the last simulation
    sel : int
        The number of best units to select
    """

    #   Initialisations
    v = []
    data = pandas.DataFrame()

    label = []
    label.append("Constraint Energy X")
    label.append("Constraint Energy Y")
    label.append("Constraint Energy")
    label.append("Internal Energy X")
    label.append("Internal Energy Y")
    label.append("Internal Energy")

    #   Read the list of units created during the last simulation
    lu = obtain.read_lu(fp_lu)

    #   Determine the maximum amount of units that can be selected
    sel_max = len(lu)

    #   Ensure that the amount of units selected is within bounds
    sel = utility.clean_int(sel, sel_max)

    #   Create a list of the number of elements removed from every element
    n_e = [utility.find_int_in_str(i) for i in lu]

    #   Loop through all labels
    for i in range(0, len(label)):

        #   Initialisations
        v.append([])

        #   Read and plot all values
        v[i].append(obtain.read_all(label[i], n_e, lu, template))

    #   Remove unnecessary brackets from the values
    v = [i[0] for i in v]

    #   Store the list of units
    data["Unit ID"] = lu

    #   Loop through the values
    for i in range(0, len(v)):

        #   Add the values to the dataframe
        data[label[i]] = v[i]

    #   Read the timestamp of the simulation
    tm = utility.read_str(fp_lu, -25, -4)

    #   Plot the desired graphs from the results
    plotting.plot_all(template, v, n_e, label, tm)

    #   Check the case identifier
    if template.case == 1:

        #   Sort the relevant values in the dataframe in ascending order
        data.sort_values(by = ["Constraint Energy Y", "Constraint Energy X"], inplace = True, ignore_index = True)
        
    elif template.case == 2:

        #   Sort the relevant values in the dataframe in ascending order
        data.sort_values(by = ["Constraint Energy", "Internal Energy"], inplace = True, ignore_index = True)

    #   Select the requested number of best performing units
    unit_select = data.iloc[0:sel]
    
    #   Save the list of best performing units
    unit_select["Unit ID"].to_csv(fp_bu, header = False, index = False)

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
    
    #   Initialisations
    label = []
    label.append("Displacement X")
    label.append("Displacement Y")
    label.append("Displacement")
    label.append("Reaction Force X")
    label.append("Reaction Force Y")
    label.append("Reaction Force")

    label_c_e = []
    label_c_e.append("Constraint Energy X")
    label_c_e.append("Constraint Energy Y")
    label_c_e.append("Constraint Energy")

    v = numpy.zeros((len(label), template.n_steps + 1, template.n_n))

    #   Loop through all the variable labels
    for i in range(0, len(label)):

        #   Create the file path of the results file
        fp_r_f = create_fp_file(template, label[i] + "_" + l, "r")

        #   Store the results from the file
        v[i] = numpy.genfromtxt(fp_r_f, delimiter = ",")

    #   Decrement the node IDs of the external nodes by 1 to be used as array indices
    n_external_i = [i - 1 for i in template.n_external]

    #   Store only the external node values
    v_ex = v[:, :, n_external_i]

    #   Loop through every constraint energy label
    for i in range(0, len(label_c_e)):

        #   Initialise the constraint energy array
        c_e = numpy.zeros(len(v_ex[i]))

        #   Loop through every step in the unit
        for j in range(0, len(v_ex[i])):

            #   Loop through every external node
            for k in range(0, len(v_ex[i, i])):

                #   Calculate the constraint energy for the current step
                c_e[j] += v_ex[i, j, k]*v_ex[i + len(label_c_e), j, k]/1000

        #   Save the constraint energy to a .csv file
        save_numpy_array_to_csv(template, label_c_e[i] + "_" + l, c_e)

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
    
    #   Initialisations
    label = []
    label.append("Comp 11 of Total Strain")
    label.append("Comp 22 of Total Strain")
    label.append("Total Strain Energy Density")

    label_i_e = []
    label_i_e.append("Internal Energy X")
    label_i_e.append("Internal Energy Y")
    label_i_e.append("Internal Energy")

    s = numpy.zeros((len(label), template.n_steps + 1, template.n_n))

    #   Loop through all the variable labels
    for i in range(0, len(label)):

        #   Create the file path of the results file
        fp_r_f = create_fp_file(template, label[i] + "_" + l, "r")

        #   Store the results from the file
        s[i] = numpy.genfromtxt(fp_r_f, delimiter = ",")

    #   Loop through all the internal energy labels
    for i in range(0, len(label_i_e)):

        #   Initialise the internal energy array
        i_e = numpy.zeros(len(s[i]))

        #   Loop through every step in the unit
        for j in range(0, len(s[i])):

            #   Loop through every external node
            for k in range(0, len(s[i, i])):

                #   Calculate the internal energy for the current step
                i_e[j] += s[i, j, k]

        #   Save the internal energy to a .csv file
        save_numpy_array_to_csv(template, label_i_e[i] + "_" + l, i_e)

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