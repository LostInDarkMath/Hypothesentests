# Copyright 2020 by Willi Sontopski. All rights reserved.

from math import sqrt, exp, log
from typing import Callable

# local file imports
from statistical_tests.statistical_test import StatisticalTest


class KsTestOneSided(StatisticalTest):
    def get_name(self) -> str:
        return "one-sided Kolmogorov Smirnov test"

    def get_statistic(self) -> float:
        """ See theorem 2.3.4 in master_thesis.pdf """
        return self._get_uep_max()[1]

    def get_cdf(self, max_iter: int) -> Callable[[float], float]:
        """ See theorem 2.3.3 in master_thesis.pdf """
        def result(x: float) -> float:
            if x <= 0:
                return 0.0
            return 1 - exp(-2 * x * x)
        return result

    def get_critical_value(self, alpha: float, epsilon: float = 0.0001, max_iter: int = 100, n: int = -1) -> float:
        """
        See equation (2.18) in master_thesis.pdf
        Parameters epsilon, max_iter and n will be ignored.
        """
        return sqrt(-0.5 * log(alpha))
