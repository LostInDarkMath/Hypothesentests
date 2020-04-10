# Copyright 2020 by Willi Sontopski. All rights reserved.
import sys
from math import sqrt
from typing import Callable, Union, List
import numpy as np
from abc import ABC, abstractmethod

# local file imports
from plotting.plotting import plot, FunctionToPlot
from statistical_tests.quantile_table import QuantileTable
from statistical_tests.quantile_table_entry import QuantileTableEntry


class StatisticalTest(ABC):
    _data = np.array([])  # a vector of random values

    def __init__(self, data_vector: Union[np.array, List[float]] = None, color: str = 'r'):
        if data_vector is None:
            data_vector = np.array([])

        self.data = np.asarray(data_vector)
        self.color = color
        self._quantile_table = QuantileTable(self.get_name())
        super().__init__()

    @property
    def data(self) -> np.array:
        return self._data

    @data.setter
    def data(self, data_vector: np.array) -> None:
        self._data = np.asarray(data_vector)
        self.data_sorted = np.sort(self.data)
        self.n = self.data.size

    @abstractmethod
    def get_statistic(self) -> float:
        pass

    @abstractmethod
    def get_cdf(self, max_iter: int) -> Callable[[float], float]:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    def do_test(self, alpha: float, printing: bool = True) -> bool:
        """Return true iff H0 is dismissed. So true means, that the data is not uniformly distributed."""
        t_n = self.get_statistic()
        c_alpha = self.get_critical_value(alpha)

        if printing:
            if t_n > c_alpha:
                print(self.get_name() + ": H0 dismissed, because Tn = " + str(t_n) + " > " + str(c_alpha)
                      + "= c_alpha. Therefore, the data is not uniformly distributed.")
            else:
                print(self.get_name() + ": H0 accepted, because Tn = " + str(t_n) + " <= " + str(
                    c_alpha) + " = c_alpha. Therefore, the data is uniformly distributed")
        return t_n > c_alpha

    def get_quantile(self, quantile: float, epsilon: float, max_iter: int) -> float:
        if quantile <= 0 or quantile >= 1:
            raise ValueError("parameter alpha must be between 0 and 1")
        if epsilon < 0:
            raise ValueError("parameter epsilon must be between 0 and 1")

        q = self._quantile_table.get(alpha=quantile, epsilon=epsilon, max_iter=max_iter)
        if q is None:
            new = self.__calculate_quantile(quantile, epsilon, max_iter)
            self._quantile_table.append(QuantileTableEntry(alpha=quantile, value=new, epsilon=epsilon, max_iter=max_iter))
            return new
        else:
            return q.value

    def __calculate_quantile(self, alpha: float, epsilon: float, max_iter: int) -> float:
        quantile = 0.5
        df = self.get_cdf(max_iter)

        while True:
            alpha_approx = df(quantile)
            if abs(alpha_approx - alpha) < epsilon:
                return quantile
            quantile -= alpha_approx - alpha

    def get_critical_value(self, alpha: float, epsilon: float = 0.0001, max_iter: int = 100, n: int = -1) -> float:
        return self.get_quantile(1 - alpha, epsilon=epsilon, max_iter=max_iter)

    def plot_cdf(self,
                 max_iter: int = 100,
                 x_min: float = 0.0,
                 x_max: float = 3.0,
                 resolution: int = 1000) -> None:
        """Plots the cumulative distribution function of the corresponding statistics."""
        f = FunctionToPlot(self.get_cdf(max_iter), label="F(x)", color=self.color)
        plot([f], x_min=x_min, x_max=x_max, resolution=resolution,
             title="cumulative distribution function of the " + self.get_name()
             )

    def plot_uep(self,
                 x_min: float = 0.0,
                 x_max: float = 1.0,
                 resolution: int = 1000,
                 max_value: float = 0.0
                 ) -> None:
        """Plots the uniform empirical process of the given data."""
        funcs = [FunctionToPlot(self.uep(), label="F(x)", color=self.color)]
        if max_value > 0.0:
            funcs.append(FunctionToPlot(lambda x: max_value, label='max'))
        plot(funcs, x_min=x_min, x_max=x_max, resolution=resolution, title="uniform empirical process")

    def plot_uep_abs(self,
                     x_min: float = 0.0,
                     x_max: float = 1.0,
                     resolution: int = 1000,
                     max_value: float = 0.0
                     ) -> None:
        """Plots the reflected uniform empirical process of the given data."""
        funcs = [FunctionToPlot(self.uep_abs(), label="|U_n|", color=self.color)]
        if max_value > 0.0:
            funcs.append(FunctionToPlot(lambda x: max_value, label='max'))
        plot(funcs, x_min=x_min, x_max=x_max, resolution=resolution, title="uniform empirical process")

    def ecdf(self) -> Callable[[float], float]:
        """Return empirical cumulative distribution function."""
        if self._data.size == 0:
            raise ValueError("there is no data")

        def result(v: float) -> float:
            return np.searchsorted(self.data_sorted, v, side='right') / self.n

        return result

    def uep(self) -> Callable[[float], float]:
        """Return the uniform empirical process."""

        def result(x: float) -> float:
            return sqrt(self.n) * (self.ecdf()(x) - x)

        return result

    def uep_abs(self) -> Callable[[float], float]:
        """Return absolute value of the uniform empirical process."""

        def result(x: float) -> float:
            return abs(self.uep()(x))

        return result

    def _get_uep_max(self) -> (float, float):
        return self._get_max_of_almost_piecewise_linear_function(self.uep())

    def _get_uep_abs_max(self) -> (float, float):
        return self._get_max_of_almost_piecewise_linear_function(self.uep_abs())

    def _get_max_of_almost_piecewise_linear_function(self, function: Callable[[float], float]) -> (float, float):
        """Returns argmax and maximum value of a functional of the uniform empirical process"""
        max_value = sys.float_info.min
        argmax = 0.0
        epsilon = 1 / (self.n * 10 ** 6)
        for i in range(self.n):
            data_i = self.data_sorted.item(i)
            fx1 = function(data_i)
            fx2 = function(data_i + epsilon)
            fx3 = function(data_i - epsilon)
            if fx1 > max_value:
                max_value = fx1
                argmax = data_i
            if fx2 > max_value:
                max_value = fx2
                argmax = data_i + epsilon
            if fx3 > max_value:
                max_value = fx3
                argmax = data_i - epsilon
        return argmax, max_value

    def generate_quantile_table(self, resolution: int, epsilon: float, max_iter: int) -> None:
        alphas = np.linspace(0., 1., resolution, endpoint=False)
        for alpha in alphas[1:]:
            rounded_alpha = round(alpha, 10)  # remove numerical error
            q = self.get_quantile(quantile=rounded_alpha, epsilon=epsilon, max_iter=max_iter)
            print("alpha:", rounded_alpha, "Quantil:", q)
        self.save_quantile_table()

    def save_quantile_table(self) -> None:
        self._quantile_table.save()
