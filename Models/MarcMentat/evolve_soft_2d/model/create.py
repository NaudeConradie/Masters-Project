##  Functions used with the Marc Mentat models

#   Imports
from evolve_soft_2d import result, utility
from evolve_soft_2d.model import modify, rep_grid
from evolve_soft_2d.file_paths import fp_t, create_fp_t_f, create_fp_m_f

from py_mentat import py_send

################################################################################

#   Prepare template parameters
#   Returns the number of nodes, the number of elements in the x- and y-direction, the number of elements as a string and whether or not such a template already exists

#   x_n:    The number of nodes in the x-direction
#   y_n:    The number of nodes in the y-direction
#   case:   The model case identifier
def prep_template(x_n, y_n, case):

    #   Calculate the number of nodes
    n_n = x_n*y_n

    #   Calculate the number of elements in the x- and y-direction
    x_e = x_n - 1
    y_e = y_n - 1

    #   Create a string with the number of elements in the x- and y-direction
    n_e_l = utility.list_to_str([x_e, y_e], "x")

    #   Create the file path of the template
    fp_t_f = create_fp_t_f(n_e_l, case)

    #   Check if the template exists
    exists = utility.if_file_exist(fp_t_f)

    return (n_n, x_e, y_e, n_e_l, fp_t_f, exists)

################################################################################

#   Create a template from which elements may be removed
#   Case:   0

#   x0:         The initial x-coordinate
#   y0:         The initial y-coordinate
#   x_n:        The number of nodes in the x-direction
#   y_n:        The number of nodes in the y-direction
#   y_e:        The number of elements in the y-direction
#   tab_name:   The name of the table
#   d:          The magnitude of the applied displacement
#   n_steps:    The number of steps in the second of the loadcase
#   n_e_l:      The number of elements as a string
#   fp_t_f:     The file path of the template model file
def template_0(x0, y0, x_n, y_n, y_e, tab_name, d, n_steps, n_e_l, fp_t_f):

    #   Clear the workspace
    py_send("*new_model yes")

    #   Grid construction
    modify.create_nodes(x0, y0, x_n, y_n)
    modify.create_elements(x_n, y_n)

    #   Add template properties
    modify.add_bc_fixed("y", "y", y0)
    modify.add_sin(tab_name)
    modify.add_bc_displacement("y", "y", d, tab_name, y_e)
    modify.add_geom_prop()
    modify.add_mat_mr()
    modify.add_contact_body()
    modify.add_lcase(n_steps)

    #   Save the template
    modify.save_model(fp_t_f, n_e_l + '_0')

    return

################################################################################

#   Generate multiple models

#   n_n:        The number of nodes
#   x_e:        The number of elements in the x-direction
#   y_e:        The number of elements in the y-direction
#   e_internal: The list of internal elements
#   n_steps:    The number of steps in the second of the loadcase
#   grid:       The representative grid of ones
#   n_e_l:      The number of elements as a string
#   case:       The model case identifier
#   fp_t_f:     The file path of the template model file
#   g:          The number of models to generate
def gen_models(n_n, x_e, y_e, e_internal, n_steps, grid, n_e_l, case, fp_t_f, g):

    #   Loop through the desired number of models to be created
    for _ in range(0, g):

        #   Determine which random elements will be removed
        rem = utility.sel_random(e_internal)
        modify.rem_el(rem)
        grid_rem = rep_grid.rem_el_grid(grid, x_e, rem)

        #   Search for cluster
        (found_free, grid_label) = rep_grid.find_cluster(grid_rem)

        #   Check if free clusters were found
        if found_free:

            #   Remove the free clusters
            (grid_rem, rem_free) = rep_grid.rem_el_free_grid(grid, grid_label, x_e, y_e)
            modify.rem_el(rem_free)

            #   Update the list of removed elements
            rem = utility.add_sort_list(rem, rem_free)

        #   Convert the list of removed elements to a string for file naming purposes
        rem_l = utility.list_to_str(rem, "_")
        m_id = utility.gen_hash(rem_l)

        #   Create the file path names of the model and relevant output files
        fp_m_mud = create_fp_m_f(n_e_l, case, m_id, '.mud')
        fp_m_log = create_fp_m_f(n_e_l, case, m_id, '_job.log')
        fp_m_t16 = create_fp_m_f(n_e_l, case, m_id, '_job.t16')

        #   Add the job
        modify.add_job()

        #   Save the altered model
        modify.save_model(fp_m_mud, m_id)

        #   Run the job 
        modify.run_job()

        #   Check the existence and validity of the results
        run_success = result.check_out(fp_m_mud, fp_m_log, fp_m_t16, m_id)
        if run_success:

            #   Inspect the results
            result.get_max_min(n_steps, n_e_l, case, m_id, fp_m_t16)
            result.get_all(n_n, n_steps, n_e_l, case, m_id, fp_m_t16)

        #   Reopen the template
        modify.open_model(fp_t_f, n_e_l + '_' + case)
    
    return