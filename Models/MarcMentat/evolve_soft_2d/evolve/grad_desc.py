##  Genetic Algorithms

#   Imports

import numpy

from evolve_soft_2d import utility

################################################################################

def gradient_d(
    x: numpy.ndarray,
    y: numpy.ndarray,
    theta,
    n: int,
    learn_rate: float = 0.01,
    ):

    cost_l = numpy.zeros(n)
    theta_l = numpy.zeros((n, 2))

    for i in range(0, n):

        p = numpy.dot(x, theta)

        theta = theta - (1/len(y))*learn_rate*(x.T.dot((p - y)))

        theta_l[i, :] = theta.T

        cost_l[i] = cal_cost(x, y, theta)

    return theta, cost_l, theta_l

################################################################################

def cal_cost(
    x: numpy.ndarray,
    y: numpy.ndarray,
    theta,
    ):

    p = x.dot(theta)

    cost = (0.5*len(y))*numpy.sum(numpy.square(p - y))

    return cost