##  File paths

#   Imports
from evolve_soft_2d import utility

################################################################################

#   Fixed file paths
fp = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Models\MarcMentat'
fp_r = fp + r'\Results'
fp_t = fp + r'\Templates'
fp_u = fp + r'\Units'

################################################################################

def create_fp_r_id(template) -> str:
    """Create the file path of the results folder up to the template level

    Parameters
    ----------
    template : class
        The unit template parameters

    Returns
    -------
    str
        The file path
    """

    fp_r_id = r'\grid_' + str(template.case) + "_" + template.n_e_l
    fp_r_id = fp_r + fp_r_id

    #   Create the folder if it does not exist
    utility.make_folder(fp_r_id)

    return fp_r_id

################################################################################

def create_fp_r_f(unit, t) -> str:
    """Create the file path of the results file

    Parameters
    ----------
    unit : class
        The unit parameters
    t : str
        The type of data to be stored

    Returns
    -------
    str
        The file path
    """

    fp_r_id = create_fp_r_id(unit.template)
    fp_r_f = fp_r_id + "\\" + t + "_" + unit.u_id + ".csv"

    return fp_r_f

################################################################################

def create_fp_r_f_da(template, t, u_id) -> str:
    """Create the file path of the results file during analysis

    Parameters
    ----------
    template : class
        The unit template parameters
    t : str
        The type of data to be stored
    u_id : str
        The unit ID

    Returns
    -------
    str
        The file path
    """

    fp_r_id = create_fp_r_id(template)
    fp_r_f = fp_r_id + "\\" + t + "_" + u_id + ".csv"

    return fp_r_f

################################################################################

def create_fp_t_id(template) -> str:
    """Create the file path of the template folder up to the template level

    Parameters
    ----------
    template : class
        The unit template parameters

    Returns
    -------
    str
        The file path
    """

    fp_t_id = r'\grid_' + str(template.case) + "_" + template.n_e_l
    fp_t_id = fp_t + fp_t_id

    #   Create the folder if it does not exist
    utility.make_folder(fp_t_id)

    return fp_t_id

################################################################################

def create_fp_t_f(template) -> str:
    """Create the file path of the template file

    Parameters
    ----------
    template : class
        The unit template parameters

    Returns
    -------
    str
        The file path
    """

    fp_t_id = create_fp_t_id(template)
    fp_t_f = fp_t_id + r'\grid_' + str(template.case) + "_" + template.n_e_l + ".mud"

    return fp_t_f

################################################################################
 
def create_fp_t_l(template) -> str:
    """Create the file path of the template log

    Parameters
    ----------
    template : class
        The unit template parameters

    Returns
    -------
    str
        The file path
    """

    fp_t_id = create_fp_t_id(template)
    fp_t_l = fp_t_id + r'\grid_' + str(template.case) + "_" + template.n_e_l + ".log"

    return fp_t_l

################################################################################
 
def create_fp_u_id(template) -> str:
    """Create the file path of the unit folder up to the template level

    Parameters
    ----------
    template : class
        The unit template parameters

    Returns
    -------
    str
        The file path
    """

    fp_u_id = r'\grid_' + str(template.case) + "_" + template.n_e_l
    fp_u_id = fp_u + fp_u_id

    return fp_u_id

################################################################################
         
def create_fp_u_m(template, t) -> str:
    """Create the file path of the log file of units created during the last simulation

    Parameters
    ----------
    template : class
        The unit template parameters
    t : str
        The time the unit generation starts

    Returns
    -------
    str
        The file path
    """

    fp_u_id = create_fp_u_id(template)
    fp_u_m = fp_u_id + t + ".log"

    return fp_u_m

################################################################################

def create_fp_u_f(unit, ext) -> str:
    """Create the file path of unit files

    Parameters
    ----------
    unit : class
        The unit parameters
    ext : str
        The extension of the file

    Returns
    -------
    str
        The file path
    """

    fp_u_id = create_fp_u_id(unit.template)
    fp_u_f = r'\grid_' + unit.u_id

    #   Create the folder if it does not exist
    utility.make_folder(fp_u_id + fp_u_f)

    fp_u_f = fp_u_id + fp_u_f + fp_u_f + ext

    return fp_u_f