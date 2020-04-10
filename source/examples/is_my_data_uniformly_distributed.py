# Copyright 2020 by Willi Sontopski. All rights reserved.

# local file imports
from statistical_tests.ln_test import LnTest
from statistical_tests.ks_test import KsTest

my_data = [0.23209831, 0.31096291, 0.05139859, 0.69648799, 0.70084184, 0.54187119,
           0.25457916, 0.46355967, 0.46506956, 0.88873228]
significance_level = 0.1

# test my_data with the Kolmogorov Smirnov test
ks_test = KsTest(data_vector=my_data)
ks_test.do_test(alpha=significance_level)

# test my_data with the new Ln test
ln_test = LnTest(data_vector=my_data)
ln_test.do_test(alpha=significance_level)

