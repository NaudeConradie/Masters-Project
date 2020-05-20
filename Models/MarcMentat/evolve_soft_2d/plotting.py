##  Plotting functions

#   Imports
import math
import matplotlib.pyplot as plot

################################################################################

def histogram(
    data: list,
    t: str,
    y: str,
    x: str,
    alpha: int = 0.5,
    bins = "auto",
    color: str = "b",
    ) -> None:
    """[summary]

    Parameters
    ----------
    data : list
        [description]
    t : str
        [description]
    y : str
        [description]
    x : str
        [description]
    alpha : int, optional
        [description], by default 0.5
    bins : str, optional
        [description], by default "auto"
    color : str, optional
        [description], by default "b"
    """

    bin_max = math.ceil(max(data))

    plot.figure()
    plot.rcParams.update({"figure.figsize":(7, 5), "figure.dpi":100})

    plot.hist(data, alpha = alpha, bins = bins, color = color)
    plot.gca().set(title = t, ylabel = y, xlabel = x)
    plot.xlim(0, bin_max)

    plot.show()

    return