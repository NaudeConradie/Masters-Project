##  Functions used with the Marc Mentat units

#   Imports
import time

from py_mentat import py_send

from evolve_soft_2d import classes, utility
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
    fp_bu = create_fp_file(template, t + "_selected", "l")

    #   Determine the maximum number of unique combinations of internal elements removed
    max_n = utility.nCr(len(template.e_internal), r = f, l = r)

    #   Check if the number of units requested is greater than the number of unique combinations
    if n > max_n:

        #   Set the number of units to be generated to the maximum number of unique combinations
        n = max_n

    modify.open_model(template.fp_t_mud)

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
        curr_mod = classes.unit_p(template, rem, grid_rem)

        #   Save the altered unit
        modify.save_model(curr_mod.fp_u_mud)

        #   Run the model
        curr_mod.run_success = modify.run_model(curr_mod.template, 1, curr_mod.u_id, curr_mod.fp_u_mud, curr_mod.fp_u_log[0], curr_mod.fp_u_t16[0])

        #   Check if the model run was successful
        if curr_mod.run_success:

            #   Obtain the constraint and internal energies of the current model
            curr_mod.c_e = obtain.read_val(template, "Constraint Energy_" + curr_mod.u_id + "_1")
            curr_mod.i_e = obtain.read_val(template, "Internal Energy_" + curr_mod.u_id + "_1")

        #   Log the current unit parameters
        print(curr_mod, file = open(curr_mod.fp_u_l, "w"))
        utility.save_v(curr_mod, curr_mod.u_id)

        #   Log the current unit ID
        print(curr_mod.u_id, file = open(fp_lu, "a"))
        all_u_id.append(curr_mod.u_id)

        #   Reopen the template
        modify.open_model(template.fp_t_mud)
    
    return fp_lu, fp_bu

################################################################################

def template_1(template) -> None:
    """Create a template from which elements may be removed

    Case:   1
    Pure strain in the y-direction

    Parameters
    ----------
    template : template
        The unit template parameters
    """

    #   Clear the workspace
    py_send("*new_model yes")

    #   Grid construction
    modify.create_nodes(template)
    modify.create_elements(template)

    #   Add template properties
    modify.add_ramp(template)
    modify.add_bc_fd_edge("yy1", "",               "y", "y", template.y0,  0)
    modify.add_bc_fd_edge("yy2", template.tab_nam, "y", "y", template.y_s, template.apply[0])
    modify.add_bc_fd_edge("xx1", "",               "x", "x", template.x0,  0)
    modify.add_bc_fd_edge("xx2", "",               "x", "x", template.x_s, 0)
    modify.add_geom_prop()
    modify.add_mat_ogden(template.ogd_mat)
    modify.add_contact_body()
    modify.add_lcase(template, 1, ["bc_fd_yy1", "bc_fd_yy2", "bc_fd_xx1", "bc_fd_xx2"])

    #   Add the job
    modify.add_job(1)
    modify.save_model(template.fp_t_mud)

    #   Run the model
    template.run_success = modify.run_model(template, 1, template.t_id, template.fp_t_mud, template.fp_t_log, template.fp_t_t16)

    #   Check if the model run was successful
    if template.run_success:

        #   Obtain the constraint energy of the current model
        template.c_e = obtain.read_val(template, "Constraint Energy_" + template.t_id + "_1")
        template.i_e = obtain.read_val(template, "Internal Energy_" + template.t_id + "_1")

    #   Save the template
    modify.save_model(template.fp_t_mud)

    #   Log the template parameters
    print(template, file = open(template.fp_t_l, "w"))
    utility.save_v(template, template.t_id)

    return

################################################################################

def template_1_test(fp_bu: str) -> None:
    """Test the best units for case 1

    Parameters
    ----------
    fp_bu : str
        The file path of the list of best units
    """    

    #   Store the list of best units
    bu = obtain.read_lu(fp_bu)

    #   Loop through the list of best units
    for i in bu:

        #   Open the current unit parameter class object
        curr_mod = utility.open_v(i)

        #   Open the current unit model
        modify.open_model(curr_mod.fp_u_mud)

        #   Add the internal pressure boundary conditions
        modify.add_bc_p_internal(curr_mod)

        #   Add the loadcase for the internal pressure
        modify.add_lcase(curr_mod.template, 2, ["bc_load_yp", "bc_load_xn", "bc_load_yn", "bc_load_xp"])

        #   Add the job for the second loadcase
        modify.add_job(2)

        #   Save the unit
        modify.save_model(curr_mod.fp_u_mud)

        #   Run the unit
        curr_mod.run_success = modify.run_model(curr_mod.template, 2, curr_mod.u_id, curr_mod.fp_u_mud, curr_mod.fp_u_log[1], curr_mod.fp_u_t16[1])

        #   Add the loadcase for all bouondary conditions
        modify.add_lcase(curr_mod.template, 2, ["bc_fd_yy1", "bc_fd_yy2", "bc_fd_xx1", "bc_fd_xx2", "bc_load_yp", "bc_load_xn", "bc_load_yn", "bc_load_xp"])

        #   Add the job for the third loadcase
        modify.add_job(3)

        #   Save the unit
        modify.save_model(curr_mod.fp_u_mud)

        #   Run the unit
        curr_mod.run_success = modify.run_model(curr_mod.template, 3, curr_mod.u_id, curr_mod.fp_u_mud, curr_mod.fp_u_log[2], curr_mod.fp_u_t16[2])

    return

################################################################################

def template_2(template) -> None:
    """Create a template from which elements may be removed

    Case:   2
    Pure shear strain

    Parameters
    ----------
    template : template
        The unit template parameters
    """

    #   Clear the workspace
    py_send("*new_model yes")

    #   Grid construction
    modify.create_nodes(template)
    modify.create_elements(template)

    #   Add template properties
    modify.add_ramp(template)
    modify.add_bc_fd_edge("xy1", "",               "x", "y", template.y0,  0)
    modify.add_bc_fd_edge("xy2", template.tab_nam, "x", "y", template.y_s, template.apply[0])
    modify.add_bc_fd_edge("yx1", "",               "y", "x", template.x0,  0)
    modify.add_bc_fd_edge("yx2", "",               "y", "x", template.x_s, 0)
    modify.add_geom_prop()
    modify.add_mat_ogden(template.ogd_mat)
    modify.add_contact_body()
    modify.add_lcase(template, 1, ["bc_fd_xy1", "bc_fd_xy2", "bc_fd_yx1", "bc_fd_yx2"])

     #   Add the job
    modify.add_job(1)
    modify.save_model(template.fp_t_mud)

    #   Run the model
    template.run_success = modify.run_model(template, 1, template.t_id, template.fp_t_mud, template.fp_t_log, template.fp_t_t16)

    #   Check if the model run was successful
    if template.run_success:

        #   Obtain the constraint energy of the current model
        template.c_e = obtain.read_val(template, "Constraint Energy_" + template.t_id + "_1")
        template.i_e = obtain.read_val(template, "Internal Energy_" + template.t_id + "_1")

    #   Save the template
    modify.save_model(template.fp_t_mud)

    print(template, file = open(template.fp_t_l, "w"))
    utility.save_v(template, template.t_id)

    return

################################################################################

def neighbours(template) -> None:
    """Create a template from which elements may be removed

    Case:   1
    Pure strain in the y-direction

    Parameters
    ----------
    template : template
        The unit template parameters
    """

    modify.open_model(template.fp_t_mud)

    x = [-template.x_s, template.x0, template.x_s]
    y = [-template.y_s, template.y0, template.y_s]

    x_mid = template.x0
    y_mid = template.y0

    n = 1

    for i in y:

        for j in x:

            if i == y_mid and j == x_mid:

                # n += 1

                continue

            template.x0 = j
            template.y0 = i

            n_init = n*template.n_n + 1

            n += 1

            #   Grid construction
            modify.create_nodes(template)
            modify.create_elements(template, n_init = n_init)

    # #   Add the job
    # modify.add_job(1)
    # modify.save_model(template.fp_t_mud)

    # #   Run the model
    # template.run_success = modify.run_model(template, 1, template.t_id, template.fp_t_mud, template.fp_t_log, template.fp_t_t16)

    # #   Check if the model run was successful
    # if template.run_success:

    #     #   Obtain the constraint energy of the current model
    #     template.c_e = obtain.read_val(template, "Constraint Energy_" + template.t_id + "_1")
    #     template.i_e = obtain.read_val(template, "Internal Energy_" + template.t_id + "_1")

    #   Save the template
    modify.save_model(template.fp_t_mud)

    # #   Log the template parameters
    # print(template, file = open(template.fp_t_l, "w"))
    # utility.save_v(template, template.t_id)

    return