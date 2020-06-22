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

def create_fp_folder(
    template,
    p: str,
    ) -> str:
    """Create the file path of the results folder up to the template level

    Parameters
    ----------
    template : class
        The unit template parameters
    p : str
        The specific folder
        "r" - The results folder
        "t" - The unit template folder
        "u" - The unit folder
        
    Returns
    -------
    str
        The folder path
    """

    #   Generate the folder name according to the current case and template
    fp_folder = r'\grid_' + template.t_id

    #   Determine which folder path to generate the folder name along
    if p == "r":
        fp_folder = fp_r + fp_folder
    elif p == "t":
        fp_folder = fp_t + fp_folder
    elif p == "u":
        fp_folder = fp_u + fp_folder

    #   Create the folder if it does not exist
    utility.make_folder(fp_folder)

    return fp_folder

################################################################################

def create_fp_file(
    template,
    l: str,
    p: str,
    unit = None,
    ) -> str:
    """Create the file path of the desired file

    Parameters
    ----------
    template : class
        The unit template parameters
    l : str
        The unique label of the file
    p : str
        The specific file path
        "l" - The log file of units generated during the current run of the programme
        "r" - The results files
        "t" - The unit template files
        "u" - The unit files
    unit : class, optional
        The unit template parameters, by default None

    Returns
    -------
    str
        The file path
    """    
    
    #   Determine which folder path to generate the file name along
    if p == "l":
        fp_file = fp_u + r'\grid_' + template.t_id + l + ".log"
    elif p == "r":
        fp_folder = create_fp_folder(template, "r")
        fp_file = fp_folder + "\\" + l + ".csv"
    elif p == "t":
        fp_folder = create_fp_folder(template, "t")
        fp_file = fp_folder + r'\grid_' + template.t_id + l
    elif p == "u":
        fp_folder = create_fp_folder(template, "u")
        fp_file = fp_folder + r'\grid_' + unit.u_id

        #   Create the folder if it does not exist
        utility.make_folder(fp_file)
        
        fp_file = fp_file + r'\grid_' + unit.u_id + l

    return fp_file