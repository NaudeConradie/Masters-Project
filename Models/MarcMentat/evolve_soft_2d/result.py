##  Functions used for obtaining and inspecting results

#   Imports
from evolve_soft_2d import model, utility
from evolve_soft_2d.file_paths import fp_m, fp_r
from evolve_soft_2d.log import m_log, en_log

from py_mentat import py_send, py_get_float

import csv
import time
import os.path
import re

################################################################################

#   Check if the updated output files exist
#   Returns a flag based on the successful output of the model

#   id1:    The number of elements in the x-direction times the number of elements in the y-direction
#   id2:    The model case identifier
#   id3:    The model identifier
def check_out(id1, id2, id3):

    #   Initialisations
    t0 = time.time()
    success = False
    decided = False

    #   Time to wait for files
    t = 1

    #   Text to look for when searching the log files
    exit_number_str = re.compile("exit number", re.IGNORECASE)

    #   File paths to the respective model and output files
    fp_id_t = r'\grid_' + id1 + '_' + id2
    fp_id_m = r'\grid_' + id3
    fp_id = fp_m + fp_id_t + fp_id_m + fp_id_m
    fp_mud = fp_id + '.mud'
    fp_log = fp_id + '_job.log'
    fp_t16 = fp_id + '_job.t16'

    #   Obtain the timestamp of the last time the model file was modified
    t_mud = os.path.getmtime(fp_mud)

    #   Wait until the log file exists and has been updated
    utility.wait_file_exist(fp_log, "log", t)
    utility.wait_file_update(fp_log, t_mud, "log", t)

    #   Loop until an exit number is detected
    while 1:

        #   Search the log file for an exit number
        (found, found_exit_n) = utility.search_text_file(fp_log, exit_number_str)

        #   Check if an exit number was found
        if found:

            #   Output the exit number
            exit_number = utility.find_int_in_str(found_exit_n)
            en_log.info("Exit number %s found for model \"grid_%s.mud\"" % (exit_number, id3))

            #   Exit the loop
            break

        #   Wait and check again
        else:
            utility.wait(t, "exit number to be found")

    #   Check if the exit number indicates a successful run
    if exit_number == 3004:

        #   Set the success flag
        success = True

        m_log.info("Model run successfully")

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
                model.run_job()

                #   Check if the updated output files exist
                success = check_out(id1, id2, id3)

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
        en_log.error("Model run unsuccessfully with exit number %i" % exit_number)
        m_log.warning("Results cannot be analysed. Check Mentat log file and exit number for details")

    #   Check if the model was run successfully without a loss of connection to the license server
    if success and not decided:

        #   Wait until the t16 file exists and has been updated
        utility.wait_file_exist(fp_t16, "t16", t)
        utility.wait_file_update(fp_t16, t_mud, "t16", t)

        t1 = time.time()

        m_log.info("Results generated in approximately %fs" % (t1 - t0))
    
    #   Check if the model was run successfully with a loss of connection to the license server
    elif success and decided:

        m_log.info("Results generated after initial connection failure")

    #   Output an error message
    else:

        t1 = time.time()

        m_log.warning("Results failed to generate after approximately %fs" % (t1 - t0))
        
    return success

################################################################################

#   Obtain maximum and minimum values from results

#   f_id:       Identification string
#   e:          Identification string of grid size
#   n_steps:    The number of steps in the second of the loadcase
def get_max_min(id1, id2, id3, n_steps):

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
    fp_id_t = r'\grid_' + id1 + '_' + id2
    fp_id_m = r'\grid_' + id3
    fp_id = fp_m + fp_id_t + fp_id_m + fp_id_m
    fp_t16 = fp_id + '_job.t16'
    py_send("@main(results) @popup(modelplot_pm) *post_open \"%s\"" % fp_t16)
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
        py_send("*post_value %s" % label[i])

        #   Loop through all steps of the post file
        for j in range(0, n_steps + 1):
            
            #   Obtain the current maximum and minimum values
            max_n_c = py_get_float("scalar_max_node()")
            max_v_c = py_get_float("scalar_1(%i)" % max_n_c)

            min_n_c = py_get_float("scalar_min_node()")
            min_v_c = py_get_float("scalar_1(%i)" % min_n_c)

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
    save_csv(id1, id2, id3, "max", id3, max_save)
    save_csv(id1, id2, id3, "min", id3, min_save)

    m_log.info("Maximum and minimum result values obtained and stored")

    return

################################################################################

#   Obtain all values from results

#   f_id:       Identification string
#   e:          Identification string of grid size
#   n_n:        The number of nodes
#   n_steps:    The number of steps in the second of the loadcase
def get_all(id1, id2, id3, n_n, n_steps):

    #   The labels of the desired results
    label = []
    label.append("Displacement X")
    label.append("Displacement Y")
    label.append("Reaction Force X")
    label.append("Reaction Force Y")

    #   Open the results file
    fp_id_t = r'\grid_' + id1 + '_' + id2
    fp_id_m = r'\grid_' + id3
    fp_id = fp_m + fp_id_t + fp_id_m + fp_id_m
    fp_t16 = fp_id + '_job.t16'
    py_send("@main(results) @popup(modelplot_pm) *post_open \"%s\"" % fp_t16)
    py_send("*post_numerics")

    #   Loop through all given labels
    for i in range(0, len(label)):

        #   Initialise list for the current label
        v = []

        #   Rewind the post file to the initial step
        py_send("*post_rewind")

        #   Set the post file to the current label
        py_send("*post_value %s" % label[i])

        #   Loop through all steps of the post file
        for j in range(0, n_steps + 1):

            #   Append an empty list to create a new index for every step
            v.append([])

            #   Loop through all 
            for k in range(1, n_n + 1):

                #   Append the current node's value to the list at the current step
                v[j].append(py_get_float("scalar_1(%i)" % k))

            #   Increment the post file
            py_send("*post_next")

        #   Save the values to a .csv file
        save_csv(id1, id2, id3, label[i], id3, v)

    #   Rewind the post file
    py_send("*post_rewind")

    m_log.info("All result values obtained and stored")

    return

################################################################################

#   Write the results to .csv files

#   m:      Minimum or maximum
#   i:      ID of the results being written
#   data:   Data to be written
def save_csv(id1, id2, id3, m, i, data):

    fp_id_t = r'\grid_' + id1 + '_' + id2
    fp_id = fp_r + fp_id_t

    utility.make_folder(fp_id)
    
    fp_csv = m + "_" + i + ".csv"

    with open(fp_id + "\\" + fp_csv, 'w') as f:

        wr = csv.writer(f)
        wr.writerows(data)

    print("%s saved" % fp_csv)

    return