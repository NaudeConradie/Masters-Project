##  Functions used for obtaining and inspecting results

#   Imports
import csv
import fileinput
import linecache
import numpy
import pandas

from scipy.spatial.distance import directed_hausdorff

from evolve_soft_2d import plotting, utility
from evolve_soft_2d.evolve import gen_alg
from evolve_soft_2d.file_paths import create_fp_file
from evolve_soft_2d.result import obtain
from evolve_soft_2d.unit import create, modify

################################################################################

def monte_carlo(
    template,
    meth: str,
    ) -> None:
    """Perform a Monte Carlo analysis on a population of units

    Parameters
    ----------
    template : template
        The unit template parameters
    meth : str
        The unit generation method
        l : L-Systems
        c : CPPNs
        r : Random generation
    """

    #   Check if the unit generation method is set to L-Systems
    if meth == "l":
        
        #   Generate a list of unit parameters
        l_u, par = create.gen_init_units(template, gen_alg.n_u, meth, [gen_alg.ls_all_max, gen_alg.ls_all_min])

    #   Check if the unit generation method is set to CPPNs
    elif meth == "c":

        #   Generate a list of unit parameters
        l_u, par = create.gen_init_units(template, gen_alg.n_u, meth, [gen_alg.cppn_all_max, gen_alg.cppn_all_min])

    #   Check if the unit generation method is set to random
    else:

        #   Generate a list of unit parameters
        l_u, par = create.gen_init_units(template, gen_alg.n_u, meth, [[gen_alg.n_u + 1, len(template.e_internal) + 1], [1, 0]])

    #   Run the population of units
    fp_lu = create.run_units(template, l_u, meth)

    #   Rank the population of units
    rank_u(template, fp_lu)

    empty_id = "49_e43d862169605c50222e999b40714037"
    full_id = "0_d41d8cd98f00b204e9800998ecf8427e"
    rank_pop(fp_lu, empty_id, full_id, par)

    return

################################################################################

def rank_u(
    template,
    fp_lu: list,
    ) -> None:
    """Rank units according to their performance

    Parameters
    ----------
    template
        The unit template parameters
    fp_lu : str
        The file path of the log file of units created during the last simulation
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
    lu = obtain.read_lu(fp_lu[1])

    #   Create a list of the number of elements removed from every element
    n_e = [utility.find_int_in_str(i) for i in lu]

    #   Loop through all labels
    for i in range(0, len(label)):

        #   Initialisations
        v.append([])

        #   Read all values
        v[i].append(obtain.read_all(template, lu, label[i]))

    #   Add the Hausdorff distance to the list of labels
    label.append("Hausdorff Distance")

    #   Read the Hausdorff distance variables
    v.append([])
    v[-1].append(obtain.read_all_hd(template, lu))

    #   Remove unnecessary brackets from the values
    v = [i[0] for i in v]

    #   Store the list of units
    data["Unit ID"] = lu

    #   Loop through the values
    for i in range(0, len(v)):

        #   Add the values to the dataframe
        data[label[i]] = v[i]

    #   Read the timestamp of the simulation
    tm = utility.read_str(fp_lu[0], -25, -4)

    # plot_data = 

    # #   Plot the desired graphs from the results
    # plotting.plot_all(template, v, n_e, label, tm)

    data.sort_values(by = ["Hausdorff Distance"], inplace = True, ignore_index = True)
    
    #   Save the list of best performing units
    data["Unit ID"].to_csv(fp_lu[5], header = False, index = False)

    return

################################################################################

def rank_pop(
    fp_lu: list,
    empty_id: str,
    full_id: str,
    par: list,
    ) -> list:

    lu = obtain.read_lu(fp_lu[0])

    with open(fp_lu[5], 'r') as f:
        lu_rank = f.read()

    try:
        
        with open(fp_lu[3], 'r') as f:
            lu_empty = f.read()

        lu_rank = lu_rank.replace(empty_id, lu_empty)

    except:
        
        lu_rank = lu_rank.replace(empty_id, "")

    try:

        with open(fp_lu[4], 'r') as f:
            lu_full = f.read()

        lu_rank = lu_rank.replace(full_id, lu_full)

    except:

        lu_rank = lu_rank.replace(full_id, "")

    try:

        with open(fp_lu[2], 'r') as f:
            lu_fail = f.read()

        lu_rank += lu_fail

    except:

        pass

    print(lu_rank)

    lu_rank = list(lu_rank.split("\n"))

    print(lu_rank)

    while "" in lu_rank:
        lu_rank.remove("")

    print(lu_rank)

    data = pandas.DataFrame()

    print(lu)
    data["Unit ID"] = lu
    print(data)
    data["Parameters"] = par

    print(data)

    lu_rank_index = dict(zip(lu_rank, range(0, len(lu_rank))))

    data["Rank"] = data["Unit ID"].map(lu_rank_index)

    data.sort_values(["Rank"], ascending = [True], inplace = True)

    data.drop("Rank", 1, inplace = True)

    print(data)

    return

################################################################################

def constraint_energy(
    template,
    l: str,
    ) -> None:
    """Calculate the constraint energy for a unit

    Parameters
    ----------
    template : template
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

def disp(
    template,
    l: str,
    ) -> list:
    """Read the displacement values for a unit

    Parameters
    ----------
    template : template
        The unit template parameters
    l : str
        The label for the results file
        Either a template or unit identifier

    Returns
    -------
    list
        The list of displacement values
    """    

    #   Initialisations
    d_e = []

    label = []
    label.append("Displacement X")
    label.append("Displacement Y")

    d = numpy.zeros((len(label), template.n_steps + 1, template.n_n))

    #   Loop through the list of labels
    for i in range(0, len(label)):

        #   Create the file path of the results file
        fp_r_f = create_fp_file(template, label[i] + "_" + l, "r")

        #   Store the results from the file
        d[i] = numpy.genfromtxt(fp_r_f, delimiter = ",")

    #   Decrement the node IDs of the external nodes by 1 to be used as array indices
    n_external_i = [i - 1 for i in template.n_external]

    #   Store only the external node values
    d_ex = d[:, :, n_external_i]

    return d_ex

################################################################################

def hausdorff_d(
    template,
    l: str,
    ) -> None:
    """Calculate the Hausdorff distance values for a unit

    Parameters
    ----------
    template : template
        The unit template parameters
    l : str
        The label for the results file
        Either a template or unit identifier
    """    

    #   Read the displacement values of the unit
    d_e = disp(template, l)
    d_e = d_e[:, template.n_steps, :]

    #   Calculate the Hausdorff distance between the unit and the template displacements
    h_d = directed_hausdorff(d_e, template.d[:, template.n_steps, :])

    #   Save the internal energy to a .csv file
    save_numpy_array_to_csv(template, "Hausdorff Distance_" + l, h_d)

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