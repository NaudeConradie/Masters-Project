##  Functions used with the Marc Mentat units

#   Imports
import time

from py_mentat import py_send

from evolve_soft_2d import utility
from evolve_soft_2d.classes import unit_p
from evolve_soft_2d.unit import inspect, modify, rep_grid
from evolve_soft_2d.result import analyse, obtain
from evolve_soft_2d.file_paths import create_fp_file

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
    template : template
        The unit template parameters
    n : int
        The number of units to generate
    f : int, optional
        The fixed amount of elements to remove, by default 0
    r : list, optional
        The range of elements which may be removed, by default []

    Returns
    -------
    str
        The file path of the log file of units generated
    """

    #   Initialisations
    all_u_id = []

    #   Check if a range of elements has been specified
    if r != []:

        #   Ensure no out-of-bounds or repeated values are in the range
        r = utility.clean_list(r, len(template.e_internal))

    #   Check if a fixed number of elements has been specified
    elif f != 0:

        #   Ensure the number is not out-of-bends
        f = utility.clean_int(f, len(template.e_internal))

    #   The time the unit generation starts as a string label
    t = time.strftime("_%Y-%m-%d--%H-%M-%S", time.gmtime())

    #   Create the file path of the log file of units created during the simulation
    fp_lu = create_fp_file(template, t, "l")

    #   Determine the maximum number of unique combinations of internal elements removed
    max_n = utility.nCr(len(template.e_internal), r = f, l = r)

    #   Check if the number of units requested is greater than the number of unique combinations
    if n > max_n:

        #   Set the number of units to be generated to the maximum number of unique combinations
        n = max_n

    #   Loop through the desired number of units to be created
    for _ in range(0, n):

        #   Initialisations
        exists = True

        #   Loop until a new unit ID is generated
        while exists:

            #   Obtain the list of element IDs to be removed
            rem = utility.sel_random(template.e_internal, f = f, r = r)

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

        #   Run the model
        curr_mod.run_success = modify.run_model(curr_mod.template, curr_mod.u_id)

        #   Check if the model run was successful
        if curr_mod.run_success:

            #   Obtain the constraint and internal energies of the current model
            curr_mod.c_e = obtain.read_val(template, "Constraint Energy_" + curr_mod.u_id)
            curr_mod.i_e = obtain.read_val(template, "Internal Energy_" + curr_mod.u_id)

        #   Log the current unit parameters
        print(curr_mod, file = open(curr_mod.fp_u_l, "w"))

        #   Log the current unit ID
        print(curr_mod.u_id, file = open(fp_lu, "a"))
        all_u_id.append(curr_mod.u_id)

        #   Reopen the template
        modify.open_model(template.fp_t_mud)
    
    return fp_lu

################################################################################

def template_1(template) -> None:
    """Create a template from which elements may be removed

    Case:   1
    Elongation in one direction while maintaining width in the other direction

    Parameters
    ----------
    template 
        The unit template parameters
    """

    #   Initialisations
    l = str(template.case) + "_" + template.n_e_l

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

    #   Check if the model run was successful
    if template.run_success:

        #   Obtain the constraint energy of the current model
        template.c_e = obtain.read_val(template, "Constraint Energy_" + l)
        template.i_e = obtain.read_val(template, "Internal Energy_" + l)

    #   Save the template
    modify.save_model(template.fp_t_mud)

    #   Log the template parameters
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
        obtain.all_val(template, l, template.fp_t_t16)
        analyse.constraint_energy(template, l)

    #   Obtain the constraint energy of the current model
    template.c_e = obtain.read_val(template, l)

    #   Save the template
    modify.save_model(template.fp_t_mud)

    print(template, file = open(template.fp_t_l, "w"))

    return