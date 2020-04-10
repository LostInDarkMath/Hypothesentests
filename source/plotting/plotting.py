# Copyright 2020 by Willi Sontopski. All rights reserved.

from typing import Callable, List
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime

# local file imports
from plotting.pickle_plots import save_plot


class FunctionToPlot:
    """Represents a function with a name and a color for plotting"""
    def __init__(self, function: Callable[[float], float], label: str, color: str = 'k'):
        self.func = function
        self.label = label
        self.color = color

    def plot(self, **kwargs) -> None:
        plot(functions_to_plot=[self], **kwargs)


def plot(functions_to_plot: List[FunctionToPlot],
         x_min: float = 0.,
         x_max: float = 1.,
         resolution: int = 1000,
         title: str = "Plot",
         print_benchmarks: bool = True,
         save_png: bool = False,
         save_pickle: bool = False,
         filename_without_extension: str = None,
         show_plot: bool = None
         ) -> None:
    """ Plots all functions in the functions_to_plot list.

    Parameters:
        functions_to_plot (list): The list of functions that will be plotted.
            Contains only elements of type FunctionToPlot.
        x_min (float): The lower bound of the plot.
        x_max (float): The upper bound of the plot.
        resolution (int): The number of points that will be plotted.
            Each function in functions_to_plot will be that often evaluated.
        title (str): The title of the plot.
        print_benchmarks (bool): Prints duration of the function evaluations.
        save_png (bool): saves the plot as png file iff True
        save_pickle (bool): saves the plot as .plt file iff True
            The plot can be loaded and viewed later with full matplotlib functionality.
        filename_without_extension (str): The filename used when the file is saved.
        show_plot (bool): Shows plot iff True. Its True by default iff the plot is not saved.

    Example:
        >>> f2p = FunctionToPlot(lambda x: x * x, label="Square", color='r')
        >>> plot([f2p], x_min=-1, x_max=1)
    """

    if x_min >= x_max or functions_to_plot == [] or resolution < 20:
        raise ValueError("invalid input arguments")

    x_axis = np.linspace(start=x_min, stop=x_max, num=resolution)
    figure = plt.figure()

    for p in functions_to_plot:
        y_axis = []
        start_time = time.time()
        for x in x_axis:
            y_axis.append(p.func(x))

        if print_benchmarks:
            print(
                "Benchmark: " + str(resolution) + " evaluations of function "
                + p.label + " took " + str(time.time() - start_time) + " seconds."
                )

        plt.plot(x_axis, y_axis, color=p.color, label=p.label)

    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid()
    plt.legend()

    if filename_without_extension is None:
        filename_without_extension = title + datetime.datetime.now().strftime('_%d.%m.%Y_%H.%M.%S')

    if show_plot is None:
        show_plot = not (save_pickle or save_png)  # useful default value depends on other parameters

    if save_png:
        plt.savefig(filename_without_extension + '.png', format='png', dpi=300)  # dpi = 300 is full HD

    if save_pickle:
        save_plot(figure, filename_without_extension + '.plt')

    if show_plot:
        plt.show()


if __name__ == "__main__":

    funcs = [
        FunctionToPlot(lambda x: x, label="id", color='r'),
        FunctionToPlot(lambda x: x * x, label="square", color='g'),
        FunctionToPlot(lambda x: x * x * x, label="cubic", color='b')
    ]
    plot(funcs, x_min=-10, x_max=10, save_pickle=True)
