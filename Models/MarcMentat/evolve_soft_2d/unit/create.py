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

################################################################################
        
def gen_units(template, n) -> str:
    """Generate multiple units

    Parameters
    ----------
    template : class
        The unit template parameters
    n : int
        The number of units to generate

    Returns
    -------
    str
        The file path of the log file of units created during the last simulation
    """

    #   Initialisations
    all_u_id = []

    #   The time the unit generation starts as a string label
    t = time.strftime("_%Y-%m-%d--%H-%M-%S", time.gmtime())

    #   Create the file path of the log file of units created during the simulation
    fp_lu = create_fp_file(template, t, "l")

    #   Loop through the desired number of units to be created
    for _ in range(0, n):

        #   Initialisations
        exists = True

        #   Loop until a new unit ID is generated
        while exists:

            #   Determine which random elements will be removed
            rem = utility.sel_random(template.e_internal)
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
            obtain.max_min(curr_mod.template, curr_mod.u_id, curr_mod.fp_u_t16)
            obtain.all_n(curr_mod.template, curr_mod.u_id, curr_mod.fp_u_t16)
            analyse.constraint_energy(curr_mod.template, curr_mod.u_id)

        #
        fp_r_f = create_fp_file(template, "Constraint Energy_" + curr_mod.u_id, "r")

        curr_mod.c_e = float(linecache.getline(fp_r_f, curr_mod.template.n_steps + 1))

        #   Log the current unit parameters
        print(curr_mod, file = open(curr_mod.fp_u_l, "w"))

        #   Log the current unit ID
        print(curr_mod.u_id, file = open(fp_lu, "a"))
        all_u_id.append(curr_mod.u_id)

        #   Reopen the template
        modify.open_model(template.fp_t_mud)
    
    return fp_lu

################################################################################

def template_0(template) -> None:
    """Create a template from which elements may be removed

    Case:   0
    Testing template

    Parameters
    ----------
    template : class
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
    modify.add_geom_prop()
    modify.add_mat_ogden(template.ogd_mat)
    modify.add_contact_body()
    modify.add_lcase(template)

    #   Save the template
    modify.save_model(template.fp_t_mud)

    print(template, file = open(template.fp_t_l, "w"))

    return

################################################################################

def template_1(template) -> None:
    """Create a template from which elements may be removed

    Case:   1
    Elongation in the y-direction while maintaining width in the x-direction

    Parameters
    ----------
    template : class
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

    #   Check the existence and validity of the results
    run_success = obtain.check_out(template.fp_t_mud, template.fp_t_log, template.fp_t_t16)
    template.run_success = run_success
    if run_success:

        #   Inspect the results
        obtain.all_n(template, str(template.case) + "_" + template.n_e_l, template.fp_t_t16)
        analyse.constraint_energy(template, str(template.case) + "_" + template.n_e_l)

    fp_r_f = create_fp_file(template, "Constraint Energy_" + str(template.case) + "_" + template.n_e_l, "r")

    template.c_e = float(linecache.getline(fp_r_f, template.n_steps + 1))

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
    template : class
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

    #   Save the template
    modify.save_model(template.fp_t_mud)

    print(template, file = open(template.fp_t_l, "w"))

    return