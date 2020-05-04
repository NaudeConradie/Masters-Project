##  Classes used by functions

#   Imports
from evolve_soft_2d import utility
from evolve_soft_2d.model import inspect, rep_grid
from evolve_soft_2d.file_paths import create_fp_t_f, create_fp_t_l, create_fp_m_f

import time

################################################################################

class mat:

    def __init__(self, name, mu, e):
        self.name = name
        self.mu = mu
        self.e = e

################################################################################

class template:

    def __init__(self, case, x0, y0, x_n, y_n, n_steps, tab_name, apply):
        self.case = case
        self.x0 = x0
        self.y0 = y0
        self.x_n = x_n
        self.y_n = y_n
        self.n_n = self.x_n * self.y_n
        self.x_e = self.x_n - 1
        self.y_e = self.y_n - 1
        self.n_e = self.x_e * self.y_e
        self.n_e_l = utility.list_to_str([self.x_e, self.y_e], "x")
        self.e_internal = inspect.find_e_internal(self.x_e, self.y_e)
        self.n_external = inspect.find_n_external(self.x_n, self.y_n)
        self.grid = rep_grid.create_grid(self.x_e, self.y_e)
        self.n_steps = n_steps
        self.tab_name = tab_name
        self.apply = apply
        self.fp_t_f = create_fp_t_f(self.case, self.n_e_l)
        self.fp_t_l = create_fp_t_l(self.case, self.n_e_l)

    def __repr__(self):
        r_cas = "Case: {}\nParameters:\n".format(self.case)
        r_ori = "Origin:            ({},{})\n".format(self.x0, self.y0)
        r_dim = "Dimensions:        {} elements\n".format(self.n_e_l)
        r_int = "Internal elements: {}\n".format(self.e_internal)
        r_ste = "Analysis steps:    {}\n".format(self.n_steps)
        r_tim = "Time created:      {}".format(time.ctime())
        return r_cas + r_ori + r_dim + r_int + r_ste + r_tim

################################################################################

class model:

    def __init__(self, template, rem, grid, run_success = False):
        self.template = template
        self.rem = rem
        self.rem_l = utility.list_to_str(rem, "_")
        self.m_id = utility.gen_hash(self.rem_l)
        self.fp_m_mud = create_fp_m_f(self.template.case, self.template.n_e_l, self.m_id, ".mud")
        self.fp_m_log = create_fp_m_f(self.template.case, self.template.n_e_l, self.m_id, "_job.log")
        self.fp_m_t16 = create_fp_m_f(self.template.case, self.template.n_e_l,self.m_id, "_job.t16")
        self.fp_m_l = create_fp_m_f(self.template.case, self.template.n_e_l, self.m_id, ".log")
        self.grid = grid[:]
        self.grid_p = self.print_grid()
        self.run_success = run_success

    def __repr__(self):
        r_mod = "Model:             {}\n".format(self.m_id)
        r_rem = "Removed elements:  {}\n".format(self.rem)
        r_gri = "Representative grid:\n{}\n".format(self.grid_p)
        r_run = "Run successful:    {}\n".format(self.run_success)
        r_tem = "Template details:\n{}".format(self.template)
        return r_mod + r_rem + r_gri + r_run + r_tem

    def print_grid(self):
        self.grid_p = [[1]*(self.template.x_e) for i in range(self.template.y_e)]
        for i in range(0, len(self.grid)):
            self.grid_p[i] = " ".join(map(str, self.grid[i]))
        self.grid_p = "\n".join(map(str, self.grid_p))
        return self.grid_p