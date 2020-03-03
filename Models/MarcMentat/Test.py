#   Imports

from py_mentat import *
from py_post import *

#   Create the node grid

def make_nodes(s, t, xs, ys):

    y = ys
    z = 0
    delx = 1/s
    dely = 1/t

    for i in range(0, t):

        x = xs

        for j in range(0, s):

            str = "*add_nodes %f %f %f" % (x, y, z)

            py_send(str)

            x = x + delx

        y = y + dely

    return

# Create the element grid

def make_elements(n, m):

    for i in range(1, m):

        n1 = (i - 1)*(n) + 1
        n2 = n1 + 1
        n4 = n1 + (n)
        n3 = n2 + (n)

        for j in range(1, n):
            
            str = "*add_elements %d %d %d %d" % (n1, n2, n3, n4)

            py_send(str)

            n1 = n1 + 1
            n2 = n2 + 1
            n3 = n3 + 1
            n4 = n4 + 1

    return

def main():

    n = 5
    m = 5

    xs = -1
    ys = -1

    make_nodes(n, m, xs, ys)
    make_elements(n, m)

    return