##  Main program

#   Imports

from py_mentat import *
from py_post import *

#   Create the node grid

def create_nodes(x0, y0, x_n, y_n):

    y = y0

    z = 0

    del_x = 1/x_n
    del_y = 1/y_n

    for i in range(0, y_n):

        x = x0

        for j in range(0, x_n):
            
            py_send("*add_nodes %f %f %f" % (x, y, z))

            x = x + del_x

        y = y + del_y

    return

#   Create the element grid

def create_elements(n, m):

    for i in range(1, m):

        n1 = (i - 1)*n + 1
        n2 = n1 + 1
        n3 = n2 + n
        n4 = n1 + n

        for j in range(1, n):

            py_send("*add_elements %d %d %d %d" % (n1, n2, n3, n4))

            n1 = n1 + 1
            n2 = n2 + 1
            n3 = n3 + 1
            n4 = n4 + 1

    return

#   Add fixed boundary conditions to left and bottom sides

def add_bc_fixed(x_bc, y_bc, x_n, y_n):

    n_n = py_get_int("nnodes()")

    py_send("*apply_type fixed_displacement")
    py_send("*apply_dof x")
    py_send("*apply_dof y")
    py_send("*apply_dof z")

    n_l = []

    for i in range(1, n_n + 1):

        x = py_get_float("node_x(%d)" % i)

        if tol_check(x, x_bc, 0.001):

            node_list.append(i)

    



#   Main function

def main():

    x_n = 6
    y_n = 6

    x0 = 0
    y0 = 0

    create_nodes(x0, y0, x_n, y_n)

    create_elements(x_n, y_n)

    if __name__ = '__main__':

        py_connect("", 40007)

        main()

        py_disconnect

    return


