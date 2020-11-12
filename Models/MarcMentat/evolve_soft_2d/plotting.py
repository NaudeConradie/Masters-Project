##  Plotting functions

#   Imports
import math
import matplotlib.pyplot as plot
import seaborn

from evolve_soft_2d import file_paths

################################################################################

def histogram(
    template,
    tm: str,
    data: list,
    t: str,
    y: str,
    x: str,
    bins = "auto",
    color: str = "b",
    ) -> None:
    """Plot a histogram

    Parameters
    ----------
    template
        The unit template parameters
    tm : str
        The timestamp of the current simulation
    data : list
        The data to be plotted
    t : str
        The title of the graph
    y : str
        The label of the y-axis
    x : str
        The label of the x-axis
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

    # #   Show the plot
    # plot.show()

    #   Save the figure
    save_plot(template, t, tm)

    return

################################################################################

def scatterplot(
    template,
    tm: str,
    x_data: list,
    y_data: list,
    t: str,
    x_l: str,
    y_l: str,
    color: str = "b",
    marker: str = "o"
    ) -> None:
    """Plot a scatter plot

    Parameters
    ----------
    template
        The unit template parameters
    tm : str
        The timestamp of the current simulation
    x_data : list
        The data to be plotted on the x-axis
    y_data : list
        The data to be plotted on the y-axis
    t : str
        The title of the graph
    y : str
        The label of the y-axis
    x : str
        The label of the x-axis
    color : str, optional
        The colour of the graph, by default "b"
    marker : str, optional
        The plot markers, by default "o"
    """

    #   Determine the maximum x-axis value of the graph
    x_max = math.ceil(max(x_data))

    #   Open a figure
    plot.figure()

    #   Plot the scatter plot
    plot.rcParams.update({"figure.figsize":(7, 5), "figure.dpi":100})
    plot.scatter(x_data, y_data, c = color, marker = marker)
    plot.gca().set(title = t, ylabel = y_l, xlabel = x_l)
    plot.xlim(0, x_max)

    # #   Show the plot
    # plot.show()

    #   Save the figure
    save_plot(template, t, tm)

    return

################################################################################

def plot_all(
    template,
    v: list,
    n_e: list,
    l: list,
    tm: str,
    ) -> None:
    """Plot all desired figures

    Parameters
    ----------
    template
        The unit template parameters
    v : list
        The data to be plotted
    n_e : list
        The list of the number of elements removed from every element
    l : list
        The list of labels of the data
    tm : str
        The timestamp of the current simulation
    """

    scatterplot(template, tm, v[0], v[1], "Constraint Energy X vs Y", "Constraint Energy X (J)", "Constraint Energy Y (J)")
    scatterplot(template, tm, v[3], v[4], "Internal Energy X vs Y", "Internal Energy X (J)", "Internal Energy Y (J)")

    scatterplot(template, tm, n_e, v[6], "Elements Removed vs Hausdorff Distance", "Number of Elements Removed", "Hausdorff Distance")

    # #   Loop through the types of data
    # for i in range(0, len(v)):

    #     #   Plot the histogram
    #     histogram(template, tm, v[i], l[i], "Frequency", "Energy (J)")

    #     #   Plot the scatterplot
    #     scatterplot(template, tm, n_e, v[i], l[i], "Energy (J)", "Number of Elements Removed")

    # #   Plot a scatterplot
    # scatterplot(template, tm, v[0], v[1], "Constraint Energy (J)", "Y-direction", "X-direction")

    return

################################################################################

def save_plot(
    template,
    t: str,
    tm: str,
    ) -> None:
    """Save a figure

    Parameters
    ----------
    template
        The unit template parameters
    t : str
        The title of the graph
    tm : str
        The timestamp of the current simulation
    """    

    #   Create the file path of the figure
    fp_p = file_paths.create_fp_file(template, t + tm, "g")

    #   Save the figure
    plot.savefig(fp_p, dpi = 300)

    #   Close the figure
    plot.close()

    return