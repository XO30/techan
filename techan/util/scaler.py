import numpy as np


class StandardScaler:
    def __init__(self, values):
        self.mean = np.mean(values)
        self.std = np.std(values)

    def __call__(self, value):
        return (value - self.mean) / self.std

    def __repr__(self):
        return f'StandardScaler(mean={self.mean}, std={self.std})'


class MinMaxScaler:
    def __init__(self, values):
        self.min = np.min(values)
        self.max = np.max(values)

    def __call__(self, value):
        return (value - self.min) / (self.max - self.min)

    def __repr__(self):
        return f'MinMaxScaler(min={self.min}, max={self.max})'
