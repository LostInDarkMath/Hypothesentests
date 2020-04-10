# Copyright 2020 by Willi Sontopski. All rights reserved.

from math import sqrt, exp, pi
from typing import Callable

# local file imports
from statistical_tests.statistical_test import StatisticalTest
from simulation.statistic_tools import normal_cdf


class LnTestOneSided(StatisticalTest):
    def get_name(self) -> str:
        return "one-sided Ln test"

    def get_statistic(self) -> float:
        """ See equation (2.21) in master_thesis.pdf """
        argmax, max_value = self._get_uep_max()
        return max_value / sqrt(argmax * (1 - argmax))

    def get_cdf(self, max_iter: int) -> Callable[[float], float]:
        """ See theorem 2.3.7 in master_thesis.pdf """

        def result(x: float) -> float:
            if x <= 0:
                return 0.0
            return 2 * normal_cdf(x) - sqrt(2 / pi) * x * exp(-0.5 * x * x) - 1

        return result
