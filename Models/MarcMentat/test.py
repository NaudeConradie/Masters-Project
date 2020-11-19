##  Main program

#   Imports
import importlib
import numpy
import seaborn

from evolve_soft_2d import classes, file_paths, log, plotting, utility
from evolve_soft_2d.evolve import cppns, gen_alg, lsystems
from evolve_soft_2d.result import analyse, obtain
from evolve_soft_2d.unit import create, inspect, modify, rep_grid

from evolve_soft_2d.file_paths import create_fp_file

from py_mentat import py_connect, py_disconnect

################################################################################

#   Main function

def main():

    #   Reload the modules
    importlib.reload(classes)
    importlib.reload(file_paths)
    importlib.reload(plotting)
    importlib.reload(utility)
    importlib.reload(cppns)
    importlib.reload(gen_alg)
    importlib.reload(lsystems)
    importlib.reload(analyse)
    importlib.reload(obtain)
    importlib.reload(create)
    importlib.reload(inspect)
    importlib.reload(modify)
    importlib.reload(rep_grid)

    #   Initialisations
    #   The template case identifier
    case = 1
    #   The number of elements in each axis direction
    x_e = 15
    y_e = 15
    #   The length of each side in mm
    e_s = 10
    #   The thickness of the unit boundary
    b = 3
    #   The number of increments per second to analyse
    n_steps = 5
    #   The text name of the table used for the applied displacement and load
    table_name = "ramp_input"
    #   The magnitude of the applied displacement in mm
    d_mag = y_e*e_s/2
    #   The magnitude of the applied internal pressure in MPa
    p_mag = 0.025

    #   The unit generation method
    g_meth = "l"
    #   The analysis method
    a_meth = "g"

    #   Genetic algorithm parameters
    gen = 15
    prob = [0.5, 0.1, 0.5]
    point = [1, 2, 2]

    #   Prepare the unit parameters
    temp = classes.template(case, x_e, y_e, e_s, b, classes.mold_star_15, n_steps, table_name, d_mag, p_mag)

    t = "_2020-10-28--16-00-12"

    # 2020-10-29--14-18-46 
    # 2020-11-14--07-51-17
    # 2020-10-28--16-00-12

    #   Generate the grid with all elements removed
    grid_rem_e, rem_e = create.gen_grid_rem_free(temp, temp.e_internal)

    #   Generate the unit ID of the empty unit
    empty_id = str(len(rem_e)) + "_" + utility.gen_hash(utility.list_to_str(rem_e, "_"))

    #   Generate the grid with all elements removed
    grid_rem_f, rem_f = create.gen_grid_rem_free(temp, [])

    #   Generate the unit ID of the full unit
    full_id = str(len(rem_f)) + "_" + utility.gen_hash(utility.list_to_str(rem_f, "_"))

    fp_lu = [create_fp_file(temp, t, "l"), create_fp_file(temp, t + "_success", "l"), create_fp_file(temp, t + "_failed", "l"), create_fp_file(temp, t + "_empty", "l"), create_fp_file(temp, t + "_full", "l"), create_fp_file(temp, t + "_ranked", "l")]

    data = analyse.rank_u(temp, g_meth, empty_id, full_id, fp_lu)

    # data_c_e = data[(data["Constraint Energy"] >= 0) & (data["Constraint Energy"] < 0.0002)]

    plotting.hist(temp, t, data, "Internal Energy")

    data_col = [i for i in data.columns]

    for i in data_col:

        seaborn.relplot(x = i, y = "Internal Energy", data = data)

        #   Save the figure
        plotting.save_plot(temp, i + "_vs_Internal Energy", t)

    return

main()