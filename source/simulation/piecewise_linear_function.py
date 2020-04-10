# Copyright 2020 by Willi Sontopski. All rights reserved.

from __future__ import annotations
import math
from typing import Callable, List

# local file imports
from plotting import plotting


class PiecewiseLinearFunction:
    def __init__(self, points: List[List[float]] = None):
        if points is None:
            points = []
        self.list_of_points = points.copy()

        # endpoints are mandatory
        if [0, 0] not in self.list_of_points:
            self.list_of_points.append([0, 0])
        if [1, 1] not in self.list_of_points:
            self.list_of_points.append([1, 1])

        self.list_of_points = sorted(self.list_of_points, key=lambda tup: tup[0])  # sort list by first element
        self.function = self.__get_affine_linear_function(self.list_of_points)
        self.inverse = self.__get_inverse_function()

        if not self.is_strictly_monotone_increasing():
            raise ValueError("Non-bijective functions cannot be inversed!")

    @staticmethod
    def __get_affine_linear_function_by_points(
            start_point: List[float],
            end_point: List[float]
    ) -> Callable[[float], float]:

        delta_x = end_point[0] - start_point[0]
        delta_y = end_point[1] - start_point[1]

        if delta_x == 0:
            increase = math.inf
            translation = start_point[0]
        else:
            increase = delta_y / delta_x
            translation = - 1 * start_point[0] * increase + start_point[1]

        def result(x: float) -> float:
            return increase * x + translation

        return result

    @staticmethod
    def __get_affine_linear_function(list_of_points: List[List[float]]) -> Callable[[float], float]:
        function_list = []

        for i in range(len(list_of_points) - 1):
            function_list.append(PiecewiseLinearFunction.__get_affine_linear_function_by_points(
                list_of_points[i], list_of_points[i + 1]
            ))

        def result(x: float) -> float:
            for j in range(len(list_of_points) - 1):
                if list_of_points[j][0] <= x < list_of_points[j + 1][0]:
                    return function_list[j](x)

        return result

    def plot(self,
             resolution: int = 1000,
             with_inverse: bool = True,
             with_idendity: bool = True,
             title: str = "Affine linear function",
             **kwargs
             ) -> None:
        functions = []
        if with_inverse:
            functions.append(plotting.FunctionToPlot(self.inverse, "f^{-1}", color='b'))
        if with_idendity:
            functions.append(plotting.FunctionToPlot(lambda x: x, "id", color='k'))
        functions.append(plotting.FunctionToPlot(self.function, "f", color='r'))
        plotting.plot(functions, x_min=0., x_max=1., resolution=resolution, title=title, **kwargs)

    def __get_inverse_function(self) -> Callable[[float], float]:
        inversed_points = []
        for p in self.list_of_points:
            inversed_points.append([p[1], p[0]])

        return self.__get_affine_linear_function(inversed_points)

    def is_strictly_monotone_increasing(self) -> bool:
        tmp = -1
        for x, y in self.list_of_points:
            if y <= tmp:
                return False
            tmp = y
        return True

    def is_inverse_correct(self, epsilon: float = 0.0001) -> bool:
        for i in range(0, 100):
            x_actual = i * 0.01
            x_expected = self.inverse(self.function(x_actual))
            if x_expected is None or abs(x_actual - x_expected) > epsilon:
                print("Inverse is not correct: x_actual=" + str(x_actual) + ", x_expected=" + str(x_expected))
                return False
        return True


if __name__ == "__main__":
    my_points = [[0.3, 0.1], [0.5, 0.1], [0.8, 0.1], [0.9, 0.2]]
    f = PiecewiseLinearFunction(my_points)
    f.plot()
