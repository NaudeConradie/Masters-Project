##  Functions used with the Marc Mentat units

#   Imports
import linecache
import time

from evolve_soft_2d import utility
from evolve_soft_2d.classes import unit_p
from evolve_soft_2d.unit import inspect, modify, rep_grid
from evolve_soft_2d.result import analyse, obtain
from evolve_soft_2d.file_paths import fp_t, create_fp_file

from py_mentat import py_send
from scipy.special import comb

################################################################################
        
def gen_units(
    template,
    n: int,
    f: int = 0,
    r: list = [],
    ) -> str:
    """Generate multiple units

    Parameters
    ----------
    template 
        The unit template parameters
    n : int
        The number of units to generate
    f : int, optional
        The fixed amount of elements to remove, by default 0

    Returns
    -------
    str
        The file path of the log file of units created during the last simulation
    """

    #   Initialisations
    all_u_id = []
    max_n = 0

    #   The time the unit generation starts as a string label
    t = time.strftime("_%Y-%m-%d--%H-%M-%S", time.gmtime())

    #   Create the file path of the log file of units created during the simulation
    fp_lu = create_fp_file(template, t, "l")

    if r != []:

        r = prep_r(r, template.e_internal)

        for i in range(0, len(r)):

            max_n += comb(len(template.e_internal), r[i], exact = True)

    elif f != 0:

        f = prep_f(f, template.e_internal)

        max_n = comb(len(template.e_internal), f, exact = True)

    else:

        for i in range(0, len(template.e_internal)):

            max_n += comb(len(template.e_internal), i, exact = True)

    if n > max_n:

        n = max_n

    #   Loop through the desired number of units to be created
    for _ in range(0, n):

        #   Initialisations
        exists = True

        #   Loop until a new unit ID is generated
        while exists:

            if f == 0 and r == []:
                #   Determine which random elements will be removed
                rem = utility.sel_random(template.e_internal)
            elif r != []:
                rem = utility.sel_random_range(template.e_internal, r)
            else:
                rem = utility.sel_random_fixed(template.e_internal, f)

            grid_rem = rep_grid.rem_el_grid(template, rem)

            #   Search for clusters
            (found_free, grid_label) = rep_grid.find_cluster(grid_rem)

            #   Check if free clusters were found
            if found_free:

                #   Remove the free clusters
                (grid_rem, rem_free) = rep_grid.rem_el_free_grid(template, grid_label)

                #   Update the list of removed elements
                rem = utility.add_sort_list(rem, rem_free)

            #   Save the list of elements to be removed from the unit as a string
            rem_l = utility.list_to_str(rem, "_")

            #   Generate the unique unit hash ID
            u_id = utility.gen_hash(rem_l)

            #   Check if the unit ID is not in the list of unit IDs generated already
            if u_id not in all_u_id:

                exists = False

        #   Remove the elements from the unit
        modify.rem_el(rem)

        #   Save the current unit parameters
        curr_mod = unit_p(template, rem, grid_rem)

        #   Save the altered unit
        modify.save_model(curr_mod.fp_u_mud)

        #   Run the job 
        modify.run_job()

        #   Check the existence and validity of the results
        run_success = obtain.check_out(curr_mod.fp_u_mud, curr_mod.fp_u_log, curr_mod.fp_u_t16)
        curr_mod.run_success = run_success
        if run_success:

            #   Inspect the results
            obtain.all_n(curr_mod.template, curr_mod.u_id, curr_mod.fp_u_t16)
            analyse.constraint_energy(curr_mod.template, curr_mod.u_id)
            analyse.internal_energy(curr_mod.template, curr_mod.u_id)

        #   Obtain the constraint energy of the current model
        curr_mod.c_e = obtain.read_c_e(template, curr_mod.u_id)

        #   Log the current unit parameters
        print(curr_mod, file = open(curr_mod.fp_u_l, "w"))

        #   Log the current unit ID
        print(curr_mod.u_id, file = open(fp_lu, "a"))
        all_u_id.append(curr_mod.u_id)

        #   Reopen the template
        modify.open_model(template.fp_t_mud)
    
    return fp_lu

################################################################################

def prep_f(f: int, l: list) -> int:

    f_temp = f

    #   Check if the number of numbers to be removed is greater than the amount of numbers available
    if f > len(l):

        #   Set the number of numbers to be removed to one less than the number of numbers available
        f_temp = len(l)
    
    #   Check if the number of numbers to be removed is less than or equal to 0
    elif f <= 0:

        #   Set the number of numbers to be removed to one
        f_temp = 1

    return f_temp

################################################################################

def prep_r(r: list, l: list) -> list:
    """[summary]

    Parameters
    ----------
    r : list
        [description]

    Returns
    -------
    list
        [description]
    """
    r_temp = r[:]

    r_temp = [utility.replace(i, len(l)) for i in r_temp]

    r_temp = list(set(r_temp))
    
    return r_temp

################################################################################

def template_1(template) -> None:
    """Create a template from which elements may be removed

    Case:   1
    Elongation in the y-direction while maintaining width in the x-direction

    Parameters
    ----------
    template 
        The unit template parameters
    """

    #   Clear the workspace
    py_send("*new_model yes")

    #   Grid construction
    modify.create_nodes(template)
    modify.create_elements(template)

    #   Add template properties
    modify.add_ramp(template)
    modify.add_bc_fd_ee("y0", "",               "y", template.y0,  0)
    modify.add_bc_fd_ee("y1", template.tab_nam, "y", template.y_e, template.apply)
    modify.add_bc_fd_ee("x0", "",               "x", template.x0,  0)
    modify.add_bc_fd_ee("x1", "",               "x", template.x_e, 0)
    modify.add_geom_prop()
    modify.add_mat_ogden(template.ogd_mat)
    modify.add_contact_body()
    modify.add_lcase(template)

    #   Add the job
    modify.add_job()
    modify.save_model(template.fp_t_mud)
    modify.run_job()

    l = str(template.case) + "_" + template.n_e_l

    #   Check the existence and validity of the results
    run_success = obtain.check_out(template.fp_t_mud, template.fp_t_log, template.fp_t_t16)
    template.run_success = run_success
    if run_success:

        #   Inspect the results
        obtain.all_n(template, l, template.fp_t_t16)
        analyse.constraint_energy(template, l)
        analyse.internal_energy(template, l)

    #   Obtain the constraint energy of the current model
    template.c_e = obtain.read_c_e(template, l)

    #   Save the template
    modify.save_model(template.fp_t_mud)

    print(template, file = open(template.fp_t_l, "w"))

    return

################################################################################

def template_2(template) -> None:
    """Create a template from which elements may be removed

    Case:   2
    Elongation of one side while maintaining width

    Parameters
    ----------
    template 
        The unit template parameters
    """

    #   Clear the workspace
    py_send("*new_model yes")

    #   Grid construction
    modify.create_nodes(template)
    modify.create_elements(template)

    #   Add template properties
    modify.add_ramp(template)
    modify.add_bc_fd_ee("y0", "", "y", template.y0,  0)
    modify.add_bc_fd_ee("y1", "", "y", template.y_e, 0)
    modify.add_bc_fd_sn("x0", "", "x", 1,            0)
    modify.add_bc_fd_sn("x1", "", "x", template.x_n, 0)
    modify.add_bc_fd_sn("x2", template.tab_nam, "x", template.x_n*(template.y_n - 1) + 1, -template.apply)
    modify.add_bc_fd_sn("x3", template.tab_nam, "x", template.x_n*template.y_n, template.apply)
    modify.add_geom_prop()
    modify.add_mat_ogden(template.ogd_mat)
    modify.add_contact_body()
    modify.add_lcase(template)

     #   Add the job
    modify.add_job()
    modify.save_model(template.fp_t_mud)
    modify.run_job()

    l = str(template.case) + "_" + template.n_e_l

    #   Check the existence and validity of the results
    run_success = obtain.check_out(template.fp_t_mud, template.fp_t_log, template.fp_t_t16)
    template.run_success = run_success
    if run_success:

        #   Inspect the results
        obtain.all_n(template, l, template.fp_t_t16)
        analyse.constraint_energy(template, l)

    #   Obtain the constraint energy of the current model
    template.c_e = obtain.read_c_e(template, l)

    #   Save the template
    modify.save_model(template.fp_t_mud)

    print(template, file = open(template.fp_t_l, "w"))

    return