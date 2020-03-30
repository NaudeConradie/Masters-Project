##  Test program

#   Used to quickly test changes to functions with an existing case open

#   Imports

from py_mentat import *
from py_post import *

from functions import *

###################################################################

#   Main function

def main():

    n_steps = 20

    #   !   CHANGE EVERY TIME MAIN IS RERUN   !   #
    res_val(7, n_steps)

    (e_id, e_n_id) = obtain_e_n_ids()

    e_net = create_e_net(e_id, e_n_id)

    rem_el_free(e_id, e_net)

    return

if __name__ == '__main__':

    py_connect("", 40007)

    main()
    
    py_disconnect