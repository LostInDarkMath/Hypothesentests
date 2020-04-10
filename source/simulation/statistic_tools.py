# Copyright 2020 by Willi Sontopski. All rights reserved.

import numpy as np
from math import erf, sqrt, exp, pi
from typing import Callable, List

# local file imports
from simulation.piecewise_linear_function import PiecewiseLinearFunction


def get_distribution_function(list_of_points: List[List[float]]) -> PiecewiseLinearFunction:
    """Return a distribution function through the given points."""
    return PiecewiseLinearFunction(list_of_points)


def quantile_function(distribution_function: PiecewiseLinearFunction) -> Callable[[float], float]:
    """Return the quantile function to a distribution function."""
    return distribution_function.inverse


def get_random_values(distribution_function: PiecewiseLinearFunction, size: int) -> np.array:
    """Inverse transform sampling: Returns a vector of random values which corresponds to the distribution."""
    uniform_distributed_values = np.random.uniform(size=size)
    inverse = quantile_function(distribution_function)
    result = []
    for x in uniform_distributed_values:
        result.append(inverse(x))
    return np.array(result)


def get_cdf_uniform_with_eps_error(epsilon: float,
                                   error_position: float,
                                   delta: float = 1.0
                                   ) -> PiecewiseLinearFunction:
    """Returns a disturbed distribution function of the uniform distribution"""
    if epsilon < 0.0 or epsilon > 1.0 or delta < 0.0 or delta > 1.0 or error_position < 0.0 or error_position > 1.0:
        ValueError("Illegal arguments")

    points = [[error_position, min(error_position + epsilon, 1.0)],
              [max(error_position - delta, 0.0), max(error_position - delta, 0.0)],
              [min(error_position + delta, 1.0), min(error_position + delta, 1.0)]]
    func = PiecewiseLinearFunction(points)
    if not func.is_inverse_correct():
        print("Warning: inverse might not be correct!")
        func.plot()
    return func


def ecdf(data: np.array) -> Callable[[float], float]:
    """Return empirical cumulative distribution function."""
    sorted_data = np.sort(data)

    def result(v: float) -> float:
        return np.searchsorted(sorted_data, v, side='right') / data.size
    return result


def uep(data: np.array) -> Callable[[float], float]:
    """Return uniform empirical process."""
    def result(v: float):
        return sqrt(data.size) * (ecdf(data)(v) - v)
    return result


def normal_cdf(x: float) -> float:
    """distribution function of the standard normal distribution"""
    return (1.0 + erf(x / sqrt(2.0))) / 2.0  # this is much faster than scipy.stats.norm.cdf(x)


def normal_density(x: float) -> float:
    """density function of the standard normal distribution"""
    return exp(- x * x / 2) / sqrt(2 * pi)  # this is much faster then scipy.stats.norm.pdf(x)
