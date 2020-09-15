##  Genetic Algorithms

#   Imports

import numpy

from evolve_soft_2d import utility
from evolve_soft_2d.unit import create

################################################################################

# def genetic(
#     template,
#     pop_n: int,
#     chrom: int,
#     all_max: list,
#     all_min: list,
#     gen: int,
#     prob: list,
#     point: list,
#     meth: str,
#     c: float = 1,
#     ) -> None:

#     if meth == "l":

#         pop_i = create.gen_units(template, pop_n, l = [all_max, all_min])

#     elif meth == "c":

#         pop_i = create.gen_units(template, pop_n, c = [all_max, all_min])

#     else:

#         pop_i = create.gen_units(template, pop_n)

#     pop_all = []
#     pop_all.append(pop_i)
#     pop_ip1 = pop_i[:]
#     pop_best = numpy.zeros((gen, chrom))

#     for i in range(0, gen):

#         #   Fitness evaluation

#         for j in range(0, pop_n, 2):

#             par_1 = sel_par(pop_n, c, fit_i, pop_i)
#             par_2 = sel_par(pop_n, c, fit_i, pop_i)

#             chi_1, chi_2 = crossover(chrom, prob_co, co_point_n, par_1, par_2)

#             chi_1 = mut(chrom, all_max, all_min, prob_m, chi_1)
#             chi_2 = mut(chrom, all_max, all_min, prob_m, chi_2)

#             chi_1 = mut_bias(chrom, all_max, all_min, prob_bm, chi_1)
#             chi_2 = mut_bias(chrom, all_max, all_min, prob_bm, chi_2)

#             pop_ip1[j] = chi_1
#             pop_ip1[j + 1] = chi_2

#         pop_i = pop_ip1

#         pop_all.append(pop_i)

#         #   Store the best member of the current generation

#     return

################################################################################

def gen_par(
    pop_n: int,
    chrom: int,
    all_max: list,
    all_min: list,
    ) -> list:
    """Generate a random initial population

    Parameters
    ----------
    pop_n : int
        The population size
    chrom : int
        The number of chromosomes a member has
    all_max : list
        The list of the maximum allele values
    all_min : list
        The list of the minimum allele values

    Returns
    -------
    list
        The population
    """    

    #   Initialisations
    pop_i = []

    #   Loop through the number of members to generate
    for i in range(0, pop_n):

        pop_i.append([])

        #   Loop through the number of chromosomes
        for j in range(0, chrom):

            #   Add a new random allele value
            pop_i[i].append(numpy.random.randint(all_min[j], all_max[j]))

    return pop_i

################################################################################

def sel_par(
    pop_n: int,
    fit_i: list,
    pop: list,
    c: float,
    ) -> list:
    """Select a parent to produce the new generation

    Parameters
    ----------
    pop_n : int
        The population size
    fit_i : list
        The fitness indices
    pop : list
        The population
    c : float
        The fitness function constant

    Returns
    -------
    list
        The parent
    """    

    #   Initialisations
    i = 0
    par_found = False
    par = pop[fit_i[0]]

    #   Generate a random threshold between 0 and 1
    x = numpy.random.uniform(size = 1)

    #   Loop until a parent is found
    while i < pop_n and not par_found:

        #   Calculate the upper and lower bounds for comparison with the threshold
        x_bel = sum([fit_check(pop_n, c, j) for j in range(1, i + 1)])
        x_abo = sum([fit_check(pop_n, c, j) for j in range(1, i + 2)])

        #   Check if the threshold is within the bounds
        if x_bel < x and x <= x_abo:

            #   Assign the parent
            par = pop[fit_i[i]]

            #   Set the exit flaf
            par_found = True

        else:

            #   Increment the counter
            i += 1

    return par

################################################################################

def crossover(
    chrom: int,
    prob_co: float,
    point_co: int,
    par_1: list,
    par_2: list
    ) -> [list, list]:
    """Apply genetic crossover to two children from two parents

    Parameters
    ----------
    chrom : int
        The number of chromosomes a member has
    prob_co : float
        The probability of crossover occurring
    point_co : int
        The potential number of crossover points
    par_1 : list
        The first parent
    par_2 : list
        The second parent

    Returns
    -------
    [list, list]
        The two children
    """    

    #   Initialisations
    chi_1 = par_1[:]
    chi_2 = par_2[:]

    #   Loop through the number of potential crossover points
    for _ in range(0, point_co):

        #   Generate a random value between 0 and 1
        x = numpy.random.uniform(size = 1)

        #   Check if the random value is below the probability
        if x < prob_co:

            #   Select a random index for crossover to occur
            co_point = numpy.random.randint(1, chrom - 1)

            #   Create temporary copies of the children
            chi_1_c = chi_1[:]
            chi_2_c = chi_2[:]

            #   Apply the crossover
            chi_1 = chi_1_c[:co_point] + chi_2_c[co_point + 1:]
            chi_2 = chi_2_c[:co_point] + chi_2_c[co_point + 1:]

    return chi_1, chi_2

################################################################################

def mut(
    chrom: int,
    all_max: list,
    all_min: list,
    prob_m: float,
    point_m: int,
    chi: list,
    ) -> list:
    """Apply random mutation to a member

    Parameters
    ----------
    chrom : int
        The number of chromosomes a member has
    all_max : list
        The list of the maximum allele values
    all_min : list
        The list of the minimum allele values
    prob_m : float
        The probability of random mutation occurring
    point_m: int
        The number of potential random mutations
    chi : list
        The member

    Returns
    -------
    list
        The mutated member
    """

    #   Loop for the number of potential random mutations
    for _ in range(0, point_m):

        #   
        x = numpy.random.uniform(size = 1)

        if x < prob_m:

            m_point = numpy.random.randint(0, chrom)

            chi[m_point] = numpy.random.randint(all_min[m_point], all_max[m_point])

    return chi

################################################################################

def mut_bias(
    chrom: int,
    all_max: list,
    all_min: list,
    prob_bm: float,
    chi: list,
    ) -> list:

    x = numpy.random.uniform(size = 1)

    if x < prob_bm:

        bm_point = numpy.random.randint(0, chrom)

        y = numpy.random.uniform(size = 1)

        if y < 0.5:

            chi[bm_point] -= 1

        else:

            chi[bm_point] += 1

        chi[bm_point] = utility.clean_int(chi[bm_point], all_max[bm_point], lb = all_min[bm_point])

    return chi

################################################################################

def fit_check(
    p: int,
    c: int,
    x: int,
    ) -> float:

    y = (2*((p + 1 - x)**c))/(p**2 + p)

    return y