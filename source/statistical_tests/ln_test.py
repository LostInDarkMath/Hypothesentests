# Copyright 2020 by Willi Sontopski. All rights reserved.

from math import sqrt
from typing import Callable

# local file imports
from statistical_tests.statistical_test import StatisticalTest
from simulation.statistic_tools import normal_cdf, normal_density


class LnTest(StatisticalTest):
    def get_name(self) -> str:
        return "Ln test"

    def get_statistic(self) -> float:
        """ See equation (2.11) in master_thesis.pdf """
        argmax, max_value = self._get_uep_abs_max()
        return max_value / sqrt(argmax * (1 - argmax))

    def get_cdf(self, max_iter: int) -> Callable[[float], float]:
        """ See theorem 2.2.15 in master_thesis.pdf """

        def result(x: float) -> float:
            if x <= 0:
                return 0.0

            res = 4 * (normal_cdf(x) - 0.5 - x * normal_density(x))  # case l = 0 in sum no. 2
            for l in range(1, max_iter + 1, 1):  # from 1 to max_iter
                al = 2 * l + 1
                phialx = normal_cdf(al * x) - 0.5
                res += 4 * (phialx / al - x * normal_density(al * x))  # sum no. 2

                for j in range(0, l, 1):  # from 0 to l - 1
                    aj = 2 * j + 1
                    res += 16 * (-1) ** (j + l) * (aj * al) / (al * al - aj * aj) * (
                                (normal_cdf(aj * x) - 0.5) / aj - phialx / al)
            return max(0.0, min(1.0, res))  # fix numerical errors

        return result
