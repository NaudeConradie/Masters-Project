##  Classes used by functions

#   Imports
import time

from evolve_soft_2d import utility
from evolve_soft_2d.unit import inspect, rep_grid
from evolve_soft_2d.file_paths import create_fp_u_f, create_fp_t_f, create_fp_t_l

################################################################################

#   Ogden material model

class ogd_mat:

    def __init__(self, name, mu, alpha) -> None:
        """Material parameters

        Parameters
        ----------
        name : str
            The name of the material
        mu : list
            The mu parameters
        alpha : list
            The exponent parameters
        """

        self.name = name
        self.mu = mu
        self.alpha = alpha

    def __repr__(self) -> str:
        """Format a representation of the material model

        Returns
        -------
        str
            Formatted representation of the Ogden material class for the log
        """

        r_nam = "Name:  {}\n".format(self.name)
        r_mu =  "Mu:    {}\n".format(self.mu)
        r_alp = "Alpha: {}".format(self.alpha)
        return r_nam + r_mu + r_alp

################################################################################

#   Unit template parameters

class template:
    
    def __init__(
        self, 
        case,
        x0,
        y0,
        x_n,
        y_n,
        ogd_mat,
        n_steps,
        tab_nam,
        apply,
    ) -> None:
        """Unit template parameters

        Parameters
        ----------
        case : int
            The unit template case identifier
        x0 : int
            The initial x-coordinate
        y0 : int
            The initial y-coordinate
        x_n : int
            The number of nodes in the x-direction
        y_n : int
            The number of nodes in the y-direction
        ogd_mat : class
            The Ogden material model
        n_steps : int
            The number of steps in the second of the simulation
        tab_nam : str
            The name of the table containing the function of the load to be applied
        apply : int
            The conditions to be applied to the unit template
        """

        self.case = case
        self.x0 = x0
        self.y0 = y0
        self.x_n = x_n
        self.y_n = y_n
        self.ogd_mat = ogd_mat
        self.n_steps = n_steps
        self.tab_nam = tab_nam
        self.apply = apply

        #   The total number of nodes
        self.n_n = self.x_n * self.y_n
        #   The number of elements in the x-direction
        self.x_e = self.x_n - 1
        #   The number of elements in the y-direction
        self.y_e = self.y_n - 1
        #   The total number of elements
        self.n_e = self.x_e * self.y_e
        #   The total number of elements as a string label
        self.n_e_l = utility.list_to_str([self.x_e, self.y_e], "x")
        #   The list of internal elements
        self.e_internal = inspect.find_e_internal(self.x_e, self.y_e)
        #   The list of external nodes
        self.n_external = inspect.find_n_external(self.x_n, self.y_n)

        #   The representative grid of ones
        self.grid = rep_grid.create_grid(self.x_e, self.y_e)

        #   The file path of the template file
        self.fp_t_f = create_fp_t_f(self)
        #   The file path of the template file log
        self.fp_t_l = create_fp_t_l(self)

    def __repr__(self) -> str:
        """Format a representation of the template

        Returns
        -------
        str
            Formatted representation of the template class for the log
        """        
        r_cas = "Case: {}\nParameters:\n".format(self.case)
        r_ori = "Origin:            ({},{})\n".format(self.x0, self.y0)
        r_dim = "Dimensions:        {} elements\n".format(self.n_e_l)
        r_int = "Internal elements: {}\n".format(self.e_internal)
        r_ste = "Analysis steps:    {}\n".format(self.n_steps)
        r_ogd = "Ogden material parameters:\n{}\n".format(self.ogd_mat)
        r_tim = "Time created:      {}".format(time.ctime())
        return r_cas + r_ori + r_dim + r_int + r_ste + r_ogd + r_tim

################################################################################

#   Unit parameters

class unit_p:

    def __init__(self, template, rem, grid, run_success = False) -> None:
        """The unit parameters

        Parameters
        ----------
        template : class
            The unit template parameters
        rem : list
            The list of elements removed from the unit
        grid : list
            The representative grid with the elements removed
        run_success : bool, optional
            The success of the unit's run, by default False
        """

        self.template = template
        self.rem = rem
        self.grid = grid
        self.run_success = run_success

        #   The list of elements removed from the unit as a string
        self.rem_l = utility.list_to_str(rem, "_")

        #   The unique unit hash ID
        self.u_id = utility.gen_hash(self.rem_l)

        #   The representative grid with the elements removed as a string label
        self.grid_l = self.format_grid()

        #   The file path of the unit file
        self.fp_u_mud = create_fp_u_f(self, ".mud")
        #   The file path of the unit log file
        self.fp_u_log = create_fp_u_f(self, "_job.log")
        #   The file path of the unit t16 file
        self.fp_u_t16 = create_fp_u_f(self, "_job.t16") 
        #   The file path of the unit file log
        self.fp_u_l = create_fp_u_f(self, ".log")
        
    def __repr__(self) -> str:
        """Format a representation of the unit

        Returns
        -------
        str
            Formatted representation of the unit class for the log
        """        
        r_mod = "Unit:             {}\n".format(self.u_id)
        r_rem = "Removed elements:  {}\n".format(self.rem)
        r_gri = "Representative grid:\n{}\n".format(self.grid_l)
        r_run = "Run successful:    {}\n".format(self.run_success)
        r_tem = "Template details:\n{}".format(self.template)
        return r_mod + r_rem + r_gri + r_run + r_tem

    def format_grid(self) -> str:
        """Function to format the representative grid for the log

        Returns
        -------
        str
            The representative grid of the unit as a string
        """
        
        self.grid_l = rep_grid.create_grid(self.template.x_e, self.template.y_e)

        for i in range(0, len(self.grid)):
            self.grid_l[i] = " ".join(map(str, self.grid[i]))
        
        self.grid_l = "\n".join(map(str, self.grid_l))
        
        return self.grid_l

################################################################################

#   Example material models

mold_star_15 = ogd_mat("Mold Star 15", [-6.50266e-06, 0.216863, 0.00137158], [-21.322, 1.1797, 4.88396])

ecoflex_0030 = ogd_mat("Ecoflex 0030", [-0.0142909, -3.64558e-06, 9.59447e-08], [-5.22444, -0.162804, 11.3772])

smooth_sil_950 = ogd_mat("Smooth Sil 950", [-0.30622, 0.0283304, 6.5963e-09], [-3.0594, 4.59654, 17.6852])