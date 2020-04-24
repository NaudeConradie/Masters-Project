##  Functions used for obtaining and inspecting results

#   Imports
from evolve_soft_2d.file_paths import create_fp_r_f

import numpy

################################################################################

#   Calculate the boundary energy for a model
#   Returns the boundary energy

#   n_e_l:      The number of elements as a string
#   case:       The model case identifier
#   m_id:       The ID of the model file
#   n_external: The list of external nodes
def boundary_energy(n_e_l, case, m_id, n_external):

    #   The labels of the required results
    label = []
    label.append("Displacement")
    label.append("Reaction Force")

    #   Loop through all the labels
    for i in range(0, len(label)):

        #   Create the file path of the results file
        fp_r_f = create_fp_r_f(n_e_l, case, label[i], m_id)

        #   Determine which variable to store the results in
        if i == 0:

            #   Store the results from the results file in the correct variable
            d = numpy.genfromtxt(fp_r_f, delimiter = ",")

        elif i == 1:

            #   Store the results from the results file in the correct variable
            r = numpy.genfromtxt(fp_r_f, delimiter = ",")

    #   Decrement the node IDs of the external nodes by 1 to be used as array indices
    n_external_i = [i - 1 for i in n_external]

    #   Store only the external node values
    d_ex_mm = d[:, n_external_i]
    r_ex = r[:, n_external_i]

    #   Convert from mm to m
    d_ex = d_ex_mm*1000

    #   Initialise the boundary energy array
    b_e = numpy.zeros(len(d_ex))

    #   Loop through every step in the model
    for i in range(0, len(d_ex)):

        #   Loop through every external node
        for j in range(0, len(d_ex[0])):

            #   Calculate the boundary energy for the current step
            b_e[i] = b_e[i] + d_ex[i, j]*r_ex[i, j]

    return b_e

################################################################################