# Copyright 2020 by Willi Sontopski. All rights reserved.

import numpy as np

# local file imports
from simulation.statistic_tools import get_cdf_uniform_with_eps_error, get_random_values
from statistical_tests.ks_test import KsTest
from plotting.plotting import plot, FunctionToPlot
from simulation.test_wrapper import WrappedStatisticalTest
from simulation.piecewise_linear_function import PiecewiseLinearFunction
from statistical_tests.statistical_test import StatisticalTest


class MonteCarloSimulation:
    def __init__(self,
                 number_of_vectors: int,
                 length_of_vector: int,
                 alpha: float,
                 epsilon: float = 0.0001,
                 max_iter: int = 100):
        self.n = length_of_vector
        self.m = number_of_vectors
        self.alpha = alpha
        self.epsilon = epsilon
        self.max_iter = max_iter
        self.tests = []

    def add_test(self, test: StatisticalTest) -> None:
        self.tests.append(test)

    def __get_exact_critical_value(self, data: np.array) -> float:
        return np.quantile(data, q=(1 - self.alpha), interpolation='lower')

    def get_exact_critical_value(self) -> float:
        """Returns the so called exact critical value of the Kolmogorov Smirnov test"""
        test = KsTest()
        tns = []
        c_n = test.get_critical_value(alpha=self.alpha, epsilon=self.epsilon, max_iter=self.max_iter)

        for i in range(self.m):
            data_vec = np.random.uniform(size=self.n)
            test.data = data_vec
            tns.append(test.get_statistic())

        critical_value = self.__get_exact_critical_value(tns)
        print("c_n=", c_n, "; exact critical value=", critical_value)
        return critical_value

    def test_arbitrary_cdf(self, test: StatisticalTest, cdf: PiecewiseLinearFunction) -> float:
        """Returns empirical probability of test dismisses H_0 (not uniform distributed).
           For testing, random vectors are generated, which follow the given cdf.
           For n to infinity, the return value converges to self.alpha, if the given data is really uniform distributed.
        """
        d_alpha = test.get_critical_value(alpha=self.alpha, epsilon=self.epsilon, max_iter=self.max_iter)

        empirical_probability_h0_dismissed = 0.0
        for i in range(self.m):
            random_values = get_random_values(cdf, size=self.n)
            test.data = random_values
            s = test.get_statistic()
            if s > d_alpha:  # if test dismisses H_0 (
                empirical_probability_h0_dismissed += 1 / self.m
        return empirical_probability_h0_dismissed

    def plot_quality_function(self,
                              epsilon_max: float = 0.05,
                              resolution: int = 20,
                              error_position: float = 0.1,
                              error_delta: float = 1.,
                              plot_cdfs: bool = False,
                              **kwargs) -> None:
        """Complexity: O(self.m * self.n * resolution * len(self.statistical_tests))"""

        wrapped_tests = []
        for test in self.tests:
            wrapped_tests.append(WrappedStatisticalTest(test, test.get_critical_value(
                alpha=self.alpha, epsilon=self.epsilon, max_iter=self.max_iter, n=self.n
            )))

        epsilons = np.linspace(start=min(0.0, epsilon_max), stop=max(0.0, epsilon_max), num=resolution)
        cdfs = []

        for epsilon in epsilons:
            cdf_with_eps_error = get_cdf_uniform_with_eps_error(
                    epsilon=epsilon, error_position=error_position, delta=error_delta
                )
            cdfs.append(FunctionToPlot(cdf_with_eps_error.function, label='epsilon=' + str(epsilon)))

            for i in range(self.m):
                random_values = get_random_values(cdf_with_eps_error, size=self.n)

                for w_test in wrapped_tests:
                    w_test.test.data = random_values

                    if w_test.test.get_statistic() > w_test.critical_value:  # if test dismisses H_0
                        if epsilon not in w_test.empirical_probability_h0_dismissed:
                            w_test.empirical_probability_h0_dismissed[epsilon] = 0.0
                        w_test.empirical_probability_h0_dismissed[epsilon] += 1 / self.m

        functions_to_plot = [FunctionToPlot(lambda x: self.alpha, label='alpha', color='k')]
        for w_test in wrapped_tests:
            functions_to_plot.append(
                FunctionToPlot(lambda eps, t=w_test: t.empirical_probability_h0_dismissed[eps],  # late binding!
                               label=w_test.test.get_name(), color=w_test.test.color)
            )

        if plot_cdfs:
            plot(cdfs, title="Gestörte Verteilungsfunktionen")
        plot(functions_to_plot, x_min=min(0., epsilon_max), x_max=max(0., epsilon_max), resolution=resolution,
             title="Vergleich Gütefunktionen; epsilon max=" + str(epsilon_max) + ", resolution=" + str(resolution)
                   + ", delta=" + str(error_delta) + ", error position=" + str(error_position),
             **kwargs
             )
