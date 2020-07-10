##  Lindenmayer system functions and classes

#   Imports
import itertools

from evolve_soft_2d import utility
from evolve_soft_2d.unit import rep_grid

################################################################################

class vocabulary:
    """The L-system vocabulary
    """

    def __init__(
        self,
        vocab: list,
        descr: list,
        ) -> None:
        """Vocabulary parameters

        Parameters
        ----------
        vocab : list
            The vocabulary members
        descr : list
            The description of the vocabulary members
        """

        self.vocab = vocab
        self.descr = descr

    def __repr__(self) -> str:
        """Format a representation of the L-system vocabulary for the log

        Returns
        -------
        str
            Formatted representation of the L-system vocabulary for the log
        """

        r = "L-System Vocabulary:\n"

        for i in range(0, len(self.vocab)):
            r += "{}: {}\n".format(self.vocab[i], self.descr[i])

        return r

################################################################################

class lsystem:
    """Lindenmayer system class
    """

    def __init__(
        self,
        vocab: vocabulary,
        gramm: list,
        axiom: str,
        n: int,
        ) -> None:
        """Lindenmayer system parameters

        Parameters
        ----------
        vocab : vocabulary
            The vocabulary of the L-system
        gramm : list
            The grammatical rules of the L-system
        axiom : str
            The initial axiom of the L-system
        n : int
            The number of iterations of the L-system
        """

        self.vocab = vocab
        self.gramm = gramm
        self.axiom = axiom
        self.n = n

        #   The final result of the L-system
        self.word = self.iterate()

        self.gramm_str = utility.list_to_str([i[0] + " -> " + i[1] for i in self.gramm], "\n")

    def __repr__(self) -> str:
        """Format a representation of the L-system

        Returns
        -------
        str
            Formatted representation of the L-system for the log
        """        

        r = "Grammar:\n{}\n".format(self.gramm_str)
        r += "Axiom:                {}\n".format(self.axiom)
        r += "Number Of Iterations: {}\n".format(self.n)
        r += "Resulting Word:       {}\n".format(self.word)
        r += "\n{}".format(self.vocab)

        return r

    def apply_gramm(
        self,
        c: str,
        ) -> str:
        """Apply the grammatical transformation to a character

        Parameters
        ----------
        c : str
            The character to be transformed

        Returns
        -------
        str
            The new string
        """        

        #   Loop through the grammatical rules
        for i in self.gramm:

            #   Check if the character matches the current rule
            if c == i[0]:

                #   Return the transformation
                return i[1]

        #   Return the original character if it matches no rules
        return c

    def rewrite(
        self,
        w: str
        ) -> str:
        """Rewrite a character string

        Parameters
        ----------
        w : str
            The character string

        Returns
        -------
        str
            The rewritten string
        """

        #   Initialisations
        rw = ""

        #   Loop through the character string
        for i in w:

            #   Rewrite the current character
            rw += self.apply_gramm(i)

        return rw

    def iterate(self) -> str:
        """Generate the final L-system string

        Returns
        -------
        str
            The final L-system string
        """

        #   Initialisation
        rw = self.axiom

        #   Loop for the specified number of iterations
        for _ in range(0, self.n):

            #   Rewrite the current string
            rw = self.rewrite(rw)

        return rw

################################################################################

def interpret_word(
    w: str,
    ) -> list:
    """Interpret a word generated by an L-system as an element grid

    Parameters
    ----------
    w : str
        The word generated by the L-system

    Returns
    -------
    list
        The element grid
    """    

    #   Initialisations
    c = []
    x = 0
    y = 0
    d = 0
    F1 = True

    x_stack = []
    y_stack = []
    d_stack = []
    x_stack.append(x)
    y_stack.append(y)
    d_stack.append(d)

    w_clean = w
    useless = ["[]", "++++", "----", "xxxxxxxx", "||||||||", "+-", "-+", "x|", "|x"]

    #   Loop through the list of useless character strings
    for i in useless:

        #   Remove useless substrings
        w_clean = w_clean.replace(i, "")

    #   Loop through every character in the string
    for i in w_clean:

        #   Check if the current character is F
        if i == "F":

            #   Check that the stack is not currently at its initial values and that the initial element flag is not set
            if len(x_stack) > 1 and F1 == False:

                #   Determine the x and y coordinates of the current element
                x, y = determine_c(d, x, y)

            else:

                #   Set the initial element coordinates
                x = 0
                y = 0

                #   Unset the flag
                F1 = False

            #   Add the element
            c.append([x, y])

        #   Check if the current character is f
        elif i == "f":

            #   Check that the stack is not currently at its initial values and that the initial element flag is not set
            if len(x_stack) > 1 and F1 == False:

                #   Determine the x and y coordinates of the current element
                x, y = determine_c(d, x, y)

            else:

                #   Set the initial element coordinates
                x = 0
                y = 0

                #   Unset the flag
                F1 = False

        #   Check if the current character is +
        elif i == "+":

            #   Update the direction
            d = update_d(i, d)

        #   Check if the current character is x
        elif i == "x":

            #   Update the direction
            d = update_d(i, d)

        #   Check if the current character is -
        elif i == "-":

            #   Update the direction
            d = update_d(i, d)

        #   Check if the current character is |
        elif i == "|":

            #   Update the direction
            d = update_d(i, d)

        #   Check if the current character is [
        elif i == "[":

            #   Push the current coordinates and direction
            x_stack.append(x)
            y_stack.append(y)
            d_stack.append(d)

        #   Check if the current character is ]
        elif i == "]":

            #   Check if the stacks have any coordinates pushed to them
            if len(x_stack) > 1:

                #   Pop the last saved coordinates and direction
                x = x_stack.pop()
                y = y_stack.pop()
                d = d_stack.pop()

                #   Check if the stack is at its initial values
                if len(x_stack) == 1:

                    #   Reset the flag
                    F1 = True

            else:

                #   Pop the original coordinates and direction
                x = x_stack[0]
                y = y_stack[0]
                d = d_stack[0]

    #   Remove any duplicate element coordinates
    c.sort()
    c = list(c for c, _ in itertools.groupby(c))

    #   Separate the x and y coordinates
    x_all = [i[0] for i in c]
    y_all = [i[1] for i in c]

    #   Normalise the coordinates
    x_all = utility.normalise_list(x_all, template.x_e)
    y_all = utility.normalise_list(y_all)

    #   Generate a grid of zeroes of the dimensions of the coordinate range
    grid_l = rep_grid.create_grid(max(x_all) + 1, max(y_all) + 1, 0)

    #   Add a second list dimension if the list is one-dimensional
    if max(y_all) == 0:
        grid_l = [grid_l]

    #   Loop through the list of coordinates
    for i in range(0, len(c)):

        #   Store the element coordinate in the grid
        grid_l[y_all[i]][x_all[i]] = 1

    #   Reverse the list order
    grid_l.reverse()

    return grid_l

################################################################################

def update_d(
    r: str,
    d: int,
    ) -> int:
    """Update the direction

    Parameters
    ----------
    r : str
        The direction of rotation
    d : int
        The current direction

    Returns
    -------
    int
        The updated direction
    """
    
    #   Check if the direction of rotation is 90 degrees positive
    if r == "+":
        d += 90

    #   Check if the direction of rotation is 45 degrees positive
    elif r == "x":
        d += 45

    #   Check if the direction of rotation is 90 degrees negative
    elif r == "-":
        d -= 90

    #   Check if the direction of rotation is 45 degrees negative
    elif r == "|":
        d -= 45
    
    #   Check if the direction is more than 360 degrees
    if d >= 360:
        d -=360

    #   Check if the direction is less than 0 degrees
    elif d < 0:
        d += 360

    return d

################################################################################

def determine_c(
    d: int,
    x: int,
    y: int,
    ) -> (int, int):
    """Determine the coordinates of the new element

    Parameters
    ----------
    d : int
        The current direction
    x : int
        The current x-coordinate
    y : int
        The current y-coordinate

    Returns
    -------
    (int, int)
        The x- and y-coordinates of the new element
    """

    if d == 0:
        y += 1

    elif d == 45:
        x += -1
        y += 1

    elif d == 90:
        x += -1

    elif d == 135:
        x += -1
        y += -1

    elif d == 180:
        y += -1

    elif d == 225:
        x += 1
        y += -1

    elif d == 270:
        x += 1

    elif d == 315:
        x += 1
        y += 1

    return (x, y)

################################################################################

def gen_lsystem(
    v: vocabulary,
    r_l: int,
    g_l: int,
    n: int,
    ) -> lsystem:
    """Generate a random L-system

    Parameters
    ----------
    v : vocabulary
        The vocabulary of the L-system
    r_l : int
        The length of the rules
    g_l : int
        The number of rules
    n : int
        The number of iterations

    Returns
    -------
    lsystem
        The L-system
    """

    #   Initialisations
    g = []

    #   Set the axiom as the initial letter of the vocabulary
    a = v.vocab[0]

    #   Loop until a rule including the axiom is defined
    while 1:

        #   Generate a random rule
        g2 = utility.gen_random(v.vocab, r_l)

        #   Check if the axiom is within the loop
        if a in g2:

            #   Exit the loop
            break

    #   Assign the first rule to the grammar
    g.append([a, g2])

    #   Loop through the remaining number of rules
    for _ in range(1, g_l):

        #   Loop until a new letter is assigned a rule
        while 1:

            #   Select a random letter
            g1 = utility.gen_random(v.vocab, 1)

            #   Check if the letter has not been selected before
            if g1 not in [i[0] for i in g]:

                #   Exit the loop
                break

        #   Assign a new rule to the grammar
        g.append([g1, utility.gen_random(v.vocab, r_l)])

    #   Define the L-system
    ls = lsystem(v, g, a, n)

    return ls

################################################################################

#   The L-system vocabulary used to generate internal elements

e_vocab = ["F", "f", "+", "x", "-", "|", "[", "]"]

e_descr = [
    "Create an element at the current position and increment the position",
    "Increment the position",
    "Rotate the current direction by 90 degrees counterclockwise",
    "Rotate the current direction by 45 degrees counterclockwise",
    "Rotate the current direction by 90 degrees clockwise",
    "Rotate the current direction by 45 degrees clockwise",
    "Push the current position",
    "Pop to the previously pushed position",
    ]

e_vocabulary = vocabulary(e_vocab, e_descr)

#   L-system axioms for symmetry

a_rot_hor = "[F]++[F]"

a_rot_ver = "-[F]++[F]"

a_rot_hor_ver = "[F]+[F]+[F]+[F]"

a_rot_dia = "x[F]++[F]"

a_rot_ndi = "|[F]++[F]"

a_rot_dia_ndi = "x[F]+[F]+[F]+[F]"