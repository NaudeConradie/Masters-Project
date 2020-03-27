##  Test program

#   Imports

from py_mentat import *
from py_post import *

from functions import *

###################################################################

#   Main function

def main():

    n_steps = 20

    #   !   CHANGE EVERY TIME MAIN IS RERUN   !   #
    res_val(19, n_steps)

    return

if __name__ == '__main__':

    py_connect("", 40007)

    main()
    
    py_disconnect

