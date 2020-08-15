##  Classes used by functions

#   Imports
import time

from evolve_soft_2d import utility
from evolve_soft_2d.unit import inspect, rep_grid
from evolve_soft_2d.file_paths import create_fp_file

################################################################################

class ogd_mat:
    """Ogden material model
    """

    def __init__(
        self,
        name: str,
        mu: list,
        alpha: list,
        ) -> None:
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

        r = "Name:  {}\n".format(self.name)
        r += "Mu:    {}\n".format(self.mu)
        r += "Alpha: {}".format(self.alpha)
        return r

################################################################################

class template:
    """Unit template parameters
    """    
    
    def __init__(
        self, 
        case: int,
        x0: int,
        y0: int,
        x_e: int,
        y_e: int,
        x_s: float,
        y_s: float,
        b: int,
        ogd_mat: ogd_mat,
        n_steps: int,
        tab_nam: str,
        apply: list,
        neighbours: bool,
        run_success: bool = False,
        c_e: list = [0, 0, 0],
        i_e: list = [0, 0, 0],
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
        x_e : int
            The number of elements in the x-direction
        y_e : int
            The number of elements in the y-direction
        x_s : float
            The side length of the unit in the x-direction
        y_s : float
            The side length of the unit in the y-direction
        b : int
            The number of elements in the boundary of the unit
        ogd_mat : class
            The Ogden material model
        n_steps : int
            The number of steps in the second of the simulation
        tab_nam : str
            The name of the table containing the function of the load to be applied
        apply : list
            The conditions to be applied to the unit template
        neighbours : bool
            The decision to add neighbouring grids
        run_success : bool, optional
            The success of the unit template's run, by default False
        c_e : list, optional
            The constraint energy of the unit template, by default [0, 0, 0]
        i_e : list, optional
            The internal energy of the unit template, by default [0, 0, 0]
        """

        self.case = case
        self.x0 = x0
        self.y0 = y0

        if x_e % 2 == 0:
            self.x_e = x_e + 1
        else:
            self.x_e = x_e

        if y_e % 2 == 0:
            self.y_e = y_e + 1
        else:
            self.y_e = y_e    

        self.x_s = x_s
        self.y_s = y_s
        self.b = b
        self.ogd_mat = ogd_mat
        self.n_steps = n_steps
        self.tab_nam = tab_nam
        self.apply = apply
        self.neighbours = neighbours
        self.run_success = run_success
        self.c_e = c_e
        self.i_e = i_e

        #   The number of nodes in the x-direction
        self.x_n = self.x_e + 1
        #   The number of nodes in the y-direction
        self.y_n = self.y_e + 1
        #   The side length of an element in the x-direction
        self.x_e_s = self.x_s/self.x_e
        #   The side length of an element in the y-direction
        self.y_e_s = self.y_s/self.y_e
        #   The total number of elements
        self.n_e = self.x_e * self.y_e
        #   The total number of nodes
        self.n_n = self.x_n * self.y_n
        #   The list of internal elements
        self.e_internal = inspect.find_e_internal(self.x_e, self.y_e, self.b)
        #   The list of external nodes
        self.n_external = inspect.find_n_external(self.x_n, self.y_n)

        #   The total number of elements as a string label
        self.n_e_l = utility.list_to_str([self.x_e, self.y_e], "x")
        #   The size of the grid as a string label
        self.s_l = utility.list_to_str([self.x_s, self.y_s], "x")

        #   The template ID
        self.t_id = str(self.case) + "_" + self.n_e_l + "_" + self.s_l + "_" + str(self.b)

        #   The representative grid of ones
        self.grid = rep_grid.create_grid(self.x_e, self.y_e, 1)

        #   The file path of the template file
        self.fp_t_mud = create_fp_file(self, ".mud", "t")
        #   The file path of the template file log
        self.fp_t_log = create_fp_file(self, "_job_1.log", "t")
        #   The file path of the unit t16 file
        self.fp_t_t16 = create_fp_file(self, "_job_1.t16", "t")
        #   The file path of the template file log
        self.fp_t_l = create_fp_file(self, ".log", "t")

    def __repr__(self) -> str:
        """Format a representation of the template for the log

        Returns
        -------
        str
            Formatted representation of the template class for the log
        """

        r = "Case: {}\nParameters:\n".format(self.case)
        r += "Origin:               ({},{})\n".format(self.x0, self.y0)
        r += "Dimensions:           {} elements\n".format(self.n_e_l)
        r += "Size:                 {} mm\n".format(self.s_l)
        r += "Boundary thickness:   {} elements\n".format(self.b)
        r += "Internal element IDs: {}\n".format(self.e_internal)
        r += "Applied displacement: {} mm\nApplied pressure:     {} MPa\n".format(self.apply[0], self.apply[1])
        r += "Neighbours added:     {}\n".format(self.neighbours)
        r += "Analysis steps:       {}\n".format(self.n_steps)
        r += "Run successful:       {}\n".format(self.run_success)
        r += "Constraint energy:\nX        : {} J\nY        : {} J\nMagnitude: {} J\n".format(self.c_e[0], self.c_e[1], self.c_e[2])
        r += "Internal energy:\nX        : {} J\nY        : {} J\nMagnitude: {} J\n".format(self.i_e[0], self.i_e[1], self.i_e[2])
        r += "\nOgden material parameters:\n{}\n".format(self.ogd_mat)
        r += "\nTime created: {}".format(time.ctime())
        return r

################################################################################

class unit_p:
    """Unit parameters
    """    

    def __init__(
        self,
        template,
        rem: list,
        grid: list,
        ls = None,
        cp = None,
        run_success: bool = False,
        c_e: list = [0, 0, 0],
        i_e: list = [0, 0, 0],
        ) -> None:
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
        c_e : list, optional
            The constraint energy of the unit template, by default [0, 0, 0]
        i_e : list, optional
            The internal energy of the unit template, by default [0, 0, 0]
        """

        self.template = template
        self.rem = rem
        self.grid = grid
        self.ls = ls
        self.cp = cp
        self.run_success = run_success
        self.c_e = c_e
        self.i_e = i_e

        #   The list of elements removed from the unit as a string
        self.rem_l = utility.list_to_str(rem, "_")

        #   Generate the unique unit ID according to the method of unit generation
        if self.ls != None:

            self.u_id = str(len(self.rem)) + "_" + utility.list_to_str(self.ls.gramm, "_")

        elif self.cp != None:

            self.u_id = str(len(self.rem)) + "_" + str(self.cp.mod_id) + "_" + str(self.cp.cppn.n_n) + "_" + str(self.cp.cppn.hl_size) + "_" + str(self.cp.cppn.scale) + "_" + str(self.cp.cppn.af_n) + "_" + str(self.cp.cppn.seed) + "_" + str(self.cp.cppn.threshold)

        else:
            
            self.u_id = str(len(self.rem)) + "_" + utility.gen_hash(self.rem_l)

        #   The representative grid with the elements removed as a string label
        self.grid_l = self.format_grid()

        #   The file path of the unit file
        self.fp_u_mud = create_fp_file(self.template, ".mud", "u", self)
        #   The file path of the unit log file
        self.fp_u_log = self.create_fp_list("log")
        #   The file path of the unit t16 file
        self.fp_u_t16 = self.create_fp_list("t16")
        #   The file path of the unit file log
        self.fp_u_l = create_fp_file(self.template, ".log", "u", self)
        
    def __repr__(self) -> str:
        """Format a representation of the unit

        Returns
        -------
        str
            Formatted representation of the unit class for the log
        """        
        r = "Unit:             {}\n".format(self.u_id)
        r += "Removed elements: {}\n".format(self.rem)

        if self.ls != None:

            r += "{}\n".format(self.ls)

        elif self.cp != None:

            r += "{}\n".format(self.cp)

        r += "Representative grid:\n{}\n".format(self.grid_l)
        r += "Run successful:   {}\n".format(self.run_success)
        r += "Constraint energy:\nX        : {} J\nY        : {} J\nMagnitude: {} J\n".format(self.c_e[0], self.c_e[1], self.c_e[2])
        r += "Internal energy:\nX        : {} J\nY        : {} J\nMagnitude: {} J\n".format(self.i_e[0], self.i_e[1], self.i_e[2])
        r += "\nTemplate details:\n{}".format(self.template)
        return r

    def format_grid(self) -> str:
        """Function to format the representative grid for the log

        Returns
        -------
        str
            The representative grid of the unit as a string
        """
        
        grid_l = rep_grid.create_grid(self.template.x_e, self.template.y_e, 1)

        for i in range(0, len(self.grid)):
            grid_l[i] = " ".join(map(str, self.grid[i]))
        
        grid_l = "\n".join(map(str, grid_l))
        
        return grid_l

    def create_fp_list(
        self,
        ext: str,
        ) -> list:
        """Create a list of unit file paths

        Parameters
        ----------
        ext : str
            The extension to add to the file path

        Returns
        -------
        list
            The list of file paths
        """        

        fp_list = []

        for i in range(1, 4):

            fp_list.append(create_fp_file(self.template, "_job_{}.{}".format(i, ext), "u", self))

        return fp_list

################################################################################

#   Example material models

mold_star_15 = ogd_mat("Mold Star 15", [-6.50266e-06, 0.216863, 0.00137158], [-21.322, 1.1797, 4.88396])

ecoflex_0030 = ogd_mat("Ecoflex 0030", [-0.0142909, -3.64558e-06, 9.59447e-08], [-5.22444, -0.162804, 11.3772])

smooth_sil_950 = ogd_mat("Smooth Sil 950", [-0.30622, 0.0283304, 6.5963e-09], [-3.0594, 4.59654, 17.6852])