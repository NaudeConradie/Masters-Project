##  Functions used with the Marc Mentat models

#   Imports
import time

from evolve_soft_2d import utility
from evolve_soft_2d.classes import model
from evolve_soft_2d.model import inspect, modify, rep_grid
from evolve_soft_2d.result import analyse, obtain
from evolve_soft_2d.file_paths import fp_t, create_fp_t_f, create_fp_m_f, create_fp_m_m

from py_mentat import py_send

################################################################################

#   Generate multiple models

#   n_n:        The number of nodes
#   x_e:        The number of elements in the x-direction
#   y_e:        The number of elements in the y-direction
#   e_internal: The list of internal elements
#   n_external: The list of external nodes
#   n_steps:    The number of steps in the second of the loadcase
#   grid:       The representative grid of ones
#   n_e_l:      The number of elements as a string
#   case:       The model case identifier
#   fp_t_f:     The file path of the template model file
#   g:          The number of models to generate
def gen_models(template, n):

    t = time.strftime("_%Y-%m-%d--%H-%M-%S", time.gmtime())

    fp_m_m = create_fp_m_m(template.case, template.n_e_l, t)

    #   Loop through the desired number of models to be created
    for _ in range(0, n):

        #   Determine which random elements will be removed
        rem = utility.sel_random(template.e_internal)
        grid_rem = rep_grid.rem_el_grid(template.grid, template.x_e, rem)

        #   Search for cluster
        (found_free, grid_label) = rep_grid.find_cluster(grid_rem)

        #   Check if free clusters were found
        if found_free:

            #   Remove the free clusters
            (grid_rem, rem_free) = rep_grid.rem_el_free_grid(template.grid, grid_label, template.x_e, template.y_e)

            #   Update the list of removed elements
            rem = utility.add_sort_list(rem, rem_free)
            
        modify.rem_el(rem)

        curr_mod = model(template, rem, grid_rem)

        #   Add the job
        modify.add_job()

        #   Save the altered model
        modify.save_model(curr_mod.fp_m_mud, curr_mod.m_id)

        #   Run the job 
        modify.run_job()

        #   Check the existence and validity of the results
        run_success = obtain.check_out(curr_mod)
        curr_mod.run_success = run_success
        if run_success:

            #   Inspect the results
            obtain.max_min(curr_mod)
            obtain.all_n(curr_mod)
            analyse.boundary_energy(curr_mod)

        print(curr_mod, file = open(curr_mod.fp_m_l, "w"))
        print(curr_mod.m_id, file = open(fp_m_m, "a"))

        #   Reopen the template
        modify.open_model(template.fp_t_f, str(template.case) + "_" + template.n_e_l)
    
    return t

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
def template_0(template):

    #   Clear the workspace
    py_send("*new_model yes")

    #   Grid construction
    modify.create_nodes(template)
    modify.create_elements(template)

    #   Add template properties
    modify.add_ramp(template.tab_name)
    modify.add_bc_fd("y0", "y", 0, "", template.y0)
    modify.add_bc_fd("y1", "y", template.apply, template.tab_name, template.y_e)
    modify.add_geom_prop()
    modify.add_mat_ogden("MoldStar15")
    modify.add_contact_body()
    modify.add_lcase(template.n_steps)

    #   Save the template
    modify.save_model(template.fp_t_f, template.n_e_l + "_0")

    print(template, file = open(template.fp_t_l, "w"))

    return

################################################################################