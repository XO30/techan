# import
import numpy as np
import pandas as pd
from datetime import datetime
from techan.core.candle_stick import CandleStick


class CandleStickFrame:
    def __init__(self, date_time: list, open: list, high: list, low: list, close: list, volume: list or None = None):
        date_time, open, high, low, close, volume = self._validate_input(date_time, open, high, low, close, volume)
        self.candle_sticks = [CandleStick(dt, o, h, l, c, v) for dt, o, h, l, c, v in
                              zip(date_time, open, high, low, close, volume)]
        self.df: pd.DataFrame = pd.DataFrame({"date_time": date_time, "open": open, "high": high, "low": low, "close": close, "volume": volume})
        self._bullish_count, self._bearish_count, self._doji_count = self._type_count()

    def __repr__(self):
        return f"CandleFrame({self.df})"

    def __str__(self):
        return f"{self.df}"

    def __len__(self):
        return len(self.candle_sticks)

    def __getitem__(self, index):
        return self.candle_sticks[index]

    def __iter__(self):
        return iter(self.candle_sticks)

    def __reversed__(self):
        return reversed(self.candle_sticks)

    @staticmethod
    def _validate_input(date_time: list, open: list, high: list, low: list, close: list, volume: list or None) -> tuple:
        """
        method to validate the input
        :param date_time: list, np.ndarray, or pd.Series of date_time of the candlesticks
        :param open: list, np.ndarray, or pd.pd.Series of open of the candlesticks
        :param high: list, np.ndarray, or pd.pd.Series of high of the candlesticks
        :param low: list, np.ndarray, or pd.pd.Series of low of the candlesticks
        :param close: list, np.ndarray, or pd.Series of close of the candlesticks
        :param volume: list, np.ndarray, or pd.Series of volume of the candlesticks or None
        :return: tuple: date_time, open, high, low, close, volume
        """
        if not isinstance(date_time, (list, np.ndarray, pd.Series)):
            raise TypeError("date_time must be list, np.ndarry, pd.Series not {}".format(type(date_time)))
        if not isinstance(open, (list, np.ndarray, pd.Series)):
            raise TypeError("open must be list, np.ndarry, or pd.Series not {}".format(type(open)))
        if not isinstance(high, (list, np.ndarray, pd.Series)):
            raise TypeError("high must be list, np.ndarry, or pd.Series not {}".format(type(high)))
        if not isinstance(low, (list, np.ndarray, pd.Series)):
            raise TypeError("low must be list, np.ndarry, or pd.Series not {}".format(type(low)))
        if not isinstance(close, (list, np.ndarray, pd.Series)):
            raise TypeError("close must be list, np.ndarry, or pd.Series not {}".format(type(close)))
        if not isinstance(volume, (list, np.ndarray, pd.Series, type(None))):
            raise TypeError("volume must be list, np.ndarry, pd.Series or NoneType not {}".format(type(volume)))
        date_time = list(date_time)
        open = list(open)
        high = list(high)
        low = list(low)
        close = list(close)
        volume = list(volume) if volume is not None else [None] * len(date_time)
        if len(date_time) != len(open) != len(high) or len(open) != len(low) or len(open) != len(close):
            raise ValueError("date_time, open, high, low, and close must be the same length")
        if not all(isinstance(x, (str, datetime)) for x in date_time):
            raise TypeError("date_time must be list of str or time.datetime not {}".format(type(date_time)))
        if not all(isinstance(x, (int, float)) for x in open):
            raise TypeError("open must be list of int or float not {}".format(type(open)))
        if not all(isinstance(x, (int, float)) for x in high):
            raise TypeError("high must be list of int or float not {}".format(type(high)))
        if not all(isinstance(x, (int, float)) for x in low):
            raise TypeError("low must be list of int or float not {}".format(type(low)))
        if not all(isinstance(x, (int, float)) for x in close):
            raise TypeError("close must be list of int or float not {}".format(type(close)))
        if not all(isinstance(x, (int, float, type(None))) for x in volume):
            raise TypeError("volume must be list of int, float or None not {}".format(type(volume)))
        return date_time, open, high, low, close, volume

    def _type_count(self) -> tuple:
        """
        method to count the number of bullish, bearish, and doji candlesticks
        :return: tuple: bullish, bearish, doji count
        """
        bullish: int = 0
        bearish: int = 0
        doji: int = 0
        for candle in self.candle_sticks:
            if candle.type() == 'bullish':
                bullish += 1
            elif candle.type() == 'bearish':
                bearish += 1
            elif candle.type() == 'doji':
                doji += 1
        return bullish, bearish, doji

    def _bullish_ratio(self) -> float:
        """
        method to calculate the ratio of bullish candlesticks
        :return: float: bullish ratio range [0, 1]
        """
        return self._bullish_count / len(self.candle_sticks)

    def _bearish_ratio(self) -> float:
        """
        method to calculate the ratio of bearish candlesticks
        :return: float: bearish ratio range [0, 1]
        """
        return self._bearish_count / len(self.candle_sticks)

    def _doji_ratio(self) -> float:
        """
        method to calculate the ratio of doji candlesticks
        :return: float: doji ratio range [0, 1]
        """
        return self._doji_count / len(self.candle_sticks)

    def type_ratio(self) -> str:
        """
        method to return the ratio of bullish, bearish, and doji candlesticks
        :return: str: bullish, bearish, and doji ratio
        """
        return 'bullish: {:.2f}, bearish: {:.2f}, doji: {:.2f}'.format(self._bullish_ratio(),
                                                                       self._bearish_ratio(),
                                                                       self._doji_ratio()
                                                                       )
