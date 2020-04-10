# Copyright 2020 by Willi Sontopski. All rights reserved.

from math import sqrt, pi, exp
from typing import Callable

# local file imports
from statistical_tests.statistical_test import StatisticalTest


class KsTest(StatisticalTest):
    def get_name(self) -> str:
        return "Kolmogorov Smirnov test"

    def get_statistic(self) -> float:
        """ See equation (2.7) in master_thesis.pdf"""
        return self._get_uep_abs_max()[1]

    def get_cdf(self, max_iter: int) -> Callable[[float], float]:
        """
        Return the Kolmogorov Smirnov distribution function
        See theorem 2.2.6 in master_thesis.pdf and
        https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test#Kolmogorov_distribution for the other formula.
        The formula in master_thesis.pdf has an extremly high numerical error when calculation a finite sum.
        """
        def result(x: float) -> float:
            if x <= 0:
                return 0.0
            res = 0.0
            for k in range(1, max_iter + 1, 1):
                a = 2 * k - 1
                res += exp(-(a * a * pi * pi) / (8 * x * x))
            return (sqrt(2 * pi) / x) * res
        return result
