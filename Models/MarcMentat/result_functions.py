##  Functions used with the results

#   Imports

from utility_functions import *
from model_functions import run_job

from py_mentat import *
from py_post import *

import csv
import time
import os.path

from pathlib import Path

################################################################################

#   Check if the updated output files exist
#   Returns a flag based on the successful output of the model

#   rem_l:  String containing all removed elements
def check_out(rem_l):

    #   Initialisations
    t0 = time.time()
    success = False

    #   Time to wait for files
    t = 1

    #   Text to look for when searching the log files
    exit_n = re.compile("exit number", re.IGNORECASE)

    #   File paths to the respective model and output file
    file_mud = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Models\MarcMentat\element_' + rem_l + '.mud'
    file_log = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Models\MarcMentat\element_' + rem_l + '_job.log'
    file_t16 = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Models\MarcMentat\element_' + rem_l + '_job.t16'

    #   Obtain the timestamp of the last time the model file was modified
    t_mud = os.path.getmtime(file_mud)

    #   Wait until the log file exists and has been updated
    wait_file_exist(file_log, "log", t)
    wait_file_update(file_log, t_mud, "log", t)

    #   Loop until an exit number is detected
    while 1:

        #   Search the log file for an exit number
        (found, found_exit_n) = search_text_file(file_log, exit_n)

        #   Check if an exit number was found
        if found:

            #   Output the exit number
            print("Exit number found")
            print(found_exit_n)

            #   Exit the loop
            break

        #   Wait and check again
        else:
            wait(t, "exit number to be found")

    #   Check if the exit number indicates a successful run
    if found_exit_n.find("3004") != -1:

        #   Set the success flag
        success = True

        print("Model run successfully")

    elif found_exit_n.find("67") != -1:

        decided = False

        print("License server connection timed out.")

        while not decided:

            dec = input("Would you like to run again? (y/n) ")

            if dec == "y":

                decided = True

                run_job()

            elif dec == "n":

                decided = True

                print("Results cannot be analysed")

            else:

                print("Warning: Invalid input received!")
                print("Please either type a single \"y\" for yes or \"n\" for no")

    #   Output a warning
    else:
        print("Warning: Model run unsuccessfully!")
        print("Check log file and exit number for details")
        print("Results cannot be analysed")

    #   Check if the model was run successfully
    if success:

        #   Wait until the t16 file exists and has been updated
        wait_file_exist(file_t16, "t16", t)
        wait_file_update(file_t16, t_mud, "t16", t)

        t1 = time.time()

        print("Results generated in approximately %fs" % (t1 - t0))
    
    else:

        t1 = time.time()

        print("Results failed to generate after approximately %fs" % (t1 - t0))
        
    return success

################################################################################

#   Obtain maximum and minimum values from results

#   rem:        The element IDs of the removed elements
#   n_steps:    The number of steps in the second of the loadcase
def res_val(rem_l, n_steps):

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
    label.append("Normal Global Stress Layer 1")
    label.append("Shear Global Stress Layer 1")
    label.append("Normal Total Strain")
    label.append("Shear Total Strain")

    #   Open the results file
    py_send("@main(results) @popup(modelplot_pm) *post_open element_%s_job.t16" % rem_l)
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

        # print("%s" % label[i])
        # print("-----------------------------")
        # print("Time|Node|Max   |Node|Min")
        # print("-----------------------------")

        #   Loop through all steps of the post file
        for j in range(0, n_steps + 1):
            
            #   Obtain the current maximum and minimum values
            max_n_c = py_get_float("scalar_max_node()")
            max_v_c = py_get_float("scalar_1(%i)" % max_n_c)

            min_n_c = py_get_float("scalar_min_node()")
            min_v_c = py_get_float("scalar_1(%i)" % min_n_c)

            # print("%4.2f|%4i|%6.3f|%4i|%7.3f" % (j/n_steps, max_n_c, max_v_c, min_n_c, min_v_c))

            #   Check if the current value is the overall maximum and minimum value
            if max_v_c > max_v[i]:

                max_v[i] = max_v_c
                max_n[i] = max_n_c
                max_t[i] = j/n_steps

            if min_v_c < min_v[i]:

                min_v[i] = min_v_c
                min_n[i] = min_n_c
                min_t[i] = j/n_steps

            #   Increment the post file
            py_send("*post_next")

        # print("-----------------------------")

    #   Rewind the post file
    py_send("*post_rewind")

    #   Write the results to csv files
    save_csv("max", "v", rem_l, max_v)
    save_csv("max", "n", rem_l, max_n)
    save_csv("max", "t", rem_l, max_t)
    save_csv("min", "v", rem_l, min_v)
    save_csv("min", "n", rem_l, min_n)
    save_csv("min", "t", rem_l, min_t)

    #   Print the minimum and maximum values
    print("---------------------------------------------------------------")
    print("Label                       |Time|Node|Max   |Time|Node|Min")
    print("---------------------------------------------------------------")

    for i in range(0, len(label)):

        print("%-28s|%4.2f|%4i|%6.3g|%4.2f|%4i|%7.3g" % (label[i], max_t[i], max_n[i], max_v[i], min_t[i], min_n[i], min_v[i]))

    print("---------------------------------------------------------------")

    print("Results analysed")

    return

################################################################################

#   Write the results to .csv files

#   m:      Minimum or maximum
#   t:      Type of value
#   i:      ID of the results being written
#   data:   Data to be written
def save_csv(m, t, i, data):

    file_path = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Models\MarcMentat\Results'

    Path(file_path).mkdir(parents = True, exist_ok = True)

    file_name = m + "_" + t + "_" + i + ".csv"

    with open(file_path + "\\" + file_name, 'w') as f:

        wr = csv.writer(f)
        wr.writerow(data)

    print("%s saved" % file_name)

    return