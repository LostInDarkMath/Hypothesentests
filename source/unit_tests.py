# Copyright 2020 by Willi Sontopski. All rights reserved.

import unittest
from math import erf, sqrt, pi, exp
from typing import Callable
import numpy as np

# local file imports
from simulation.piecewise_linear_function import PiecewiseLinearFunction
from simulation.statistic_tools import get_cdf_uniform_with_eps_error
from statistical_tests.ln_test import LnTest


class UnitTests(unittest.TestCase):
    def test_affine_linear_function(self):
        points = [[0.3, 0.1], [0.5, 0.11], [0.8, 0.12], [0.9, 0.2]]
        f = PiecewiseLinearFunction(points)
        self.assertTrue(f.is_strictly_monotone_increasing())
        self.assertTrue(f.is_inverse_correct())

        for point in points:
            self.assertAlmostEqual(point[1], f.function(point[0]))

    def test_affine_linear_function_constant(self):
        points = [[0.3, 0.1], [0.5, 0.1], [0.8, 0.11], [0.9, 0.2]]
        self.assertRaises(ValueError, PiecewiseLinearFunction, points)

    def test_inverse_custom_cdf(self):
        epsilon = 0.1
        delta = 0.11
        position = 0.5
        cdf_1 = self.get_cdf_inverse(epsilon=epsilon, delta=delta, x_position=position)
        cdf_2 = get_cdf_uniform_with_eps_error(epsilon=epsilon, delta=delta, error_position=position).inverse

        x_axis = np.linspace(start=0.0, stop=1.0, num=1000, endpoint=False)
        for x in x_axis:
            self.assertAlmostEqual(cdf_1(x), cdf_2(x), places=8)

    @staticmethod
    def get_cdf_inverse(epsilon: float, delta: float, x_position: float) -> Callable[[float], float]:
        if delta < 0.0 or delta > 1.0 or x_position < 0.0 or x_position > 1.0 or delta <= abs(epsilon) or \
                epsilon < max(-x_position, x_position - 1) or epsilon > min(x_position, 1 - x_position):
            ValueError("illegal arguments")

        def f(x: float) -> float:
            if x < max(0, x_position - delta) or x > min(1, x_position + delta):
                return x
            elif max(0, x_position - delta) <= x and x <= x_position + epsilon:
                return (x - x_position - epsilon) / (1 + (epsilon / min(delta, x_position))) + x_position
            else:
                return (x - x_position - epsilon) / (1 - (epsilon / min(delta, 1 - x_position))) + x_position

        return f

    def test_ferger_cdf(self):
        max_iter = 200
        ferger_test = LnTest()
        cdf = ferger_test.get_cdf(max_iter=max_iter)
        cdf_old = self.ferger_get_cdf_old(max_iter=max_iter)
        x_axis = np.linspace(start=0.0, stop=5.0, num=100)
        for x in x_axis:
            self.assertAlmostEqual(cdf(x), cdf_old(x), places=5)

    @staticmethod
    def ferger_get_cdf_old(max_iter: int) -> Callable:
        """Return the Ferger 2018 distribution function
           This version is not optimized, but more readable. It is used to test the optimized version."""

        def Phi(x: float) -> float:
            """distribution function of the standard normal distribution"""
            return (1.0 + erf(x / sqrt(2.0))) / 2.0  # this is much faster than scipy.stats.norm.cdf(x)

        def phi(x: float) -> float:
            """density function of the standard normal distribution"""
            return exp(- x * x / 2) / sqrt(2 * pi)  # this is much faster then scipy.stats.norm.pdf(x)

        def sum_1(x: float) -> float:
            res = 0.0
            for l in range(1, max_iter + 1, 1):  # from 1 to max_iter
                for j in range(0, l, 1):  # from 0 to l - 1
                    aj = 2 * j + 1
                    al = 2 * l + 1
                    res += (-1) ** (j + l) * (aj * al) / (al * al - aj * aj) * (
                            (Phi(aj * x) - 0.5) / aj - (Phi(al * x) - 0.5) / al)
            return res

        def sum_2(x: float) -> float:
            res = 0.0
            for j in range(0, max_iter + 1, 1):
                aj = 2 * j + 1
                res += (Phi(aj * x) - 0.5) / aj - x * phi(aj * x)
            return res

        def result(x: float) -> float:
            if x <= 0:
                return 0.0
            return max(0.0, min(1.0, 16 * sum_1(x) + 4 * sum_2(x)))  # fix numerical errors

        return result


if __name__ == '__main__':
    unittest.main()
