# Copyright 2020 by Willi Sontopski. All rights reserved.
import os
from typing import Union

# local file imports
from statistical_tests.quantile_table_entry import QuantileTableEntry


class QuantileTable:
    """Persists and manage quantiles"""
    def __init__(self, filename: str):
        self.filename = os.path.join('quantile_tables', filename.strip().strip(' ') + ".csv")
        self.quantiles = []
        self.separator = ';'
        self.load()

    def save(self) -> None:
        if "Vn" in self.filename:
            return
        try:
            with open(self.filename, 'w') as file:
                s = self.separator
                file.write('alpha' + s + "value" + s + "epsilon" + s + "max_iter\n")  # write headline
                for q in self.quantiles:
                    file.write(q.to_string(separator=self.separator) + '\n')
        except Exception as e:
            print(e)

    def load(self) -> None:
        if "Vn" in self.filename:
            return
        try:
            with open(self.filename, 'r') as file:
                content = file.readlines()
                content = [x.strip().replace(',', '.') for x in content]  # remove Linebreaks \n
                for line in content[1:]:
                    s = line.split(self.separator)
                    self.quantiles.append(QuantileTableEntry(round(float(s[0]), 10), float(s[1]), float(s[2]), int(s[3])))
        except Exception as e:
            print(e)

    def append(self, quantile: QuantileTableEntry) -> None:
        q = self.__get(quantile.alpha)

        if q is None:
            self.quantiles.append(quantile)
        elif quantile.is_better_than(q):
            self.quantiles[self.quantiles.index(q)] = quantile
        self.quantiles.sort(key=lambda x: x.alpha, reverse=False)  # keep list always sorted

    def get(self, alpha: float, epsilon: float, max_iter: int) -> Union[QuantileTableEntry, None]:
        q = self.__get(alpha)
        if q is None:
            return q
        if q.epsilon <= epsilon and q.max_iter >= max_iter:
            return q
        return None

    def __get(self, alpha: float) -> Union[QuantileTableEntry, None]:
        """Use binary search because self.quantiles is always sorted by alpha
        Return None if no such quantile is in the list."""
        left = 0
        right = len(self.quantiles) - 1

        while left <= right:
            mid = int(left + (right - left) / 2)

            if self.quantiles[mid].alpha == alpha:
                return self.quantiles[mid]
            elif self.quantiles[mid].alpha < alpha:
                left = mid + 1
            else:
                right = mid - 1
        return None  # If we reach here, then the element was not present

    def save_in_latex_format(self) -> None:
        decimal_places = 10
        try:
            with open(self.filename.strip('.csv') + '.tex', 'w') as file:
                file.writelines([
                    r"% !TEX root = masterarbeit.tex" + '\n',
                    r"\begin{tabular}{l|l||l|l||l|l}" + '\n',
                    r"$\alpha$ & $\alpha$-Quantil & $\alpha$ & $\alpha$-Quantil & $\alpha$ & $\alpha$-Quantil \\" + "\n",
                    r"\hline" + '\n'
                ])

                for i in range(1, 34):
                    alpha_1 = round(i * 0.01, 2)
                    alpha_2 = round(alpha_1 + 0.33, 2)
                    alpha_3 = round(alpha_1 + 0.66, 2)

                    file.write(
                        str(alpha_1) + ' & ' + str(round(self.__get(alpha_1).value, decimal_places)) + ' & ' +
                        str(alpha_2) + ' & ' + str(round(self.__get(alpha_2).value, decimal_places)) + ' & ' +
                        str(alpha_3) + ' & ' + str(round(self.__get(alpha_3).value, decimal_places)) + r"\\" + '\n'
                               )

                file.write(r"\end{tabular}")
        except Exception as e:
            print(e)
