# Copyright 2020 by Willi Sontopski. All rights reserved.
import time

# lokale Importe
from statistical_tests.ln_test import LnTest
from statistical_tests.vn_test import VnTest
from statistical_tests.ks_test import KsTest
from simulation.statistic_tools import get_cdf_uniform_with_eps_error
from simulation.monte_carlo import MonteCarloSimulation

# Parameter der Monte-Carlo-Simulation
####################################
n = 200                 # n = 10, 25, 50, 100, 500, 1000;  Länge der generierten Zufallsvektoren
m = 10**4               # m = 10 ** 4; Anzahl der Monte-Carlo-Iterationen der Simulation
alpha = 0.1             # alpha = 0.1; Signifikanzniveau
epsilon_max = 0.1       # error_max = 0.1; Maximalwert der Störung der Verteilungsfunktion der Gleichverteilung
fehlerposition = 0.5    # reelle Zahl zwischen 0.0 und 1.0; Der X-Wert, an welchem die Verteilungsfunktion gestört wird
delta = 0.11            # Breite der Störung der Verteilungsfunktion
aufloesung = 30         # Anzahl der Werte zwischen 0 und epsilon_max, mit welchen die Verteilungsfunktion gestört wird
#####################################

mon = MonteCarloSimulation(number_of_vectors=m, length_of_vector=n, alpha=alpha)

mon.add_test(KsTest(color='r'))
mon.add_test(VnTest(color='b'))
mon.add_test(LnTest(color='g'))

cdf = get_cdf_uniform_with_eps_error(epsilon=epsilon_max, error_position=fehlerposition, delta=delta)

print("Das Programm hält an, während der Plot angezeigt wird. Schließe den Plot zum Fortfahren.")
cdf.plot(title="Epsilon=" + str(epsilon_max) + "; Fehlerposition=" + str(fehlerposition) + "; Fehlerbreite=" + str(delta), print_benchmarks=False, with_inverse=True)

print("Das kann jetzt eine Weile dauern ... bitte warten...")
start_time = time.time()
mon.plot_quality_function(epsilon_max=epsilon_max, error_delta=delta, error_position=fehlerposition, resolution=aufloesung, print_benchmarks=False)
print("Fertig nach " + str((time.time() - start_time)/60) + " Minuten.")
