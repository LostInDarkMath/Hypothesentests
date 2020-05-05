# Copyright 2020 by Willi Sontopski. All rights reserved.

from typing import List
import matplotlib.pyplot as plt
import numpy as np

# local file imports
from simulation.statistic_tools import get_random_values, ecdf, uep
from simulation.piecewise_linear_function import PiecewiseLinearFunction


def plot_data(
        list_of_data: List[List[float]],
        plot_scatter: bool = True,
        plot_ecdf: bool = True,
        plot_uep: bool = True
              ) -> None:
    """Plots data and the corresponding empirical cumulative distribution function."""
    fig_uep, ax_uep = plt.subplots()
    fig_ecdf, ax_ecdf = plt.subplots()
    fig_scatter, ax_scatter = plt.subplots()
    number_of_samples = len(list_of_data)

    # make sure, that each color is only used once
    cm = plt.get_cmap('gist_rainbow')
    colors = [cm(1. * i / number_of_samples) for i in range(number_of_samples)]
    ax_scatter.set_prop_cycle(color=colors)
    ax_ecdf.set_prop_cycle(color=colors)
    ax_uep.set_prop_cycle(color=colors)

    x_axis_grid = np.linspace(0., 1., len(list_of_data[0]))  # grid with equal distance in [0,1]

    for i, data in enumerate(list_of_data):
        emp_dist_func = ecdf(data)(x_axis_grid)
        uni_emp_proc = uep(np.array(data))(x_axis_grid)

        if plot_scatter:
            ax_scatter.scatter(x_axis_grid, data, s=2)  # s = Size of each point
        if plot_ecdf:
            ax_ecdf.plot(x_axis_grid, emp_dist_func, linewidth=1, label='F_n(x), ' + str(i + 1))
        if plot_uep:
            ax_uep.plot(x_axis_grid, uni_emp_proc, linewidth=1, label='U_n(x), ' + str(i + 1))

    # actual plotting: all in one
    if plot_uep:
        ax_uep.set_title('Uniformer empirischer Prozess')
        ax_uep.set_xlabel('x')
        ax_uep.set_ylabel('U_n(x)')
        ax_uep.grid()
        ax_uep.legend()
        ax_uep.plot()

    if plot_ecdf:
        ax_ecdf.plot(x_axis_grid, x_axis_grid, linewidth=1, color='k', label='F_U(x)')  # real distribution function

        ax_ecdf.set_title('Empirische Verteilungsfunktion der Rohdaten gegen die echte Verteilungsfunktion')
        ax_ecdf.set_xlabel('x')
        ax_ecdf.set_ylabel('F(x)')
        ax_ecdf.grid()
        ax_ecdf.legend()
        ax_ecdf.plot()

    if plot_scatter:
        ax_scatter.set_title('Plot der Rohdaten')
        ax_scatter.set_xlabel('Index des Datums')
        ax_scatter.set_ylabel('Wert der x-ten Zufallszahl')
        ax_scatter.grid()
        ax_scatter.plot()
    plt.show()


if __name__ == "__main__":
    SIZE_OF_SINGLE_SAMPLE = 10000
    NUMBER_OF_SAMPLES = 5
    EPSILON = 0.02  # should be <= 0.05
    my_points = [[0.5, 0.45], [0.5, 0.55]]

    my_distribution_function = PiecewiseLinearFunction(my_points)
    uniform_dist_with_eps_error = PiecewiseLinearFunction([[0.9, 0.9], [0.95, 0.95 + EPSILON]])
    distr_func = uniform_dist_with_eps_error
    distr_func.plot(resolution=SIZE_OF_SINGLE_SAMPLE)

    my_list = []
    for j in range(NUMBER_OF_SAMPLES):
        my_list.append(get_random_values(distr_func, SIZE_OF_SINGLE_SAMPLE))
    plot_data(my_list)
