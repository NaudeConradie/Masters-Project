##  Functions used with the Marc Mentat units

#   Imports
import time

from py_mentat import py_send

from evolve_soft_2d import classes, utility
from evolve_soft_2d.evolve import cppns, lsystems
from evolve_soft_2d.unit import inspect, modify, rep_grid
from evolve_soft_2d.result import analyse, obtain
from evolve_soft_2d.file_paths import create_fp_file

################################################################################
        
def gen_units(
    template,
    n: int,
    l: int = 0,
    c: list = [],
    f: int = 0,
    r: list = [],
    ) -> [str, str]:
    """Generate multiple units

    Parameters
    ----------
    template : template
        The unit template parameters
    n : int
        The number of units to generate
    l : int, optional
        The length of L-system rules, by default 0
    c : list, optional
        The list of CPPN parameters, by default []
    f : int, optional
        The fixed amount of elements to remove, by default 0
    r : list, optional
        The range of elements which may be removed, by default []

    Returns
    -------
    [str, str]
        The file paths of the log files of all units generated and the best units generated
    """

    #   Initialisations
    all_u_id = []
    seed = 0

    #   Check if the L-System rule length is 0
    if l == 0:

        #   Check if the list of CPPN parameters is empty
        if c == []:

            #   Check if a range of elements has been specified
            if r != []:

                #   Ensure no out-of-bounds or repeated values are in the range
                r = utility.clean_list(r, len(template.e_internal))

            #   Check if a fixed number of elements has been specified
            elif f != 0:

                #   Ensure the number is not out-of-bounds
                f = utility.clean_int(f, len(template.e_internal))

        else:

            #   Ensure the rounding threshold is within bounds
            c[5] = utility.clean_int(c[5], 0.9)

    else:

        #   Calculate the number of iterations for the L-Systenm
        l_n = round(template.x_n/2 - template.b)

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

    #   Open the template file
    modify.open_model(template.fp_t_mud)

    #   Loop through the desired number of units to be created
    for _ in range(0, n):

        #   Initialisations
        exists = True
        ls = None
        cp = None
        
        #   Loop until a new unit ID is generated
        while exists:

            #   Increment the seed for the CPPN
            seed += 1

            #   Check if the length of the L-system rules is not 0
            if l != 0:

                #   Generate a random L-System
                ls = lsystems.gen_lsystem(lsystems.e_vocabulary, l, l_n)

                #   Obtain the list of elements to be removed
                rem = lsystems.interpret_word(template, ls.word)

            #   Check if the list of CPPN parameters is not empty
            elif c != []:

                #   Generate a random CPPN
                cp_n = cppns.cppn(c[0], c[1], c[2], template.x_e - 2*template.b, template.y_e - 2*template.b, c[3], c[4], seed, c[5])

                #   Save the CPPN model
                cp = cppns.cppn_i(cp_n, 0)

                #   Obtain the list of elements to be removed
                rem = cppns.cppn_rem(template, cp.grid)

            else:   

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
        curr_mod = classes.unit_p(template, rem, grid_rem, ls = ls, cp = cp)

        #   Save the altered unit
        modify.save_model(curr_mod.fp_u_mud)

        #   Run the model
        curr_mod.run_success = modify.run_model(curr_mod.template, 1, curr_mod.u_id, curr_mod.fp_u_mud, curr_mod.fp_u_log[0], curr_mod.fp_u_t16[0])

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
        all_u_id.append(u_id)

        #   Reopen the template
        modify.open_model(template.fp_t_mud)
    
    return fp_lu, fp_bu

################################################################################

def pre_temp_pre(template) -> None:
    """Apply the initial template properties

    Parameters
    ----------
    template
        The unit template parameters
    """

    #   Clear the workspace
    py_send("*new_model yes")

    #   Construct the grid
    modify.create_nodes(template)
    modify.create_elements(template)

    #   Add the application graph
    modify.add_ramp(template)

    return

################################################################################

def pre_temp_mid(template):
    """Apply template properties

    Parameters
    ----------
    template
        The unit template parameters
    """    

    #   Check if neighbouring grids are required
    if template.neighbours == True:

        #   Add neighbouring grids
        modify.add_neighbours(template)

    #   Add template properties
    modify.add_geom_prop()
    modify.add_mat_ogden(template.ogd_mat)
    modify.add_contact_body()

    return

################################################################################

def pre_temp_pos(template):
    """Apply the final template properties

    Parameters
    ----------
    template
        The unit template parameters
    """    

    #   Add the job
    modify.add_job(1)
    modify.save_model(template.fp_t_mud)

    #   Run the model
    template.run_success = modify.run_model(template, 1, template.t_id, template.fp_t_mud, template.fp_t_log, template.fp_t_t16)

    #   Check if the model run was successful
    if template.run_success:

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

def template_1(template) -> None:
    """Create a template from which elements may be removed

    Case:   1
    Pure strain in the y-direction

    Parameters
    ----------
    template : template
        The unit template parameters
    """

    #   Apply the initial template conditions
    pre_temp_pre(template)
    
    #   Add the boundary conditions
    modify.add_bc_fd_edge("yy1", "",               "y", "y", template.y0,  0)
    modify.add_bc_fd_edge("yy2", template.tab_nam, "y", "y", template.y_s, template.apply[0])
    modify.add_bc_fd_edge("xx1", "",               "x", "x", template.x0,  0)
    modify.add_bc_fd_edge("xx2", "",               "x", "x", template.x_s, 0)

    #   Apply template conditions
    pre_temp_mid(template)
    
    #   Add the loadcase
    modify.add_lcase(template, 1, ["bc_fd_yy1", "bc_fd_yy2", "bc_fd_xx1", "bc_fd_xx2"])

    #   Apply the final template conditions
    pre_temp_pos(template)

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

    #   Apply the initial template conditions
    pre_temp_pre(template)

    #   Add the boundary conditions
    modify.add_bc_fd_edge("xy1", "",               "x", "y", template.y0,  0)
    modify.add_bc_fd_edge("xy2", template.tab_nam, "x", "y", template.y_s, template.apply[0])
    modify.add_bc_fd_edge("yx1", "",               "y", "x", template.x0,  0)
    modify.add_bc_fd_edge("yx2", "",               "y", "x", template.x_s, 0)

    #   Apply template conditions
    pre_temp_mid(template)

    modify.add_lcase(template, 1, ["bc_fd_xy1", "bc_fd_xy2", "bc_fd_yx1", "bc_fd_yx2"])

    #   Apply the final template conditions
    pre_temp_pos(template)

    return

################################################################################

def template_2_test(fp_bu: str) -> None:
    """Test the best units for case 2

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
        modify.add_lcase(curr_mod.template, 2, ["bc_fd_xy1", "bc_fd_xy2", "bc_fd_yx1", "bc_fd_yx2", "bc_load_yp", "bc_load_xn", "bc_load_yn", "bc_load_xp"])

        #   Add the job for the third loadcase
        modify.add_job(3)

        #   Save the unit
        modify.save_model(curr_mod.fp_u_mud)

        #   Run the unit
        curr_mod.run_success = modify.run_model(curr_mod.template, 3, curr_mod.u_id, curr_mod.fp_u_mud, curr_mod.fp_u_log[2], curr_mod.fp_u_t16[2])

    return

################################################################################

def template_3(template) -> None:
    """Create a template from which elements may be removed

    Case:   3
    Elongation of one side

    Parameters
    ----------
    template : template
        The unit template parameters
    """

    #   Apply the initial template conditions
    pre_temp_pre(template)

    #   Add the boundary conditions
    modify.add_bc_fd_edge("yy1", "",               "y", "y", template.y0,  0)
    modify.add_bc_fd_edge("yy2", "",               "y", "y", template.y_s, 0)
    modify.add_bc_fd_node("xf1", "",               "x", 1,            0)
    modify.add_bc_fd_node("xf2", "",               "x", template.x_n, 0)
    modify.add_bc_fd_node("xn",  template.tab_nam, "x", template.n_n - template.x_n + 1, -template.apply[0])
    modify.add_bc_fd_node("xp",  template.tab_nam, "x", template.n_n, template.apply[0])

    #   Apply template conditions
    pre_temp_mid(template)

    modify.add_lcase(template, 1, ["bc_fd_yy1", "bc_fd_yy2", "bc_fd_xf1", "bc_fd_xf2", "bc_fd_xn", "bc_fd_xp"])

    #   Apply the final template conditions
    pre_temp_pos(template)

    return

################################################################################

def template_4(template) -> None:
    """Create a template from which elements may be removed

    Case:   4
    Reshape to a circle of a specified radius

    Parameters
    ----------
    template : template
        The unit template parameters
    """

    bc = []

    #   Apply the initial template conditions
    pre_temp_pre(template)

    #   Add the boundary conditions
    x, y = inspect.find_n_coord(template.n_external)
    x = utility.normalise_list(x, -1, f = template.x_s/2)
    y = utility.normalise_list(y, -1, f = template.y_s/2)
    x, y = utility.square_to_circle(x, y)
    # x = [i*template.x_n/2 for i in x]
    # y = [i*template.y_n/2 for i in y]

    for i in range(0, len(template.n_external)):

        modify.add_bc_fd_node("x{}".format(i), template.tab_nam, "x", template.n_external[i], x[i])
        modify.add_bc_fd_node("y{}".format(i), template.tab_nam, "y", template.n_external[i], y[i])

        bc.append("bc_fd_x{}".format(i))
        bc.append("bc_fd_y{}".format(i))

    #   Apply template conditions
    pre_temp_mid(template)

    modify.add_lcase(template, 1, bc)

    #   Apply the final template conditions
    pre_temp_pos(template)

    return