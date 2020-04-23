##  Test program

#   Imports
from evolve_soft_2d.model import modify, create
from evolve_soft_2d import file_paths

def main():
    #   Initialisations
    #   Text name of the table used for the applied load
    table_name = "sin_input"
    #   Number of nodes per axis (one more than number of elements desired)
    x_n = 6
    y_n = 6
    #   Coordinates of initial position
    x0 = 0
    y0 = 0
    #   Number of increments per second to analyse
    n_steps = 4
    #   Magnitude of the applied load and/or displacement
    #   p_mag = 25
    d_mag = 1

    #   Flag to be set if the base model needs to be regenerated
    regen_base = False

    case = "0"

    #   Prepare the model parameters
    (n_n, x_e, y_e, n_e_l, fp_t_id, exists) = create.prep_template(x_n, y_n, case)

    print(fp_t_id)

    #   Open the base file if it exists
    if exists and not regen_base:
        modify.open_model(fp_t_id, n_e_l + '_' + case)

