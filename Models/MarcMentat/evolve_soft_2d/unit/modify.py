##  Functions used with the Marc Mentat units

#   Imports
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
            x = x + 1

        #   Increment the y-coordinate
        y = y + 1

    return

################################################################################
 
def create_elements(template) -> None:
    """Create an element grid on the node grid

    Parameters
    ----------
    template 
        The unit template parameters
    """

    #   Loop through the elements in the y-direction
    for i in range(1, template.y_n):

        #   Initialise the nodal coordinates
        n1 = (i - 1)*template.x_n + 1
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
    
def add_bc_fd_ee(
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
    for i in range(0, len(n_l)):
        py_send("{} ".format(n_l[i]))

    py_send("#")

    return

################################################################################

def add_bc_fd_sn(
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
  
def add_load(
    label: str,
    p: float, 
    tab_nam: str, 
    x_e: int, 
    y_e: int, 
    axis: str, 
    direc: int, 
    coord: int,
    ) -> None:
    """Add a load along a specified axis in a specified direction

    Parameters
    ----------
    label : str
        The label of the load
    p : float
        The magnitude of the applied pressure
    tab_nam : str
        The name of the table defining the load function
    x_e : int
        The number of elements in the x-direction
    y_e : int
        The number of elements in the y-direction
    axis : str
        The axis of the load
        "x" or "y"
    direc : int
        The direction of the load with respect to the axis
        1 for positive and -1 for negative
    coord : int
        The axis coordinate of the load
    """

    py_send("*new_apply")
    py_send("*apply_type edge_load")
    py_send("*apply_name load_{}".format(label))

    #   Apply a pressure with the given magnitude and table
    py_send("*apply_dof p")
    py_send("*apply_dof_value p {}".format(p))
    py_send("*apply_dof_table p {}".format(tab_nam))

    #   Find the correct edges according to the specified axes and directions
    if (axis == "x") and (direc == -1):
        s = 1
        edges = [i*x_e - (x_e - coord) for i in range(1, y_e + 1)]
    elif (axis == "x") and (direc == 1):
        s = 3
        edges = [i*x_e - (x_e - coord) for i in range(1, y_e + 1)]
    elif (axis == "y") and (direc == -1):
        s = 2
        edges = [i + x_e*(coord - 1) for i in range(1, x_e + 1)]
    elif (axis == "y") and (direc == 1):
        s = 4
        edges = [i + x_e*(coord - 1) for i in range(1, x_e + 1)]
        
    #   Apply the load to the correct edges
    py_send("*add_apply_edges")

    if axis == "x":
        for i in range(0, y_e):
            py_send("{}:{} ".format(edges[i], s))
    elif axis == "y":
        for i in range(0, x_e):
            py_send("{}:{} ".format(edges[i], s))

    py_send("#")

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
 
def add_lcase(template) -> None:
    """Add a loadcase

    Parameters
    ----------
    template 
        The unit template parameters
    """

    py_send("*new_loadcase")
    py_send("*loadcase_type struc:static")
    py_send("*loadcase_value nsteps {}".format(template.n_steps))

    return

################################################################################

def add_job() -> None:
    """Add a job
    """

    py_send("*prog_use_current_job on")
    py_send("*new_job structural")
    py_send("*job_name job")
    py_send("*add_job_loadcases lcase1")
    py_send("*job_option strain:large")
    py_send("*job_option follow:on")
    py_send("*add_post_tensor stress_g")
    py_send("*add_post_tensor strain")
    py_send("*add_post_var von_mises")
    py_send("*add_post_var te_energy")

    return

################################################################################

def run_job() -> None:
    """Run a job
    """

    t0 = time.time()

    py_send("*update_job")
    py_send("*submit_job 1") 
    py_send("*monitor_job")

    t1 = time.time()

    m_log.info("Job run in {:.3f}s".format(t1 - t0))

    return

################################################################################

def run_model(
    template,
    l: str,
    fp_mud: str,
    fp_log: str,
    fp_t16: str,
    ) -> bool:
    """Run a model

    Parameters
    ----------
    template : template
        The unit template parameters
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
        True if the model run was successful, false otherwise
    """

    #   Run the job
    run_job()

    #   Determine the existence of the results
    run_success = obtain.check_out(fp_mud, fp_log, fp_t16)

    #   Check if the run was a success
    if run_success:

        #   Obtain the results
        obtain.all_val(template, l, fp_t16)

        #   Analyse the results
        analyse.constraint_energy(template, l)
        analyse.internal_energy(template, l)
        
    return run_success

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
    for i in range(0, len(rem)):

        #   Remove the element from the grid
        py_send("{} ".format(rem[i]))

    py_send("#")

    return