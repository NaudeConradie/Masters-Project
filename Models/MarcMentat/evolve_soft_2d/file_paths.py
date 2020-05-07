##  File paths

#   Imports
from evolve_soft_2d import utility

################################################################################

#   Fixed file paths
fp = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Units\MarcMentat'
fp_m = fp + r'\Units'
fp_r = fp + r'\Results'
fp_t = fp + r'\Templates'

################################################################################

#   Create the file path of the unit folder up to the template level

#   template:   The unit template parameters
def create_fp_m_id(template):

    fp_m_id = r'\grid_' + str(template.case) + "_" + template.n_e_l
    fp_m_id = fp_m + fp_m_id

    #   Returns the file path
    return fp_m_id

################################################################################

#   Create the file path of the log file of units created during the last simulation

#   template:   The unit template parameters
#   t:          The time the unit generation starts as a string label
def create_fp_m_m(template, t):

    fp_m_id = create_fp_m_id(template)
    fp_m_m = fp_m_id + t + ".log"

    #   Returns the file path
    return fp_m_m

################################################################################

#   Create the file path of unit files

#   unit:  The unit parameters
#   ext:    The extension of the file
def create_fp_m_f(unit, ext):

    fp_m_id = create_fp_m_id(unit.template)
    fp_m_f = r'\grid_' + unit.m_id

    #   Create the folder if it does not exist
    utility.make_folder(fp_m_id + fp_m_f)

    fp_m_f = fp_m_id + fp_m_f + fp_m_f + ext

    #   Returns the file path
    return fp_m_f

################################################################################

#   Create the file path of the results folder up to the template level

#   template:   The unit template parameters
def create_fp_r_id(template):

    fp_r_id = r'\grid_' + str(template.case) + "_" + template.n_e_l
    fp_r_id = fp_r + fp_r_id

    #   Create the folder if it does not exist
    utility.make_folder(fp_r_id)

    #   Returns the file path
    return fp_r_id

################################################################################

#   Create the file path of the results file

#   unit:  The unit parameters
#   t:      The type of data to be stored
def create_fp_r_f(unit, t):

    fp_r_id = create_fp_r_id(unit.template)
    fp_r_f = fp_r_id + "\\" + t + "_" + unit.m_id + ".csv"

    #   Returns the file path
    return fp_r_f

################################################################################

#   Create the file path of the results file during analysis

#   unit:  The unit parameters
#   t:      The type of data to be stored
def create_fp_r_f_da(template, t, m_id):

    fp_r_id = create_fp_r_id(template)
    fp_r_f = fp_r_id + "\\" + t + "_" + m_id + ".csv"

    #   Returns the file path
    return fp_r_f

################################################################################

#   Create the file path of the template folder up to the template level

#   template:   The unit template parameters
def create_fp_t_id(template):

    fp_t_id = r'\grid_' + str(template.case) + "_" + template.n_e_l
    fp_t_id = fp_t + fp_t_id

    #   Create the folder if it does not exist
    utility.make_folder(fp_t_id)

    #   Returns the file path
    return fp_t_id

################################################################################

#   Create the file path of the template file

#   template:   The unit template parameters
def create_fp_t_f(template):

    fp_t_id = create_fp_t_id(template)
    fp_t_f = fp_t_id + r'\grid_' + str(template.case) + "_" + template.n_e_l + ".mud"

    #   Returns the file path
    return fp_t_f

################################################################################

#   Create the file path of the template log

#   template:   The unit template parameters
def create_fp_t_l(template):

    fp_t_id = create_fp_t_id(template)
    fp_t_l = fp_t_id + r'\grid_' + str(template.case) + "_" + template.n_e_l + ".log"

    #   Returns the file path
    return fp_t_l