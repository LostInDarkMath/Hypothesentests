# Copyright 2020 by Willi Sontopski. All rights reserved.

from __future__ import annotations


class QuantileTableEntry:
    def __init__(self, alpha: float, value: float, epsilon: float, max_iter: int):
        self.alpha = alpha
        self.value = value
        self.epsilon = epsilon
        self.max_iter = max_iter

    def is_better_than(self, other: QuantileTableEntry) -> bool:
        return self.alpha == other.alpha and self.epsilon <= other.epsilon and self.max_iter >= other.max_iter

    def to_string(self, separator: str) -> str:
        return (str(self.alpha) + separator + str(self.value) + separator
                + str(self.epsilon) + separator + str(self.max_iter)).replace('.', ',')
