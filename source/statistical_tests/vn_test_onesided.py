# Copyright 2020 by Willi Sontopski. All rights reserved.

from math import sqrt, pi, log
from typing import Callable

# local file imports
from statistical_tests.statistical_test import StatisticalTest


class VnTestOneSided(StatisticalTest):
    def get_name(self) -> str:
        return "one-sided Vn test"

    def get_statistic(self) -> float:
        """ See equation (2.19) in master_thesis.pdf """
        ks_statistic = self.uep()

        def f(t: float) -> float:
            if t <= 0.0 or t >= 1.0:
                return 0.0  # avoid division by zero
            return ks_statistic(t) / sqrt(t * (1 - t))

        argmax, max_value = self._get_max_of_almost_piecewise_linear_function(f)
        return max_value

    def get_cdf(self, max_iter: int) -> Callable:
        raise ValueError("The Vn test has no distribution function!")

    def get_critical_value(self, alpha: float, n: int = -1, epsilon: float = 0.0001, max_iter: int = 100) -> float:
        """
        Arguments epsilon and max_iter are not used here.
        See equation (2.20) in master_thesis.pdf
        """
        if n == -1:
            n = self.n
        if n < 3:
            raise ValueError("n should be >= 3")

        loglogn = log(log(n))
        an = sqrt(2 * loglogn)
        dn = 2 * loglogn + 0.5 * log(loglogn) - 0.5 * log(pi)
        return (dn - log(-log(1 - alpha))) / an
