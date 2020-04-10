# Copyright 2020 by Willi Sontopski. All rights reserved.
"""Save and load interactive matplotlib plots with pickle."""

import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import pickle


def save_plot(figure: plt.Figure, filename: str) -> None:
    """Saves plot with pickle

    Example:
        >>> fig_handle = plt.figure()
        >>> x = np.linspace(0, 2 * np.pi)
        >>> y = np.sin(x)
        >>> plt.plot(x, y)
        >>> save_plot(fig_handle, "my_plot.plt")
    """

    with open(filename, 'wb') as file:  # should be 'wb' rather than 'w': write in binary mode!
        pickle.dump(figure, file)


def load_plot(filename: str, show_plot: bool = True) -> plt.Figure:
    """Load plot with pickle

     Exceptions:
        FileNotFoundError : iff the file was not found
        pickle.UnpicklingError : iff pickle is unable to unpickle it
        KeyError : iff read file is corrupt

    Example:
        >>> load_plot("my_plot.plt")
    """

    with open(filename, 'rb') as file:  # should be 'rb' rather than 'r': read in binary mode!
        figure = pickle.load(file)

    if show_plot:
        show_figure(figure)
    return figure


def show_figure(figure: plt.Figure) -> None:
    """Shows the figure, even if the figure was shown and therefore closed before"""
    try:
        figure.show()
        plt.show()
    except AttributeError:
        # the exception is raised iff the figure was closed. In this case we need a dummy figure ans its manager
        # https://stackoverflow.com/questions/49503869/attributeerror-while-trying-to-load-the-pickled-matplotlib-figure
        dummy = plt.figure()
        new_manager = dummy.canvas.manager
        new_manager.canvas.figure = figure
        figure.set_canvas(new_manager.canvas)
        figure.show()
        plt.show()


def show_all_saved_plots(
        pathname: str = '', 
        file_type: str = 'plt', 
        check_subdirectories: bool = False
) -> None:
    """ Opens and displays all plots (in pickle dump format) in the given directory.
        If pathname == '', the current working directory is used.

    Example:
        >>> show_all_saved_plots("dist")  # looks at subdirectory "dist"
        >>> show_all_saved_plots("C:\\Users\\sontopski\\Desktop")
    """
    for file in glob.glob(os.path.join(pathname, "*." + file_type), recursive=check_subdirectories):
        print(file)
        load_plot(file, show_plot=True)


if __name__ == "__main__":
    # load_plot("my_plot.plt")
    show_all_saved_plots()

    # Plot simple sinus function
    fig_handle = plt.figure()
    x = np.linspace(0, 2 * np.pi)
    y = np.exp(x)
    plt.plot(x, y)
    plt.show()
    save_plot(fig_handle, "my_plot.plt")
