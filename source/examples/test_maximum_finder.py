# Copyright 2020 by Willi Sontopski. All rights reserved.
from math import sqrt

import numpy as np

# local file imports
from statistical_tests.ks_test import KsTest
from plotting.plotting import FunctionToPlot, plot
from statistical_tests.vn_test import VnTest


def test_uep_max_argmax():
    test = KsTest()
    test.data = np.random.uniform(size=1000)
    argmax_abs, max_value_abs = test._get_uep_abs_max()
    argmax, max_value = test._get_uep_max()
    print('max', argmax, max_value)
    print('max abs', argmax_abs, max_value_abs)
    print(test.get_statistic())
    uep_abs = test.uep_abs()
    uep = test.uep()

    plot([FunctionToPlot(uep_abs, "|U_n|", 'r'),
          FunctionToPlot(uep, "U_n", 'k'),
          FunctionToPlot(lambda x: max_value, "max", 'b'),
          FunctionToPlot(lambda x: max_value_abs, "max_abs", 'g'),
          FunctionToPlot(lambda x: -max_value_abs, "max_abs", 'g'),
          ], resolution=10000)


def test_max_vn_test():
    def vn_plus(t: float) -> float:
        if t <= 0.0 or t >= 1.0:
            return 0.0  # avoid division by zero
        return test.uep()(t) / sqrt(t * (1 - t))

    def vn(t: float) -> float:
        if t <= 0.0 or t >= 1.0:
            return 0.0  # avoid division by zero
        return test.uep_abs()(t) / sqrt(t * (1 - t))

    test = VnTest()
    test.data = np.random.uniform(size=100)
    argmax_abs, max_value_abs = test._get_max_of_almost_piecewise_linear_function(vn)
    argmax, max_value = test._get_max_of_almost_piecewise_linear_function(vn_plus)
    print('max V_n^+', argmax, max_value)
    print('max V_n', argmax_abs, max_value_abs)
    print(test.get_statistic())
    uep_abs = test.uep_abs()
    uep = test.uep()

    plot([FunctionToPlot(uep_abs, "|U_n|", 'r'),
          FunctionToPlot(uep, "U_n", 'k'),
          FunctionToPlot(vn_plus, "V_n^+", 'c'),
          FunctionToPlot(vn, "V_n", 'y'),
          FunctionToPlot(lambda x: max_value, "max V_n^+", 'b'),
          FunctionToPlot(lambda x: max_value_abs, "max V_n", 'g'),
          FunctionToPlot(lambda x: -max_value_abs, "-max V_n", 'g'),
          ], resolution=1000)


if __name__ == "__main__":
    test_uep_max_argmax()
    test_max_vn_test()
