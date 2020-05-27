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
    bins : optional
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
    plot.hist(data, bins = bins, color = color)
    plot.gca().set(title = t, ylabel = y, xlabel = x)
    plot.xlim(0, bin_max)

    #   Show the plot
    plot.show()

    return

################################################################################

def scatterplot(
    template,
    x_data: list,
    y_data: list,
    t: str,
    y: str,
    x: str,
    color: str = "b",
    marker: str = "o"
    ) -> None:
    """[summary]

    Parameters
    ----------
    template : [type]
        [description]
    x_data : list
        [description]
    y_data : list
        [description]
    t : str
        [description]
    y : str
        [description]
    x : str
        [description]
    color : str, optional
        [description], by default "b"
    marker : str, optional
        [description], by default "o"
    """

    x_max = math.ceil(max(x_data))

    #   Open a figure
    plot.figure()

    #   Plot the scatter plot
    plot.rcParams.update({"figure.figsize":(7, 5), "figure.dpi":100})
    plot.scatter(x_data, y_data, c = color, marker = marker)
    plot.gca().set(title = t, ylabel = y, xlabel = x)
    plot.xlim(0, x_max)

    #   Show the plot
    plot.show()

    return