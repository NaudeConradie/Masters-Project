##  Utility functions

#   Imports
import hashlib
import numpy
import os.path
import re
import time

from pathlib import Path

################################################################################

def wait(
    t: float,
    f: str,
    ) -> None:
    """Wait for a specified time

    Parameters
    ----------
    t : float
        The time in seconds to wait
    f : str
        The name of the object being waited for
    """

    print("Waiting for %s..." % f)

    time.sleep(t)

    return

################################################################################
  
def wait_file_exist(
    file_name: str,
    label: str,
    t: float,
    ) -> None:
    """Wait until a specified file exists

    Parameters
    ----------
    file_name : str
        The name of the file to be waited for
    label : str
        The label for the output message
    t : float
        The time in seconds to wait per loop
    """
    
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
  
def wait_file_update(
    file_name: str,
    t0: float,
    label: str,
    t: float,
    ) -> None:
    """Wait until a specified file is updated

    Parameters
    ----------
    file_name : str
        The name of the file to be waited for
    t0 : float
        The time since which the file should have been updated
    label : str
        The label for the output message
    t : float
        The time in seconds to wait per loop
    """

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

def if_file_exist(file_name: str) -> bool:
    """Check if a specified file exists

    Parameters
    ----------
    file_name : str
        The name of the file to be checked

    Returns
    -------
    bool
        True if the file exists, False otherwise
    """

    exists = os.path.exists(file_name)

    return exists

################################################################################

def make_folder(l: str) -> None:
    """Make a folder if it does not exist

    Parameters
    ----------
    l : str
        The folder name and path
    """

    Path(l).mkdir(parents=True, exist_ok=True)

    return

################################################################################

def sel_random(l: list) -> list:
    """Randomly select a random number of numbers from a given list of numbers

    Parameters
    ----------
    l : list
        The given list of numbers

    Returns
    -------
    list
        The randomly selected numbers
    """

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

    return sel

################################################################################

def sel_random_fixed(
    l: list,
    f: int,
    ) -> list:
    """Randomly select a fixed number of numbers from a given list of numbers

    Parameters
    ----------
    l : list
        The given list of numbers
    f : int
        The fixed number of numbers

    Returns
    -------
    list
        The randomly selected numbers
    """    
    
    #   Initialisations
    sel = []
    l_temp = l[:]

    #   Loop through the list of numbers to be selected
    for i in range(0, f):
        
        #   Select a random number from the list of numbers
        sel.append(numpy.random.choice(numpy.asarray(l_temp)))

        #   Remove the selected number from the list of numbers to prevent the same number from being selected more than once
        l_temp.remove(sel[i])

    #   Sort the list of selected numbers
    sel.sort()

    return sel

################################################################################

def sel_random_range(
    l: list,
    r: list,
    ) -> list:
    """Randomly select a ranged amount of numbers from a given list of numbers

    Parameters
    ----------
    l : list
        The given list of numbers
    r : list
        The range of numbers to be selected

    Returns
    -------
    list
        The randomly selected numbers
    """

    #   Initialisations
    sel = []
    l_temp = l[:]

    r_sel = numpy.random.choice(numpy.asarray(r))

    #   Loop through the list of numbers to be selected
    for i in range(0, r_sel):
        
        #   Select a random number from the list of numbers
        sel.append(numpy.random.choice(numpy.asarray(l_temp)))

        #   Remove the selected number from the list of numbers to prevent the same number from being selected more than once
        l_temp.remove(sel[i])

    #   Sort the list of selected numbers
    sel.sort()

    return sel

################################################################################

def replace(x: int, m: int) -> int:
    """Replace list elements that are outside of an allowed range

    Parameters
    ----------
    x : int
        The list item to be inspected
    m : int
        The maximum allowed value

    Returns
    -------
    int
        The list item value
    """    

    if x > m:
        return m

    elif x <= 0:
        return 1

    else:
        return x

################################################################################

#   Generate a random hash code from a given string

#   The string to be hashed
def gen_hash(s: str) -> str:
    """Generate a random hash code from a given string

    Parameters
    ----------
    s : str
        The string to be hashed

    Returns
    -------
    str
        The hash code
    """
    m = hashlib.md5()
    m.update(bytes(s, encoding = 'utf8'))
    hash_code = str(m.hexdigest())

    return hash_code

################################################################################

def search_text_file(
    file_name: str,
    find_text: str,
    ) -> (bool, str):
    """Search a text file for the first occurrence of a given text string

    Parameters
    ----------
    file_name : str
        The name of the file to be searched through
    find_text : str
        The text to be searched for

    Returns
    -------
    (bool, str)
        True if the text was found, false otherwise
        The entire line containing the text
    """
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

    return (found, found_text)

################################################################################

def add_sort_list(
    l1: list,
    l2: list,
    ) -> list:
    """Add two lists and sort them

    Parameters
    ----------
    l1 : list
        The first list to be added
    l2 : list
        The second list to be added

    Returns
    -------
    list
        The added and sorted list
    """
    #   Add two lists
    l = l1 + l2

    #   Sort the added lists
    l.sort()

    return l

################################################################################

def list_to_float(l: list) -> [list, int]:
    """Extract a list of floats from a given list

    Parameters
    ----------
    l : list
        The list to be extracted from

    Returns
    -------
    [list, int]
        The list of floats
        The number of list of items that failed to convert to string
    """

    #   Initialisations
    l_o = []
    l_f = 0

    #   Loop through the list
    for i in range(0, len(l)):

        #   Add the current list item as a float
        try:
            l_o.append(float(l[i]))

        #   Increment the failure counter
        except:
            l_f += 1

    return (l_o, l_f)

################################################################################

def list_to_str(
    l: list,
    c: str,
    ) -> str:
    """Convert a list into a string connected by a given symbol

    Parameters
    ----------
    l : list
        The list to be converted
    c : str
        The symbol to be inserted between list items

    Returns
    -------
    str
        The output string
    """

    s = c.join(map(str, l))

    return s

################################################################################

def find_int_in_str(s: str) -> int:
    """Finds the first integer in a string

    Parameters
    ----------
    s : str
        The string to be searched

    Returns
    -------
    int
        The integer found
    """
    
    i = int(re.search(r'\d+', s).group())

    return i