##  Lindenmayer system functions and classes

#   Imports
import itertools
import numpy
import pandas

from evolve_soft_2d import utility
from evolve_soft_2d.unit import rep_grid

################################################################################

class vocabulary:
    """The L-system vocabulary
    """

    def __init__(
        self,
        var: list,
        con: list,
        var_descr: list,
        con_descr: list,
        ) -> None:
        """Vocabulary parameters

        Parameters
        ----------
        vocab : list
            The vocabulary members
        descr : list
            The description of the vocabulary members
        """

        self.var = var
        self.con = con
        self.var_descr = var_descr
        self.con_descr = con_descr

    def __repr__(self) -> str:
        """Format a representation of the L-system vocabulary for the log

        Returns
        -------
        str
            Formatted representation of the L-system vocabulary for the log
        """

        r = "L-System Variables:\n"
        for i in range(0, len(self.var)):
            r += "{}: {}\n".format(self.var[i], self.var_descr[i])
        r += "L-System Constants:\n"
        for i in range(0, len(self.con)):
            r += "{}: {}\n".format(self.con[i], self.con_descr[i])

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
        seed: int = None,
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
        seed : int, optional
            The seed for the random generation, by default None
        """

        self.seed = seed
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
        if self.seed is not None:
            r += "\nSeed: {}\n".format(self.seed)

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
        rw = "F"

        #   Loop for the specified number of iterations
        for _ in range(0, self.n):

            #   Rewrite the current string
            rw = self.rewrite(rw)

        #   Apply the axiom
        rw = self.axiom.replace("F", rw)

        return rw

################################################################################

def interpret_word(
    template,
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

    keep = []

    #   Determine how many reflections are initiated
    reflections = w.count("(")

    #   Loop through the number of reflections
    for _ in range(0, reflections):

        #   Find the reflection boundary indices
        b1 = w.find("(")
        b2 = w.find(")")

        #   Apply the reflection transformation
        s = utility.clean_str(w[b1:b2 + 1], ["(", ")", "+", "-", "x"], ["[", "]", "x", "+", "-"])

        #   Replace the relevant substring with its reflection
        w = utility.clean_str(w, [w[b1:b2 + 1]], [s])

    #   Loop through every character in the string
    for i in w:

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

        #   Check if the current character is -
        elif i == "-":

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

    #   Format the list of coordinates as a dataframe
    col = ["x", "y"]
    c = pandas.DataFrame(c, columns = col)

    #   Normalise the coordinates
    c.x = utility.normalise_list(c.x, template.x_e/2 - 0.5)
    c.y = utility.normalise_list(c.y, template.y_e/2 - 0.5)

    #   Remove any coordinates outside the bounds of the internal space
    c = c[c.x >= template.b]
    c = c[c.x < template.x_e - template.b]
    c = c[c.y >= template.b]
    c = c[c.y < template.y_e - template.b]

    #   Reformat the dataframe
    c = c.reset_index(drop = True)
    c = c.astype(int)

    #   Loop through the dataframe
    for i in range(0, len(c)):

        #   Append the element coordinate to the list of coordinates
        keep.append(1 + c.x[i] + c.y[i]*template.x_e)

    #   Determine which elements should be removed
    rem = utility.unique_list(template.e_internal, keep)

    return rem

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
    
    #   Check if the direction of rotation is 45 degrees positive
    if r == "+":
        d += 45

    #   Check if the direction of rotation is 45 degrees negative
    elif r == "-":
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
    seed: int,
    v: vocabulary,
    a_i: int,
    r_n: int,
    r_l: int,
    n: int,
    ) -> lsystem:
    """Generate a random L-system

    Parameters
    ----------
    seed : int
        The seed for the random generation
    v : vocabulary
        The vocabulary of the L-system
    a_i : int
        The index of the axis of symmetry to use
    r_n : int
        The number of rules to generate
    r_l : int
        The length of the rules
    n : int
        The number of iterations for the L-System

    Returns
    -------
    lsystem
        The L-System
    """    

    #   Initialisations
    g = []
    i = 0
    j = 0

    #   Select the axiom from the list of axioms
    aos = a_all[a_i]

    #   Loop until a rule including the command to draw an element is defined
    while 1:

        #   Generate a random rule
        g2 = utility.gen_random(l_c, r_l, seed + i)

        #   Check if the command to draw an element is included in the rule
        if "F" in g2:

            #   Exit the loop
            break

        i += 1

    #   Save the first rule
    g.append(["F", g2])

    #   Loop through the number of rules to generate
    for i in range(1, r_n):

        #   Loop until a rule applied to a new character is generated
        while 1:

            numpy.random.seed(seed = seed + j)

            #   Select a character
            g1 = numpy.random.choice(e_var[1:])

            #   Check if the character already has a rule applied to it
            if g1 not in [i[0]for i in g]:
                
                #   Exit the loop
                break

            j += 1

        #   Generate the rule
        g2 = utility.gen_random(l_c, r_l, seed = seed + i)

        #   Add the rule to the list of rules
        g.append([g1, g2])

    #   Define the L-system
    ls = lsystem(v, g, aos, n, seed = seed)

    return ls

################################################################################

#   The L-system vocabulary used to generate internal elements

e_var = ["F", "f", "+", "-"]

e_con = ["[", "]", "(", ")"]

e_var_descr = [
    "Create an element at the current position and increment the position",
    "Increment the position",
    "Rotate the current direction by 45 degrees counterclockwise",
    "Rotate the current direction by 45 degrees clockwise",
    ]

e_con_descr = [
    "Push the current position",
    "Pop to the previously pushed position",
    "Push and reflect the current position",
    "Pop and unreflect to the previously pushed and reflected position",
    ]

e_vocabulary = vocabulary(e_var, e_con, e_var_descr, e_con_descr)

#   L-system axioms for symmetry

a_rot_hor = "[F]++++[F]"

a_rot_ver = "--[F]++++[F]"

a_rot_hor_ver = "[F]++[F]++[F]++[F]"

a_rot_dia = "+[F]++++[F]"

a_rot_ndi = "-[F]++++[F]"

a_rot_dia_ndi = "+[F]++[F]++[F]++[F]"

a_mir_hor = "[F]++++(F)"

a_mir_ver = "--[F]++++(F)"

a_mir_hor_ver = "[F]++(F)++[F]++(F)"

a_mir_dia = "+[F]++++(F)"

a_mir_ndi = "-[F]++++(F)"

a_mir_dia_ndi = "+[F]++(F)++[F]++(F)"

a_all = [a_rot_hor, a_rot_ver, a_rot_hor_ver, a_rot_dia, a_rot_ndi, a_rot_dia_ndi, a_mir_hor, a_mir_ver, a_mir_hor_ver, a_mir_dia, a_mir_ndi, a_mir_dia_ndi]

#   L-System components for random generation
l_c = ["F", "f", "+", "-", "++", "--", "fF", "Ff", "[F]", "[f]", "[+F]", "[+fF]", "[-F]", "[-fF]"]