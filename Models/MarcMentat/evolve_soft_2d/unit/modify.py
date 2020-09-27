##  Functions used with the Marc Mentat units

#   Imports
from evolve_soft_2d import utility
from evolve_soft_2d.log import m_log
from evolve_soft_2d.result import analyse, obtain

from py_mentat import py_send, py_get_int, py_get_float

import time

################################################################################

def open_model(fp_id: str) -> None:
    """Open a model

    Parameters
    ----------
    fp_id : str
        The complete file path of the model to be opened
    """

    py_send(r'*open_model "{}"'.format(fp_id))

    return

################################################################################

def save_model(fp_id: str) -> None:
    """Save a model

    Parameters
    ----------
    fp_id : str
        The complete file path of the model to be saved
    """

    py_send("*set_save_formatted off")
    py_send(r'*save_as_model "{}" yes'.format(fp_id))

    return

################################################################################

def create_nodes(template) -> None:
    """Create a 2D node grid on the xy-plane

    Parameters
    ----------
    template 
        The unit template parameters
    """

    #   Initialisations
    y = template.y0
    z = 0

    #   Loop through the nodes in the y-direction
    for _ in range(0, template.y_n):

        #   Initialise the x-coordinate
        x = template.x0

        #   Loop through the nodes in the x-direction
        for _ in range(0, template.x_n):
            
            #   Add the node
            py_send("*add_nodes {} {} {}".format(x, y, z))

            #   Increment the x-coordinate
            x = x + template.e_s

        #   Increment the y-coordinate
        y = y + template.e_s

    return

################################################################################
 
def create_elements(
    template,
    n_init: int = 1,
    ) -> None:
    """Create an element grid on the node grid

    Parameters
    ----------
    template 
        The unit template parameters
    n_init : int, optional
        The initial node number, by default 1
    """

    #   Loop through the elements in the y-direction
    for i in range(1, template.y_n):

        #   Initialise the nodal coordinates
        n1 = (i - 1)*template.x_n + n_init
        n2 = n1 + 1
        n3 = n2 + template.x_n
        n4 = n1 + template.x_n

        #   Loop through the elements in the x-direction
        for _ in range(1, template.x_n):

            #   Add the element
            py_send("*add_elements {} {} {} {}".format(n1, n2, n3, n4))

            #   Increment the nodal coordinates
            n1 = n1 + 1
            n2 = n2 + 1
            n3 = n3 + 1
            n4 = n4 + 1

    return

################################################################################

def add_neighbours(template) -> None:
    """Add solid neighbouring grids

    Parameters
    ----------
    template
        The unit template parameters
    """    

    #   Initialisations
    x = [-template.x_s, template.x0, template.x_s]
    y = [-template.y_s, template.y0, template.y_s]

    x_mid = template.x0
    y_mid = template.y0

    n = 1

    #   Loop through all y-axis initial coordinates
    for i in y:

        #   Loop through all x-axis initial coordinates
        for j in x:

            #   Check if the starting coordinates are the original grid's
            if i == y_mid and j == x_mid:

                #   Skip this step in the loop
                continue

            #   Set the initial coordinates of the template
            template.x0 = j
            template.y0 = i

            #   Set the initial node ID
            n_init = n*template.n_n + 1
                        
            #   Construct the neighbouring grid
            create_nodes(template)
            create_elements(template, n_init = n_init)

            #   Increment the counter
            n += 1

    #   Merge overlapping nodes
    sweep()

    return

################################################################################

def copy_neighbours(template) -> None:
    """Surround the current grid with copies of itself

    Parameters
    ----------
    template
        The unit template parameters
    """

    #   Initialisations
    x = [-template.x_s, template.x0, template.x_s]
    y = [-template.y_s, template.y0, template.y_s]

    x_mid = template.x0
    y_mid = template.y0

    n_l = ["n:{}".format(i) for i in range(1, template.n_n + 1)]
    e_l = ["e:{}".format(i) for i in range(1, template.n_e + 1)]

    n_l = utility.list_to_str(n_l, " ")
    e_l = utility.list_to_str(e_l, " ")

    l = utility.list_to_str([n_l, e_l], " ")

    #   Loop through all y-axis initial coordinates
    for i in y:

        #   Loop through all x-axis initial coordinates
        for j in x:

            #   Check if the starting coordinates are the original grid's
            if i == y_mid and j == x_mid:

                #   Skip this step in the loop
                continue

            #   Set the origin coordinates of the copy
            py_send("*set_duplicate_translation x {}".format(j))
            py_send("*set_duplicate_translation y {}".format(i))

            #   Copy the grid
            py_send("*duplicate_combined")
            py_send("{} #".format(l))

    #   Clear all duplicate nodes
    sweep()

    return

################################################################################
 
def add_ramp(template) -> None:
    """Add a ramp to a table

    Parameters
    ----------
    template 
        The unit template parameters
    """

    py_send("*new_md_table 1 1")
    py_send("*table_name \"{}\"".format(template.tab_nam))
    py_send("*set_md_table_type 1 \"time\"")
    py_send("*set_md_table_step_v 1 100")
    py_send("*set_md_table_step_f 1 100")
    py_send("*set_md_table_method_formula")

    #   The ramp function is defined according to y = x
    py_send("*md_table_formula v1")

    return

################################################################################
    
def add_bc_fd_edge(
    label: str,
    tab_nam: str,
    a: str,
    d: str,
    e: int,
    m: float,
    ) -> None:
    """Add fixed displacement boundary conditions along an entire edge

    Parameters
    ----------
    label : str
        The label of the boundary condition
    tab_nam : str
        The name of the table defining the displacement function if applicable
    a : str
        The axis of the applied boundary condition
        "x" or "y"
    d : str
        The direction of the applied boundary condition
        "x" or "y"
    e : int
        The edge coordinate of the boundary condition
    m : float
        The magnitude of the applied displacement
    """

    #   Initialisation
    n_l = []

    #   Fetch the total number of nodes
    n_n = py_get_int("nnodes()")

    #   Apply the fixed boundary condition
    py_send("*new_apply")
    py_send("*apply_type fixed_displacement")
    py_send("*apply_name bc_fd_{}".format(label))
    py_send("*apply_dof {}".format(a))
    py_send("*apply_dof_value {} {}".format(a, m))
    
    #   Apply the displacement function if applicable
    if tab_nam != "":
        py_send("*apply_dof_table {} {}".format(a, tab_nam))

    #   Loop through the number of nodes
    for i in range(1, n_n + 1):

        #   Fetch the relevant coordinate of the current node
        c_n = py_get_float("node_{}({})".format(d, i))

        #   Check if the selected coordinate matches the desired edge
        if c_n == e:

            #   Add the node to the list
            n_l.append(i)

    #   Apply the boundary condition to the selected nodes
    py_send("*add_apply_nodes ")

    #   Loop through the selected nodes
    for i in n_l:
        py_send("{} ".format(i))

    py_send("#")

    return

################################################################################

def add_bc_fd_node(
    label: str,
    tab_nam: str,
    a: str,
    n: int,
    d: float,
    ) -> None:
    """Add fixed displacement boundary conditions on a single node

    Parameters
    ----------
    label : str
        The label of the boundary condition
    tab_nam : str
        The name of the table defining the displacement function if applicable
    a : str
        The axis of the boundary condition
        "x" or "y"
    n : int
        The node number of the boundary condition
    d : float
        The magnitude of the applied displacement
    """

    #   Apply the fixed boundary condition
    py_send("*new_apply")
    py_send("*apply_type fixed_displacement")
    py_send("*apply_name bc_fd_{}".format(label))
    py_send("*apply_dof {}".format(a))
    py_send("*apply_dof_value {} {}".format(a, d))
    
    #   Apply the displacement function if applicable
    if tab_nam != "":
        py_send("*apply_dof_table {} {}".format(a, tab_nam))

    #   Apply the boundary condition to the selected nodes
    py_send("*add_apply_nodes {} #".format(n))

    return

################################################################################

def add_bc_fr_node(
    label: str,
    tab_nam: str,
    a: str,
    n: int,
    d: float,
    ) -> None:
    """Add fixed rotation boundary conditions on a single node

    Parameters
    ----------
    label : str
        The label of the boundary condition
    tab_nam : str
        The name of the table defining the displacement function if applicable
    a : str
        The axis of the boundary condition
        "x" or "y"
    n : int
        The node number of the boundary condition
    d : float
        The magnitude of the applied displacement
    """

    #   Apply the fixed rotation boundary condition
    py_send("*new_apply")
    py_send("*apply_type fixed_displacement")
    py_send("*apply_name bc_fr_{}".format(label))
    py_send("*apply_dof r{}".format(a))
    py_send("*apply_dof_value r{} {}".format(a, d))
    
    #   Apply the displacement function if applicable
    if tab_nam != "":
        py_send("*apply_dof_table r{} {}".format(a, tab_nam))

    #   Apply the boundary condition to the selected nodes
    py_send("*add_apply_nodes {} #".format(n))

    return

################################################################################

def add_bc_p_internal(unit_p) -> None:
    """Add pressure boundary conditions to all internal edges

    Parameters
    ----------
    unit_p : unit_p
        The unit parameters class object
    """

    #   Initialisations
    label = []
    label.append("yp")
    label.append("xn")
    label.append("yn")
    label.append("xp")

    #   Find all internal edges
    ip_e = obtain.internal_edges(unit_p)

    #   Loop through all primary directions
    for i in range(0, 4):

        #   Add the pressure boundary condition in the current direction
        add_bc_p_edge(label[i], unit_p.template.apply[1], unit_p.template.tab_nam, i, ip_e[i])

    return

################################################################################

def add_bc_p_edge(
    label: str,
    p: float, 
    tab_nam: str, 
    d: int,
    e: list,
    ) -> None:
    """Add a pressure boundary condition to a list of elements in a given direction

    Parameters
    ----------
    label : str
        The label of the boundary condition
    p : float
        The magnitude of the pressure
    tab_nam : str
        The name of the table defining the pressure function
    d : int
        The direction of the applied pressure
        0, 1, 2 or 3
    e : list
        The list of elements
    """

    py_send("*new_apply")
    py_send("*apply_type edge_load")
    py_send("*apply_name bc_load_{}".format(label))

    #   Apply a pressure with the given magnitude and table
    py_send("*apply_dof p")
    py_send("*apply_dof_value p {}".format(p))
    py_send("*apply_dof_table p {}".format(tab_nam))
        
    #   Apply the load to the correct edges
    py_send("*add_apply_edges ")

    #   Loop through all elements
    for i in e:

        #   Add the appropriate edge
        py_send("{}:{} ".format(i, d))

    py_send("#")

    return

################################################################################

def add_inertia_rel() -> None:
    """Add inertia relief
    """    

    py_send("*loadcase_option inertia_relief:on")

    #   Loop through the degrees of freedom
    for i in range(1, 7):

        #   Check if the current degree of freedom is translation in the z-direction
        if i == 3:

            #   Skip this step in the loop
            continue

        py_send("*set_loadcase_inert_rlf_supp_dof_def {}".format(i))

    #   Add node 1 as the support node
    py_send("*add_loadcase_inert_rlf_supp_nodes 1 #")

    return

################################################################################

def add_geom_prop() -> None:
    """Add plane strain geometrical properties
    """

    py_send("*geometry_type mech_planar_pstrain")
    py_send("*add_geometry_elements all_existing")

    return

################################################################################
  
def add_mat_ogden(ogd_mat) -> None:
    """Add an Ogden material model

    Parameters
    ----------
    ogd_mat : ogd_mat
        The Ogden material model
    """

    py_send("*new_mater standard")
    py_send("*mater_option general:state:solid")
    py_send("*mater_option general:skip_structural:off")
    py_send("*mater_name \"{}\"".format(ogd_mat.name))
    py_send("*mater_option structural:type:ogden")
    py_send("*mater_param structural:ogden_nterm 3")
    py_send("*mater_param structural:ogden_modulus_1 {}".format(ogd_mat.mu[0]))
    py_send("*mater_param structural:ogden_exp_1 {}".format(ogd_mat.alpha[0]))
    py_send("*mater_param structural:ogden_modulus_2 {}".format(ogd_mat.mu[1]))
    py_send("*mater_param structural:ogden_exp_2 {}".format(ogd_mat.alpha[1]))
    py_send("*mater_param structural:ogden_modulus_3 {}".format(ogd_mat.mu[2]))
    py_send("*mater_param structural:ogden_exp_3 {}".format(ogd_mat.alpha[2]))
    py_send("*add_mater_elements all_existing")

    return

################################################################################

def add_contact_body() -> None:
    """Add a contact body
    """

    py_send("*new_cbody mesh")
    py_send("*contact_option state:solid")
    py_send("*contact_option skip_structural:off")
    py_send("*add_contact_body_elements all_existing")
    
    return

################################################################################
 
def add_lcase(
    template,
    l_id: int,
    l_bc: list,
    ir: bool = False,
    ) -> None:
    """Add a loadcase

    Parameters
    ----------
    template
        The unit template parameters
    l_id : int
        The loadcase ID
    l_bc : list
        The list of loadcase boundary conditions
    ir : bool, optional
        Whether or not to include inertia relief, by default False
    """

    py_send("*new_loadcase")
    py_send("*loadcase_type struc:static")
    py_send("*loadcase_name lcase{}".format(l_id))
    py_send("*clear_loadcase_loads")

    #   Loop through the list of boundary conditions
    for i in l_bc:

        #   Add the boundary conditions
        py_send("*add_loadcase_loads {}".format(i))

    #   Check if inertia relief is required
    if ir == True:

        #   Add inertia relief
        add_inertia_rel()

    py_send("*loadcase_value nsteps {}".format(template.n_steps))

    return

################################################################################

def add_job(
    j_id: int,
    j_bc: list,
    ) -> None:
    """Add a job

    Parameters
    ----------
    j_id : int
        The job ID
    """

    py_send("*prog_use_current_job on")
    py_send("*new_job structural")
    py_send("*job_name job_{}".format(j_id))
    py_send("*add_job_loadcases lcase{}".format(j_id))
    py_send("*clear_job_applys")

    #   Loop through the list of boundary conditions
    for i in j_bc:

        #   Add the boundary conditions
        py_send("*add_job_applys {}".format(i))

    py_send("*job_option strain:large")
    py_send("*job_option follow:on")
    py_send("*add_post_tensor stress_g")
    py_send("*add_post_tensor strain")
    py_send("*add_post_var von_mises")
    py_send("*add_post_var te_energy")

    return

################################################################################

def run_job(j_id: int) -> None:
    """Run a job

    Parameters
    ----------
    j_id : int
        The job ID
    """

    t0 = time.time()

    py_send("*edit_job job_{}".format(j_id))
    py_send("*update_job")
    py_send("*submit_job 1") 
    py_send("*monitor_job")

    t1 = time.time()

    m_log.info("Job run in {:.3f}s".format(t1 - t0))

    return

################################################################################

def run_model(
    template,
    j_id: int,
    l: str,
    fp_mud: str,
    fp_log: str,
    fp_t16: str,
    d_temp: list = None,
    ) -> bool:
    """Run a model

    Parameters
    ----------
    template
        The unit template parameters
    j_id : int
        The job ID
    l : str
        The label of the model
    fp_mud : str
        The file path of the model file
    fp_log : str
        The file path of the model log file
    fp_t16 : str
        The file path of the model t16 file

    Returns
    -------
    bool
        The success of the run
    """

    #   Run the job
    run_job(j_id)

    #   Determine the existence of the results
    run_success = obtain.check_out(fp_mud, fp_log, fp_t16, j_id)

    #   Check if the run was a success
    if run_success:

        #   Obtain the results
        obtain.all_val(template, l + "_" + str(j_id), fp_t16)

        #   Analyse the results
        analyse.constraint_energy(template, l + "_" + str(j_id))
        analyse.internal_energy(template, l + "_" + str(j_id))

        if d_temp is not None:

            analyse.hausdorff_d(template, l + "_" + str(j_id))
        
    return run_success

################################################################################

def sweep() -> None:
    """Merge all overlapping nodes
    """

    py_send("*sweep_all")

    return

################################################################################

def rem_el(rem: list) -> None:
    """Remove a selection of elements

    Parameters
    ----------
    rem : list
        The list of selected elements to be removed
    """

    py_send("*remove_elements ")

    #   Loop through the number of elements to be removed
    for i in rem:

        #   Remove the element from the grid
        py_send("{} ".format(i))

    py_send("#")

    return

################################################################################

def rem_bc(bc: str) -> None:
    """Remove a selected boundary condition

    Parameters
    ----------
    bc : str
        The name of the boundary condition
    """    

    py_send("*edit_apply {}".format(bc))
    py_send("*remove_current_apply")

    return