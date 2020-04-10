# Copyright 2020 by Willi Sontopski. All rights reserved.

# local file imports
from statistical_tests.statistical_test import StatisticalTest


class WrappedStatisticalTest:
    def __init__(self, test: StatisticalTest, critical_value: float):
        self.test = test
        self.critical_value = critical_value
        self.empirical_probability_h0_dismissed = dict()
