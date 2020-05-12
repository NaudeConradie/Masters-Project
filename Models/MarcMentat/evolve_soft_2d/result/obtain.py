##  Functions used for obtaining and inspecting results

#   Imports
from evolve_soft_2d import unit, utility
from evolve_soft_2d.file_paths import fp_u, fp_r, create_fp_r_f
from evolve_soft_2d.log import m_log, en_log

from py_mentat import py_send, py_get_float

import csv
import time
import os.path
import re

################################################################################

def check_out(unit) -> bool:
    """Check if the updated output files exist

    Parameters
    ----------
    unit : class
        The unit parameters

    Returns
    -------
    bool
        True if the updated output files exist, false if otherwise
    """

    #   Initialisations
    t0 = time.time()
    success = False
    decided = False

    #   Time to wait for files
    t = 1

    #   Text to look for when searching the log files
    exit_number_str = re.compile("exit number", re.IGNORECASE)

    #   Obtain the timestamp of the last time the unit file was modified
    t_mud = os.path.getmtime(unit.fp_u_mud)

    #   Wait until the log file exists and has been updated
    utility.wait_file_exist(unit.fp_u_log, "log", t)
    utility.wait_file_update(unit.fp_u_log, t_mud, "log", t)

    #   Loop until an exit number is detected
    while 1:

        #   Search the log file for an exit number
        (found, found_exit_n) = utility.search_text_file(unit.fp_u_log, exit_number_str)

        #   Check if an exit number was found
        if found:

            #   Output the exit number
            exit_number = utility.find_int_in_str(found_exit_n)
            en_log.info("Exit number {} found for unit \"grid_{}.mud\"".format(exit_number, unit.u_id))

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
                success = check_out(unit)

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
        utility.wait_file_exist(unit.fp_u_t16, "t16", t)
        utility.wait_file_update(unit.fp_u_t16, t_mud, "t16", t)

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

def max_min(unit) -> None:
    """Obtain the maximum and minimum values from the results

    Parameters
    ----------
    unit : class
        The unit parameters
    """

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
    py_send("@main(results) @popup(modelplot_pm) *post_open \"{}\"".format(unit.fp_u_t16))
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
        for j in range(0, unit.template.n_steps + 1):
            
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
    save_2d_list_to_csv(unit, "max", max_save)
    save_2d_list_to_csv(unit, "min", min_save)

    m_log.info("Maximum and minimum result values obtained and stored")

    return

################################################################################

def all_n(unit) -> None:
    """Obtain values for all nodes from results

    Parameters
    ----------
    unit : class
        The unit parameters
    """

    #   The labels of the desired results
    label = []
    label.append("Equivalent Von Mises Stress")
    label.append("Displacement")
    label.append("Reaction Force")

    #   Open the results file
    py_send("@main(results) @popup(modelplot_pm) *post_open \"{}\"".format(unit.fp_u_t16))
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
        for j in range(0, unit.template.n_steps + 1):

            #   Append an empty list to create a new index for every step
            v.append([])

            #   Loop through all 
            for k in range(1, unit.template.n_n + 1):

                #   Append the current node's value to the list at the current step
                v[j].append(py_get_float("scalar_1({})".format(k)))

            #   Increment the post file
            py_send("*post_next")

        #   Save the values to a .csv file
        save_2d_list_to_csv(unit, label[i], v)

    #   Rewind the post file
    py_send("*post_rewind")

    m_log.info("All result values obtained and stored")

    return

################################################################################

def save_2d_list_to_csv(unit, t, data) -> None:
    """Write the results to .csv files

    Parameters
    ----------
    unit : class
        The unit parameters
    t : str
        The type of data to be stored
    data : list
        The results to be stored
    """

    #   Create the file path of the results file
    fp_r_csv = create_fp_r_f(unit, t)

    #   Write the data to the results file
    with open(fp_r_csv, 'w') as f:
        wr = csv.writer(f)
        wr.writerows(data)

    print("{}_{}.csv saved".format(t, unit.u_id))

    return