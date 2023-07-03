import numpy as np


class StandardScaler:
    def __init__(self, values: np.ndarray or list):
        self.mean: np.ndarray = np.mean(values)
        self.std: np.ndarray = np.std(values)

    def __call__(self, value: float) -> float:
        return (value - self.mean) / self.std

    def __repr__(self):
        return f'StandardScaler(mean={self.mean}, std={self.std})'

    def save(self, name: str, path: str) -> None:
        """
        Saves the mean and std to a file
        :param name: filename
        :param path: path to save
        :return: None
        """
        np.save(f'{path}/{name}.npy', np.array([self.mean, self.std]))

    def load(self, path: str) -> None:
        """
        Loads the mean and std from a file
        :param path: path to load from
        :return: None
        """
        self.mean, self.std = np.load(path)
        return None


class MinMaxScaler:
    def __init__(self, values: np.ndarray or list):
        self.min: np.ndarray = np.min(values)
        self.max: np.ndarray = np.max(values)

    def __call__(self, value: float) -> float:
        return (value - self.min) / (self.max - self.min)

    def __repr__(self):
        return f'MinMaxScaler(min={self.min}, max={self.max})'

    def save(self, name: str, path: str) -> None:
        """
        Saves the min and max to a file
        :param name: filename
        :param path: path to save
        :return: None
        """
        np.save(f'{path}/{name}.npy', np.array([self.min, self.max]))
        return None

    def load(self, path) -> None:
        """
        Loads the min and max from a file
        :param path: path to load from
        :return: None
        """
        self.min, self.max = np.load(path)
        return None
