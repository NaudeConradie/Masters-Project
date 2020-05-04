##  File paths

#   Imports
from evolve_soft_2d import utility

#   File paths
fp = r'C:\Users\Naude Conradie\Desktop\Repository\Masters-Project\Models\MarcMentat'
fp_m = fp + r'\Models'
fp_r = fp + r'\Results'
fp_t = fp + r'\Templates'

################################################################################

#   Create the file path of the model folder up to the template level
#   Returns the file path

#   n_e_l:  The number of elements as a string
#   case:   The model case identifier
def create_fp_m_id(case, n_e_l):

    fp_m_id = r'\grid_' + str(case) + "_" + n_e_l
    fp_m_id = fp_m + fp_m_id

    return fp_m_id

################################################################################

#   Create the file path of the model file or output file
#   Returns the file path

#   n_e_l:  The number of elements as a string
#   case:   The model case identifier
#   m_id:   The model identifier
#   ext:    The extension of the file
def create_fp_m_m(case, n_e_l, t):

    #   Create the file path of the model and output file folder
    fp_m_id = create_fp_m_id(case, n_e_l)

    fp_m_m = fp_m_id + t + ".log"

    return fp_m_m

################################################################################

#   Create the file path of the model file or output file
#   Returns the file path

#   n_e_l:  The number of elements as a string
#   case:   The model case identifier
#   m_id:   The model identifier
#   ext:    The extension of the file
def create_fp_m_f(case, n_e_l, m_id, ext):

    #   Create the file path of the model and output file folder
    fp_m_id = create_fp_m_id(case, n_e_l)
    fp_m_f = r'\grid_' + m_id

    #   Create the folder if it does not exist
    utility.make_folder(fp_m_id + fp_m_f)

    fp_m_f = fp_m_id + fp_m_f + fp_m_f + ext

    return fp_m_f

################################################################################

#   Create the file path of the results folder up to the template level
#   Returns the file path

#   n_e_l:  The number of elements as a string
#   case:   The model case identifier
def create_fp_r_id(case, n_e_l):

    fp_r_id = r'\grid_' + str(case) + "_" + n_e_l
    fp_r_id = fp_r + fp_r_id

    #   Create the folder if it does not exist
    utility.make_folder(fp_r_id)

    return fp_r_id

################################################################################

#   Create the file path of the results file
#   Returns the file path

#   n_e_l:  The number of elements as a string
#   case:   The model case identifier
#   t:      The type of data to be stored
#   m_id:   The model identifier
def create_fp_r_f(case, n_e_l, t, m_id):

    #   Create the file path of the results file folder
    fp_r_id = create_fp_r_id(case, n_e_l)

    fp_r_f = fp_r_id + "\\" + t + "_" + m_id + ".csv"

    return fp_r_f

################################################################################

#   Create the file path of the template folder up to the template level
#   Returns the file path

#   n_e_l:  The number of elements as a string
#   case:   The model case identifier
def create_fp_t_id(case, n_e_l):

    fp_t_id = r'\grid_' + str(case) + "_" + n_e_l
    fp_t_id = fp_t + fp_t_id

    utility.make_folder(fp_t_id)

    return fp_t_id

################################################################################

#   Create the file path of the template file
#   Returns the file path

#   n_e_l:  The number of elements as a string
#   case:   The model case identifier
def create_fp_t_f(case, n_e_l):

    fp_t_id = create_fp_t_id(case, n_e_l)
    fp_t_f = fp_t_id + r'\grid_' + str(case) + "_" + n_e_l + ".mud"

    return fp_t_f

################################################################################

#   Create the file path of the template log
#   Returns the file path

#   n_e_l:  The number of elements as a string
#   case:   The model case identifier
def create_fp_t_l(case, n_e_l):

    fp_t_id = create_fp_t_id(case, n_e_l)
    fp_t_l = fp_t_id + r'\grid_' + str(case) + "_" + n_e_l + ".log"

    return fp_t_l