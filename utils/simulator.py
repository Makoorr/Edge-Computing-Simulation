import random

class Simulator:
    Factors = [-1, 1]

    def __init__(self, seed: int, mean: float, standard_deviation: float):
        self._random = random.Random(seed)
        self._mean = mean
        self._standard_deviation = abs(standard_deviation)
        self._step_size_factor = self._standard_deviation / 10
        self._value = self._mean - self._random.random()

    def calculate_next_value(self) -> float:
        value_change = self._random.random() * self._step_size_factor
        factor = self.Factors[self.decide_factor()]
        
        self._value += value_change * factor
        return self._value

    def decide_factor(self) -> int:
        if self._value > self._mean:
            distance = self._value - self._mean
            continue_direction = 1
            change_direction = 0
        else:
            distance = self._mean - self._value
            continue_direction = 0
            change_direction = 1

        chance = (self._standard_deviation / 2) - (distance / 50)
        random_value = self._random.random() * self._standard_deviation

        return continue_direction if random_value < chance else change_direction