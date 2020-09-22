##  Functions used with the Marc Mentat units

#   Imports
import numpy
import time

from py_mentat import py_send

from evolve_soft_2d import classes, utility
from evolve_soft_2d.evolve import cppns, gen_alg, lsystems
from evolve_soft_2d.unit import inspect, modify, rep_grid
from evolve_soft_2d.result import analyse, obtain
from evolve_soft_2d.file_paths import create_fp_file

################################################################################

def gen_init_units(
    template,
    n: int,
    meth: str,
    a: list,
    ) -> list:
    """Generate an initial population of units

    Parameters
    ----------
    template
        The unit template parameters
    n : int
        The number of units to generate
    meth : str
        The unit generation method
        l:  L-Systems
        c:  CPPNs
        r:  Random
    a : list
        The maximum and minimum parameters

    Returns
    -------
    list
        The population
    """    

    #   Initialisations
    rem = []

    #   Check if the generation method is specified as L-Systems
    if meth == "l":

        #   Initialisations
        ls = []

        #   Generate the random parameters
        ls_par = gen_alg.gen_par(n, 5, a[0], a[1])

        #   Loop through the list of parameters
        for i in ls_par:

            #   Create the current L-System instance
            ls_i = lsystems.gen_lsystem(i[0], lsystems.e_vocabulary, i[1], i[2], i[3], i[4])

            #   Add the L-System instance to the list
            ls.append(ls_i)

            #   Obtain the list of elements to be removed
            rem.append(lsystems.interpret_word(template, ls_i.word))

        #   Save the list of units
        lu = numpy.array([rem, ls]).T.tolist()

    #   Check if the generation method is specified as CPPNs
    elif meth == "c":

        #   Initialisations
        cp = []

        #   Generate the random parameters
        cp_par = gen_alg.gen_par(n, 6, a[0], a[1])

        #   Loop through the list of parameters
        for i in cp_par:

            #   Generate the CPPN
            cp_c = cppns.cppn(i[0], a[0][1], i[2], i[3], i[4], i[5], template.x_e - 2*template.b, template.y_e - 2*template.b)

            #   Save the specific CPPN model
            cp_i = cppns.cppn_i(cp_c, i[1])

            #   Add the CPPN model to the list
            cp.append(cp_i)

            #   Obtain the list of elements to be removed
            rem.append(cppns.cppn_rem(template, cp_i.grid))

        #   Save the list of units
        lu = numpy.array([rem, cp]).T.tolist()

    else:

        #   Generate the random parameters
        r_par = gen_alg.gen_par(n, 2, a[0], a[1])

        #   Loop through the list of parameters
        for i in r_par:

            #   Add the list of elements to be removed
            rem.append(utility.sel_random(template.e_internal, f = i[1], seed = i[0]))

        #   Save the list of units
        lu = numpy.array([rem, r_par]).T.tolist()

    return lu

################################################################################

def gen_bred_units(
    template,
    meth: str,
    par: list,
    c_mod_max: int = None,
    ) -> list:
    """Generate a bred population of units

    Parameters
    ----------
    template
        The unit template parameters
    meth : str
        The unit generation method
        l:  L-Systems
        c:  CPPNs
        r:  Random
    par : list
        The list of unit parameters
    c_mod_max : int, optional
        The maximum number of CPPN models per network, by default None

    Returns
    -------
    list
        The population
    """    

    #   Initialisations
    rem = []

    #   Check if the generation method is specified as L-Systems
    if meth == "l":

        #   Initialisations
        ls = []

        #   Loop through the list of parameters
        for i in par:

            #   Create the current L-System instance
            ls_i = lsystems.gen_lsystem(i[0], lsystems.e_vocabulary, i[1], i[2], i[3], i[4])

            #   Add the L-System instance to the list
            ls.append(ls_i)

            #   Obtain the list of elements to be removed
            rem.append(lsystems.interpret_word(template, ls_i.word))

        #   Save the list of units
        lu = numpy.array([rem, ls]).T.tolist()

    #   Check if the generation method is specified as CPPNs
    elif meth == "c":

        #   Initialisations
        cp = []

        #   Loop through the list of parameters
        for i in par:

            #   Generate the CPPN
            cp_c = cppns.cppn(i[0], c_mod_max, i[2], i[3], i[4], i[5], template.x_e - 2*template.b, template.y_e - 2*template.b)

            #   Save the specific CPPN model
            cp_i = cppns.cppn_i(cp_c, i[0])

            #   Add the CPPN model to the list
            cp.append(cp_i)

            #   Obtain the list of elements to be removed
            rem.append(cppns.cppn_rem(template, cp_i.grid))

        #   Save the list of units
        lu = numpy.array([rem, cp]).T.tolist()

    else:

        #   Loop through the list of parameters
        for i in par:

            #   Add the list of elements to be removed
            rem.append(utility.sel_random(template.e_internal, f = i[1], seed = i[0]))

        #   Save the list of units
        lu = numpy.array([rem, par]).T.tolist()

    return lu

################################################################################

def run_units(
    template,
    l_u: list,
    meth: str,
    ) -> [str, str]:

    #   The time the unit generation starts as a string label
    t = time.strftime("_%Y-%m-%d--%H-%M-%S", time.gmtime())
    print("Yes")

    #   Create the file path of the log file of units created during the simulation
    fp_lu = create_fp_file(template, t, "l")
    fp_lu_rank = create_fp_file(template, t + "_ranked", "l")
    print("Yes")

    for i in l_u:

        #   Open the template file
        modify.open_model(template.fp_t_mud)
        print("Yes")

        #   Generate the grid with elements removed, search for any free element clusters, and update the grid and list
        grid_rem, rem = gen_grid_rem_free(template, i[0])
        print("Yes")

        if meth == "l":

            #   Remove the elements, save and run the model and obtain the desired results
            rem_el_run_results(template, rem, grid_rem, fp_lu, ls = i[1])
            print("Yes")

        elif meth == "c":

            #   Remove the elements, save and run the model and obtain the desired results
            rem_el_run_results(template, rem, grid_rem, fp_lu, cp = i[1])

        else:

            #   Remove the elements, save and run the model and obtain the desired results
            rem_el_run_results(template, rem, grid_rem, fp_lu)

    return fp_lu, fp_lu_rank

################################################################################

def gen_grid_rem_free(
    template,
    rem: list,
    ) -> [list, list]:
    """Generate the representative grid with the desired elements removed, search for any free-floating element clusters, add them to the list of elements to be removed and update the representative grid

    Parameters
    ----------
    template : template
        The unit template parameters
    rem : list
        The list of elements to be removed

    Returns
    -------
    [list, list]
        The representative grid and the updated list of elements to be removed
    """    

    #   Remove the elements from the representative grid
    grid_rem = rep_grid.rem_el_grid(template, rem)

    #   Search for clusters
    (found_free, grid_label) = rep_grid.find_cluster(grid_rem)

    #   Check if free clusters were found
    if found_free:

        #   Remove the free clusters
        (grid_rem, rem_free) = rep_grid.rem_el_free_grid(template, grid_label)

        #   Update the list of removed elements
        rem = utility.add_sort_list(rem, rem_free)

    return grid_rem, rem

################################################################################

def rem_el_run_results(
    template,
    rem: list,
    grid_rem: list,
    fp_lu: str,
    ls: int = None,
    cp: list = None,
    ) -> None:
    """Remove the elements from the unit model, save and run the model, obtain the desired results from the model and reopen the template model

    Parameters
    ----------
    template : template
        The unit template parameters
    rem : list
        The list of elements to be removed
    grid_rem : list
        The representative grid with the elements removed
    fp_lu : str
        The file path of the log file of the list of all units generated
    ls : int, optional
        The L-system rule length, by default None
    cp : list, optional
        The CPPN parameters, by default None
    """    

    #   Save the current unit parameters
    curr_mod = classes.unit_p(template, rem, grid_rem, ls = ls, cp = cp)

    #   Remove the elements from the unit
    modify.rem_el(rem)

    #   Add the internal pressure boundary conditions
    modify.add_bc_p_internal(curr_mod)

    modify.copy_neighbours(template)

    modify.add_lcase(template, 2, template_bc_ip)
    modify.add_job(2, template_bc_ip)

    #   Save the altered unit
    modify.save_model(curr_mod.fp_u_mud)

    #   Run the model
    curr_mod.run_success = modify.run_model(template, 2, curr_mod.u_id, curr_mod.fp_u_mud, curr_mod.fp_u_log[1], curr_mod.fp_u_t16[1], template.d)

    #   Check if the model run was successful
    if curr_mod.run_success:

        #   Obtain the constraint and internal energies of the current model
        curr_mod.c_e = obtain.read_xym(template, curr_mod.u_id, "Constraint Energy")
        curr_mod.i_e = obtain.read_xym(template, curr_mod.u_id, "Internal Energy")

    #   Log the current unit parameters
    print(curr_mod, file = open(curr_mod.fp_u_l, "w"))
    utility.save_v(curr_mod, curr_mod.u_id)

    #   Log the current unit ID
    print(curr_mod.u_id, file = open(fp_lu, "a"))

    #   Reopen the template
    modify.open_model(template.fp_t_mud)

    return

################################################################################

def temp_create(template) -> list:
    """Create a template from which elements may be removed

    Case:   1
    Pure strain in the y-direction
    Case:   2
    Pure shear strain
    Case:   3
    Elongation of one side

    Parameters
    ----------
    template : template
        The unit template parameters
    """

    #   Clear the workspace
    py_send("*new_model yes")

    #   Construct the grid
    modify.create_nodes(template)
    modify.create_elements(template)

    #   Add the application graph
    modify.add_ramp(template)

    if template.case == 1:
        template_1_bc(template)
    elif template.case == 2:
        template_2_bc(template)
    else:
        template_3_bc(template)

    #   Check if neighbouring grids are required
    if template.neighbours == True:

        #   Add neighbouring grids
        modify.add_neighbours(template)

    #   Add template properties
    modify.add_geom_prop()
    modify.add_mat_ogden(template.ogd_mat)
    modify.add_contact_body()

    #   Add the loadcase
    modify.add_lcase(template, 1, template_bc_fd[template.case - 1])

    #   Add the job
    modify.add_job(1, template_bc_fd[template.case - 1])
    modify.save_model(template.fp_t_mud)

    #   Run the model
    template.run_success = modify.run_model(template, 1, template.t_id, template.fp_t_mud, template.fp_t_log, template.fp_t_t16)

    #   Check if the model run was successful
    if template.run_success:

        template.d = analyse.disp(template, template.t_id + "_1")

        #   Obtain the constraint energy of the current model
        template.c_e = obtain.read_xym(template, template.t_id, "Constraint Energy")
        template.i_e = obtain.read_xym(template, template.t_id, "Internal Energy")

    #   Save the template
    modify.save_model(template.fp_t_mud)

    #   Log the template parameters
    print(template, file = open(template.fp_t_l, "w"))
    utility.save_v(template, template.t_id)

    return

################################################################################

def template_1_bc(template) -> None:

    #   Add the boundary conditions
    modify.add_bc_fd_edge("yy1", "",               "y", "y", template.y0,  0)
    modify.add_bc_fd_edge("yy2", template.tab_nam, "y", "y", template.y_s, template.apply[0])
    modify.add_bc_fd_edge("xx1", "",               "x", "x", template.x0,  0)
    modify.add_bc_fd_edge("xx2", "",               "x", "x", template.x_s, 0)

    return

################################################################################

def template_2_bc(template) -> None:

    #   Add the boundary conditions
    modify.add_bc_fd_edge("xy1", "",               "x", "y", template.y0,  0)
    modify.add_bc_fd_edge("xy2", template.tab_nam, "x", "y", template.y_s, template.apply[0])
    modify.add_bc_fd_edge("yx1", "",               "y", "x", template.x0,  0)
    modify.add_bc_fd_edge("yx2", "",               "y", "x", template.x_s, 0)

    return

################################################################################

def template_3_bc(template) -> None:

    #   Add the boundary conditions
    modify.add_bc_fd_edge("yy1", "",               "y", "y", template.y0,  0)
    modify.add_bc_fd_edge("yy2", "",               "y", "y", template.y_s, 0)
    modify.add_bc_fd_node("xf1", "",               "x", 1,            0)
    modify.add_bc_fd_node("xf2", "",               "x", template.x_n, 0)
    modify.add_bc_fd_node("xn",  template.tab_nam, "x", template.n_n - template.x_n + 1, -template.apply[0])
    modify.add_bc_fd_node("xp",  template.tab_nam, "x", template.n_n, template.apply[0])

    return

# ################################################################################

# def template_1_test(fp_lu_rank: str) -> None:
#     """Test the best units for case 1

#     Parameters
#     ----------
#     fp_lu_rank : str
#         The file path of the list of best units
#     """    

#     #   Store the list of best units
#     bu = obtain.read_lu(fp_lu_rank)

#     #   Loop through the list of best units
#     for i in bu:

#         #   Open the current unit parameter class object
#         curr_mod = utility.open_v(i)

#         #   Open the current unit model
#         modify.open_model(curr_mod.fp_u_mud)

#         #   Add the internal pressure boundary conditions
#         modify.add_bc_p_internal(curr_mod)

#         #   Add the loadcase for the internal pressure
#         modify.add_lcase(curr_mod.template, 2, ["bc_load_yp", "bc_load_xn", "bc_load_yn", "bc_load_xp"])

#         #   Add the job for the second loadcase
#         modify.add_job(2)

#         #   Save the unit
#         modify.save_model(curr_mod.fp_u_mud)

#         #   Run the unit
#         curr_mod.run_success = modify.run_model(curr_mod.template, 2, curr_mod.u_id, curr_mod.fp_u_mud, curr_mod.fp_u_log[1], curr_mod.fp_u_t16[1])

#         #   Add the loadcase for all bouondary conditions
#         modify.add_lcase(curr_mod.template, 2, ["bc_fd_yy1", "bc_fd_yy2", "bc_fd_xx1", "bc_fd_xx2", "bc_load_yp", "bc_load_xn", "bc_load_yn", "bc_load_xp"])

#         #   Add the job for the third loadcase
#         modify.add_job(3)

#         #   Save the unit
#         modify.save_model(curr_mod.fp_u_mud)

#         #   Run the unit
#         curr_mod.run_success = modify.run_model(curr_mod.template, 3, curr_mod.u_id, curr_mod.fp_u_mud, curr_mod.fp_u_log[2], curr_mod.fp_u_t16[2])

#     return

# ################################################################################

# def template_2_test(fp_lu_rank: str) -> None:
#     """Test the best units for case 2

#     Parameters
#     ----------
#     fp_lu_rank : str
#         The file path of the list of best units
#     """    

#     #   Store the list of best units
#     bu = obtain.read_lu(fp_lu_rank)

#     #   Loop through the list of best units
#     for i in bu:

#         #   Open the current unit parameter class object
#         curr_mod = utility.open_v(i)

#         #   Open the current unit model
#         modify.open_model(curr_mod.fp_u_mud)

#         #   Add the internal pressure boundary conditions
#         modify.add_bc_p_internal(curr_mod)

#         #   Add the loadcase for the internal pressure
#         modify.add_lcase(curr_mod.template, 2, ["bc_load_yp", "bc_load_xn", "bc_load_yn", "bc_load_xp"])

#         #   Add the job for the second loadcase
#         modify.add_job(2)

#         #   Save the unit
#         modify.save_model(curr_mod.fp_u_mud)

#         #   Run the unit
#         curr_mod.run_success = modify.run_model(curr_mod.template, 2, curr_mod.u_id, curr_mod.fp_u_mud, curr_mod.fp_u_log[1], curr_mod.fp_u_t16[1])

#         #   Add the loadcase for all bouondary conditions
#         modify.add_lcase(curr_mod.template, 2, ["bc_fd_xy1", "bc_fd_xy2", "bc_fd_yx1", "bc_fd_yx2", "bc_load_yp", "bc_load_xn", "bc_load_yn", "bc_load_xp"])

#         #   Add the job for the third loadcase
#         modify.add_job(3)

#         #   Save the unit
#         modify.save_model(curr_mod.fp_u_mud)

#         #   Run the unit
#         curr_mod.run_success = modify.run_model(curr_mod.template, 3, curr_mod.u_id, curr_mod.fp_u_mud, curr_mod.fp_u_log[2], curr_mod.fp_u_t16[2])

#     return

# ################################################################################

# def template_4(template) -> None:
#     """Create a template from which elements may be removed

#     Case:   4
#     Reshape to a circle of a specified radius

#     Parameters
#     ----------
#     template : template
#         The unit template parameters
#     """

#     bc = []

#     #   Apply the initial template conditions
#     temp_pre(template)

#     #   Add the boundary conditions
#     x, y = inspect.find_n_coord(template.n_external)
#     x = utility.normalise_list(x, -1, f = template.x_s/2)
#     y = utility.normalise_list(y, -1, f = template.y_s/2)
#     x, y = utility.square_to_circle(x, y)
#     # x = [i*template.x_n/2 for i in x]
#     # y = [i*template.y_n/2 for i in y]

#     for i in range(0, len(template.n_external)):

#         modify.add_bc_fd_node("x{}".format(i), template.tab_nam, "x", template.n_external[i], x[i])
#         modify.add_bc_fd_node("y{}".format(i), template.tab_nam, "y", template.n_external[i], y[i])

#         bc.append("bc_fd_x{}".format(i))
#         bc.append("bc_fd_y{}".format(i))

#     #   Apply template conditions
#     pre_temp_mid(template)

#     modify.add_lcase(template, 1, bc)

#     #   Apply the final template conditions
#     temp_pos(template)

#     return

################################################################################

template_bc_fd = [
    ["bc_fd_yy1", "bc_fd_yy2", "bc_fd_xx1", "bc_fd_xx2"],
    ["bc_fd_xy1", "bc_fd_xy2", "bc_fd_yx1", "bc_fd_yx2"],
    ["bc_fd_yy1", "bc_fd_yy2", "bc_fd_xf1", "bc_fd_xf2", "bc_fd_xn", "bc_fd_xp"],
    ]

template_bc_ip = ["bc_load_yp", "bc_load_xn", "bc_load_yn", "bc_load_xp"]