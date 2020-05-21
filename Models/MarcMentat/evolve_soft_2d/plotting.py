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
        The data to be plotted
    t : str
        The title of the graph
    y : str
        The label of the y-axis
    x : str
        The label of the x-axis
    alpha : int, optional
        The alpha value of the graph, by default 0.5
    bins : str, optional
        The bin settings, by default "auto"
    color : str, optional
        The colour of the graph, by default "b"
    """

    #   Determine the maximum x-axis value of the graph
    bin_max = math.ceil(max(data))

    #   Open a figure
    plot.figure()

    #   Plot the histogram
    plot.rcParams.update({"figure.figsize":(7, 5), "figure.dpi":100})
    plot.hist(data, alpha = alpha, bins = bins, color = color)
    plot.gca().set(title = t, ylabel = y, xlabel = x)
    plot.xlim(0, bin_max)

    #   Show the plot
    plot.show()

    return