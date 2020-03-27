##  Test program

#   Imports

from py_mentat import *
from py_post import *

from functions import *

###################################################################

#   Main function

def main():

    #   !   CHANGE EVERY TIME MAIN IS RERUN   !   #
    res_val(19)

    return

if __name__ == '__main__':

    py_connect("", 40007)

    main()
    
    py_disconnect

