##  Utility functions

#   Imports
import hashlib
import numpy
import os.path
import re
import time

from pathlib import Path

################################################################################

#   Wait for a specified time

#   t:  The time in seconds to wait
#   f:  The object being waited for
def wait(t, f):

    print("Waiting for %s..." % f)

    time.sleep(t)

    return

################################################################################

#   Wait until a specified file exists

#   file_name:  The name of the file to be waited for
#   label:      The label for the output message
#   t:          The time in seconds to wait per loop
def wait_file_exist(file_name, label, t):

    #   Loop until the file exists
    while 1:

        #   Check if the file exists
        exists = if_file_exist(file_name)

        #   Break out of the loop if the file exists
        if exists:

            break

        #   Wait and check again
        else:
            wait(t, "%s file to be created..." % label)

    return

################################################################################

#   Wait until a specified file is updated

#   file_name:  The name of the file to be waited for
#   t0:         The time since which the file should have been updated
#   label:      The label for the output message
#   t:          The time in seconds to wait per loop
def wait_file_update(file_name, t0, label, t):

    #   Loop until the file has been updated
    while 1:

        #   See how recently the file has been updated
        t_mod = os.path.getmtime(file_name)

        #   Break out of the loop if the file has been updated since the given time
        if t_mod > t0:

            break

        #   Wait and check again
        else:
            wait(t, "%s file to be updated..." % label)

    return

################################################################################

#   Check if a specified file exists

#   file_name:  The name of the file to be checked
def if_file_exist(file_name):

    exists = os.path.exists(file_name)

    #   Returns whether or not the file exists
    return exists

################################################################################

#   Make a folder if it does not exist

#   l:  The folder name and path as a string
def make_folder(l):

    Path(l).mkdir(parents=True, exist_ok=True)

    return

################################################################################

#   Randomly select a random amount of numbers from a given list of numbers

#   l:  The list of numbers
def sel_random(l):

    #   Initialisations
    sel = []
    l_temp = l[:]

    #   Generate a random number determining how many numbers will be selected
    sel_n = numpy.random.randint(low = 1, high = len(l))

    #   Loop through the list of numbers to be selected
    for i in range(0, sel_n):
        
        #   Select a random number from the list of numbers
        sel.append(numpy.random.choice(numpy.asarray(l_temp)))

        #   Remove the selected number from the list of numbers to prevent the same number from being selected more than once
        l_temp.remove(sel[i])

    #   Sort the list of selected numbers
    sel.sort()

    #   Returns the numbers that were selected
    return sel

################################################################################

#   Generate a random hash code from a given string

#   The string to be hashed
def gen_hash(s):

    m = hashlib.md5()
    m.update(bytes(s, encoding = 'utf8'))
    hash_code = str(m.hexdigest())

    #   Returns the hash code
    return hash_code

################################################################################

#   Search a text file for the first occurrence of a given text string

#   file_name:  The name of the file to be searched through
#   find_text:  The text to be searched for
def search_text_file(file_name, find_text):

    #   Initialisations
    found_text = ""
    found = False

    #   Open the file to be read
    with open(file_name, "rt") as f:

        #   Loop through every line in the file until the text string
        for line in f:

            #   Check if the text is in the current line of the file
            if find_text.search(line) != None:

                #   Save the entire line of text containing the desired text
                found_text = line.rstrip("\n")

                #   Set the found flag to true
                found = True

                #   Exit the loop
                break

    #   Returns if the text was found and the entire line it was found in
    return (found, found_text)

################################################################################

#   Add two lists and sort them

#   l1: The first list to be added
#   l2: The second list to be added
def add_sort_list(l1, l2):

    #   Add two lists
    l = l1 + l2

    #   Sort the added lists
    l.sort()

    #   Returns the added and sorted list
    return l

################################################################################

#   Convert a list into a string connected by a given symbol

#   l:  The list to be converted
#   c:  The symbol to be inserted between list items
def list_to_str(l, c):

    s = c.join(map(str, l))

    #   Returns the string
    return s

################################################################################

#   Finds the first integer in a string

#   s:  The string to be searched
def find_int_in_str(s):

    i = int(re.search(r'\d+', s).group())

    #   Returns the integer
    return i