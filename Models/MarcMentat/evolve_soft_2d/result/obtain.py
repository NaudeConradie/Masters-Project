##  Functions used for obtaining and inspecting results

#   Imports
from evolve_soft_2d import unit, utility
from evolve_soft_2d.file_paths import fp_m, fp_r, create_fp_r_f
from evolve_soft_2d.log import m_log, en_log

from py_mentat import py_send, py_get_float

import csv
import time
import os.path
import re

################################################################################

#   Check if the updated output files exist
#   Returns a flag based on the successful output of the unit

#   fp_m_mud:   The complete file path of the unit file
#   fp_m_log:   The complete file path of the log file
#   fp_m_t16:   The complete file path of the t16 file
#   m_id:       The ID of the unit file
def check_out(mod):

    #   Initialisations
    t0 = time.time()
    success = False
    decided = False

    #   Time to wait for files
    t = 1

    #   Text to look for when searching the log files
    exit_number_str = re.compile("exit number", re.IGNORECASE)

    #   Obtain the timestamp of the last time the unit file was modified
    t_mud = os.path.getmtime(mod.fp_m_mud)

    #   Wait until the log file exists and has been updated
    utility.wait_file_exist(mod.fp_m_log, "log", t)
    utility.wait_file_update(mod.fp_m_log, t_mud, "log", t)

    #   Loop until an exit number is detected
    while 1:

        #   Search the log file for an exit number
        (found, found_exit_n) = utility.search_text_file(mod.fp_m_log, exit_number_str)

        #   Check if an exit number was found
        if found:

            #   Output the exit number
            exit_number = utility.find_int_in_str(found_exit_n)
            en_log.info("Exit number {} found for unit \"grid_{}.mud\"".format(exit_number, mod.m_id))

            #   Exit the loop
            break

        #   Wait and check again
        else:
            utility.wait(t, "exit number to be found")

    #   Check if the exit number indicates a successful run
    if exit_number == 3004:

        #   Set the success flag
        success = True

        m_log.info("Unit run successfully")

    #   Check if the exit number indicates a loss of connection to the license server
    elif exit_number == 67:
        m_log.error("License server connection timed out")

        #   Loop until a valid decision is made
        while not decided:

            #   Request a user response
            dec = input("Would you like to run again? (y/n) ")

            #   Check if the response was yes
            if dec == "y":

                #   Set flag that a decision was made
                decided = True

                #   Rerun the job
                unit.run_job()

                #   Check if the updated output files exist
                success = check_out(mod)

            #   Check if the response was no
            elif dec == "n":

                #   Set flag that a decision was made
                decided = True

                m_log.warning("Results cannot be analysed")

            #   Check if response was invalid
            else:

                m_log.error("Invalid input received")
                print("Please either type a single \"y\" for yes or \"n\" for no")

    #   Output a warning
    else:
        en_log.error("Unit run unsuccessfully with exit number {}".format(exit_number))
        m_log.warning("Results cannot be analysed. Check Mentat log file and exit number for details")

    #   Check if the unit was run successfully without a loss of connection to the license server
    if success and not decided:

        #   Wait until the t16 file exists and has been updated
        utility.wait_file_exist(mod.fp_m_t16, "t16", t)
        utility.wait_file_update(mod.fp_m_t16, t_mud, "t16", t)

        t1 = time.time()
        m_log.info("Results generated in approximately {:.3f}s".format(t1 - t0))
    
    #   Check if the unit was run successfully with a loss of connection to the license server
    elif success and decided:

        m_log.info("Results generated after initial connection failure")

    #   Output an error message
    else:

        t1 = time.time()
        m_log.warning("Results failed to generate after approximately {:.3f}s".format(t1 - t0))
        
    return success

################################################################################

#   Obtain the maximum and minimum values from the results

#   n_steps:    The number of steps in the second of the loadcase
#   n_e_l:      The number of elements as a string
#   case:       The unit case identifier
#   m_id:       The ID of the unit file
#   fp_m_t16:   The complete file path of the t16 file
def max_min(mod):

    #   Initialisations

    #   Empty lists for the values and their respective nodes and timestamps
    max_v = []
    max_n = []
    max_t = []
    min_v = []
    min_n = []
    min_t = []

    #   The labels of the desired results
    label = []
    label.append("Displacement X")
    label.append("Displacement Y")
    label.append("Reaction Force X")
    label.append("Reaction Force Y")
    label.append("Equivalent Von Mises Stress")
    label.append("Total Strain Energy Density")

    #   Open the results file
    mod
    py_send("@main(results) @popup(unitplot_pm) *post_open \"{}\"".format(mod.fp_m_t16))
    py_send("*post_numerics")

    #   Loop through all given labels
    for i in range(0, len(label)):

        #   Initialise lists for the current label
        max_v.append(0)
        max_n.append(0)
        max_t.append(0)

        min_v.append(0)
        min_n.append(0)
        min_t.append(0)

        #   Rewind the post file to the initial step
        py_send("*post_rewind")

        #   Set the post file to the current label
        py_send("*post_value {}".format(label[i]))

        #   Loop through all steps of the post file
        for j in range(0, mod.template.n_steps + 1):
            
            #   Obtain the current maximum and minimum values
            max_n_c = py_get_float("scalar_max_node()")
            max_v_c = py_get_float("scalar_1({})".format(max_n_c))

            min_n_c = py_get_float("scalar_min_node()")
            min_v_c = py_get_float("scalar_1({})".format(min_n_c))

            #   Check if the current value is the overall maximum or minimum value
            if max_v_c > max_v[i]:

                max_v[i] = max_v_c
                max_n[i] = int(max_n_c)
                max_t[i] = j

            if min_v_c < min_v[i]:

                min_v[i] = min_v_c
                min_n[i] = int(min_n_c)
                min_t[i] = j

            #   Increment the post file
            py_send("*post_next")

    #   Rewind the post file
    py_send("*post_rewind")

    max_save = []
    max_save.append(max_t)
    max_save.append(max_n)
    max_save.append(max_v)

    min_save = []
    min_save.append(min_t)
    min_save.append(min_n)
    min_save.append(min_v)

    #   Write the results to csv files
    save_2d_list_to_csv(mod, "max", max_save)
    save_2d_list_to_csv(mod, "min", min_save)

    m_log.info("Maximum and minimum result values obtained and stored")

    return

################################################################################

#   Obtain values for all nodes from results

#   n_n:        The number of nodes
#   n_steps:    The number of steps in the second of the loadcase
#   n_e_l:      The number of elements as a string
#   case:       The unit case identifier
#   m_id:       The ID of the unit file
#   fp_m_t16:   The complete file path of the t16 file
def all_n(mod):

    #   The labels of the desired results
    label = []
    label.append("Equivalent Von Mises Stress")
    label.append("Displacement")
    label.append("Reaction Force")

    #   Open the results file
    py_send("@main(results) @popup(unitplot_pm) *post_open \"{}\"".format(mod.fp_m_t16))
    py_send("*post_numerics")

    #   Loop through all given labels
    for i in range(0, len(label)):

        #   Initialise list for the current label
        v = []

        #   Rewind the post file to the initial step
        py_send("*post_rewind")

        #   Set the post file to the current label
        py_send("*post_value {}".format(label[i]))

        #   Loop through all steps of the post file
        for j in range(0, mod.template.n_steps + 1):

            #   Append an empty list to create a new index for every step
            v.append([])

            #   Loop through all 
            for k in range(1, mod.template.n_n + 1):

                #   Append the current node's value to the list at the current step
                v[j].append(py_get_float("scalar_1({})".format(k)))

            #   Increment the post file
            py_send("*post_next")

        #   Save the values to a .csv file
        save_2d_list_to_csv(mod, label[i], v)

    #   Rewind the post file
    py_send("*post_rewind")

    m_log.info("All result values obtained and stored")

    return

################################################################################

#   Write the results to .csv files

#   n_e_l:  The number of elements as a string
#   case:   The unit case identifier
#   t:      The type of data to be stored
#   m_id:   The ID of the unit file
#   data:   The results to be stored
def save_2d_list_to_csv(mod, t, data):
    
    #   Create the file path of the results file
    fp_r_csv = create_fp_r_f(mod, t)

    #   Write the data to the results file
    with open(fp_r_csv, 'w') as f:
        wr = csv.writer(f)
        wr.writerows(data)

    print("{}_{}.csv saved".format(t, mod.m_id))

    return