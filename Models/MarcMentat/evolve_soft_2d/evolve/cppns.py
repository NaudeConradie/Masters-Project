##  CPPN functions and classes

#   Imports
import numpy

from evolve_soft_2d import utility

################################################################################

class cppn:
    """The CPPN class object
    """

    def __init__(
        self,
        mod_n: int,
        n_n: int,
        hl_size: int,
        x: int,
        y: int,
        scale: float,
        af_n: int,
        seed: int,
        threshold: float = 0.5,
        ) -> None:
        """The CPPN parameters

        Parameters
        ----------
        mod_n : int
            The number of models to be generated from a particular seed
        n_n : int
            The number of nodes in each fully connected layer of the network
        hl_size : int
            The size of the hidden layers
        x : int
            The number of elements in the x-direction
        y : int
            The number of elements in the y-direction
        scale : float
            The scale of the focus on the model
        af_n : int
            The umber of activation functions to apply
        seed : int
            The seed for the random generation
        threshold : float, optional
            The rounding threshold of the model element values, by default 0.5
        """

        self.mod_n = mod_n
        self.n_n = n_n
        self.hl_size = hl_size
        self.x = x
        self.y = y
        self.scale = scale
        self.af_n = af_n
        self.seed = seed
        self.threshold = threshold

        #   The resolution of the grid
        self.res = self.x*self.y

        #   Build the grid
        self.grid = self.cppn_grid()

    def __repr__(self) -> str:
        """Format a representation of the CPPN

        Returns
        -------
        str
            Formatted representation of the CPPN for the log
        """

        r = "Model Dimensions:          {}x{} elements\n".format(self.x, self.y)
        r += "Seed:                      {}\n".format(self.seed)
        r += "Rounding Threshold:        {}\n".format(self.threshold)
        r += "Model Scale:               1:{}\n".format(self.scale)
        r += "Size Of Hidden Layer:      {}\n".format(self.hl_size)
        r += "Number Of Nodes Per Layer: {}\n".format(self.n_n)
        r += "Activation Functions:\n"

        for i in range(0, self.af_n + 1):

            r += "{}\n".format(self.af[i])

        return r

    def cppn_grid(self) -> numpy.array:
        """Generates model grids

        Returns
        -------
        numpy.array
            The model grid
        """

        #   Initialisations
        self.af = []

        #   The list of possible activation functions
        af_l = [self.cppn_sin, self.cppn_cos, self.cppn_tanh, self.cppn_sigm, self.cppn_srel]
        af_o = [self.cppn_sigm_o, self.cppn_srel_o]

        #   Set the random generation seed
        numpy.random.seed(seed = self.seed)

        #   Generate the hidden layer for each model
        hl = numpy.random.uniform(low = -1, high = 1, size = (self.mod_n, self.hl_size)).astype(numpy.float32)

        #   Generate the grid matrix
        x_r = numpy.linspace(-1*self.scale, self.scale, num = self.x)
        x_m = numpy.matmul(numpy.ones((self.y, 1)), x_r.reshape((1, self.x)))

        y_r = numpy.linspace(-1*self.scale, self.scale, num = self.y)
        y_m = numpy.matmul(y_r.reshape((self.y, 1)), numpy.ones((1, self.x)))
        
        r_m = numpy.sqrt(x_m*x_m + y_m*y_m)

        x_d = numpy.tile(x_m.flatten(), self.mod_n).reshape(self.mod_n, self.res, 1)
        y_d = numpy.tile(y_m.flatten(), self.mod_n).reshape(self.mod_n, self.res, 1)
        r_d = numpy.tile(r_m.flatten(), self.mod_n).reshape(self.mod_n, self.res, 1)

        #   Scale the hidden layers
        hl_scale = numpy.reshape(hl, (self.mod_n, 1, self.hl_size))*numpy.ones((self.res, 1), dtype = numpy.float32)*self.scale

        #   Unwrap the grid matrices
        x_d_unwrap = numpy.reshape(x_d, (self.mod_n*self.res, 1))
        y_d_unwrap = numpy.reshape(y_d, (self.mod_n*self.res, 1))
        r_d_unwrap = numpy.reshape(r_d, (self.mod_n*self.res, 1))
        hl_unwrap = numpy.reshape(hl_scale, (self.mod_n*self.res, self.hl_size))

        #   Build the network
        n = self.fully_connected(hl_unwrap, self.n_n, True) + self.fully_connected(x_d_unwrap, self.n_n, False) + self.fully_connected(y_d_unwrap, self.n_n, False) + self.fully_connected(r_d_unwrap, self.n_n, False)

        #    Build the model
        mod = numpy.tanh(n)

        #   Loop through the desired number of activation functions
        for i in range(0, self.af_n):

            numpy.random.seed(seed = self.seed + i)

            #   Select and record the activation function
            mod, af_c = numpy.random.choice(af_l)(mod)
            self.af.append(af_c)

        numpy.random.seed(seed = self.seed)

        #   Apply and record the final function
        mod, af_o = numpy.random.choice(af_o)(mod)
        self.af.append(af_o)

        #   Round the grid according to the given threshold
        mod = [0 if i < self.threshold else 1 for i in mod]

        #   Reshape the grid to fit the given dimensions
        mod = numpy.reshape(mod, (self.mod_n, self.x, self.y))

        return mod

    def fully_connected(
        self,
        i_v: numpy.array,
        o_d,
        w_bias: bool,
        ) -> numpy.array:
        """Connect the hidden layers of the CPPN

        Parameters
        ----------
        i_v : numpy.array
            The input vector
        o_d
            The output dimensions
        w_bias : bool
            If the layers should be connected with bias

        Returns
        -------
        numpy.array
            The connected results
        """        

        #   Set the random generation seed
        numpy.random.seed(seed = self.seed)

        #   Generate the random matrix
        m = numpy.random.standard_normal(size = (i_v.shape[1], o_d)).astype(numpy.float32)

        #   Multiply the input with the matrix
        result = numpy.matmul(i_v, m)

        #   Check if the bias must be included
        if w_bias:

            #   Generate the random bias
            bias = numpy.random.standard_normal(size = (1, o_d)).astype(numpy.float32)

            #   Add the bias to the result
            result += bias*numpy.ones((i_v.shape[0], 1), dtype = numpy.float32)

        return result

    def cppn_sin(
        self,
        hl: numpy.array
        ) -> (numpy.array, str):    
        """Apply sin as the activation function for the current layer

        Parameters
        ----------
        hl : numpy.array
            The current layer

        Returns
        -------
        numpy.array, str:
            The new layer
            The label of the activation function
        """

        name = "sin"

        out = numpy.sin(self.fully_connected(hl, self.n_n, True))

        return out, name

    def cppn_cos(
        self,
        hl: numpy.array
        ) -> (numpy.array, str):
        """Apply cos as the activation function for the current layer

        Parameters
        ----------
        hl : numpy.array
            The current layer

        Returns
        -------
        numpy.array, str:
            The new layer
            The label of the activation function
        """

        name = "cos"

        out = numpy.cos(self.fully_connected(hl, self.n_n, True))

        return out, name

    def cppn_tanh(
        self,
        hl: numpy.array
        ) -> (numpy.array, str):
        """Apply tanh as the activation function for the current layer

        Parameters
        ----------
        hl : numpy.array
            The current layer

        Returns
        -------
        numpy.array, str:
            The new layer
            The label of the activation function
        """

        name = "tanh"

        out = numpy.tanh(self.fully_connected(hl, self.n_n, True))

        return out, name

    def cppn_sigm(
        self,
        hl: numpy.array
        ) -> (numpy.array, str):
        """Apply a sigmoid as the activation function for the current layer

        Parameters
        ----------
        hl : numpy.array
            The current layer

        Returns
        -------
        numpy.array, str:
            The new layer
            The label of the activation function
        """

        name = "sigmoid"

        out = utility.sigmoid(self.fully_connected(hl, self.n_n, True))

        return out, name

    def cppn_srel(
        self,
        hl: numpy.array
        ) -> (numpy.array, str):
        """Apply smooth ReLu as the activation function for the current layer

        Parameters
        ----------
        hl : numpy.array
            The current layer

        Returns
        -------
        numpy.array, str:
            The new layer
            The label of the activation function
        """

        name = "smooth ReLu"

        out = utility.smooth_relu(self.fully_connected(hl, self.n_n, True))

        return out, name

    def cppn_sigm_o(
        self,
        hl: numpy.array
        ) -> (numpy.array, str):
        """Apply a sigmoid as the activation function for the final layer

        Parameters
        ----------
        hl : numpy.array
            The current layer

        Returns
        -------
        numpy.array, str:
            The new layer
            The label of the activation function
        """

        name = "sigmoid"

        out = utility.sigmoid(self.fully_connected(hl, 1, True))

        return out, name

    def cppn_srel_o(
        self,
        hl: numpy.array
        ) -> (numpy.array, str):
        """Apply smooth ReLu as the activation function for the final layer

        Parameters
        ----------
        hl : numpy.array
            The current layer

        Returns
        -------
        numpy.array, str:
            The new layer
            The label of the activation function
        """

        name = "smooth ReLu"

        out = utility.smooth_relu(self.fully_connected(hl, 1, True))

        return out, name

################################################################################

class cppn_i:
    """The CPPN model
    """    

    def __init__(
        self,
        cppn: cppn,
        mod_id: int,
        ) -> None:
        """The CPPN model parameters

        Parameters
        ----------
        cppn : cppn
            The CPPN
        mod_id : int
            The model number
        """        

        self.cppn = cppn
        self.mod_id = mod_id

        #   The model grid
        self.grid = self.cppn.grid[self.mod_id].tolist()

    def __repr__(self) -> str:
        """Format a representation of the CPPN model

        Returns
        -------
        str
            Formatted representation of the CPPN model for the log
        """

        r = "Model ID: {}\n".format(self.mod_id)
        r += "CPPN Parameters:\n{}".format(self.cppn)

        return r

################################################################################

def cppn_rem(
    template,
    grid: list,
    ) -> list:
    """Obtain the list of elements to be removed according to the generated CPPN

    Parameters
    ----------
    template
        The unit template parameters
    grid : list
        The grid generated by the CPPN

    Returns
    -------
    list
        The list of element IDs to be removed
    """

    #   Initialisations
    rem = []

    #   Create a copy of the grid
    g_temp = grid[:]

    #   Reverse the order of the grid
    g_temp.reverse()

    #   Calculate the element ID offset according to the boundary thickness
    offset = template.x_e*template.b + template.b + 1

    #   Loop through rows of the grid
    for i in g_temp:

        #   Loop through the elements in the current row
        for j in range(0, len(i)):

            #   Check if the current element needs to be removed
            if i[j] == 0:

                #   Add the element ID to the list of element IDs to be removed
                rem.append(j + offset)

        #   Increment the offset
        offset += template.x_e

    return rem