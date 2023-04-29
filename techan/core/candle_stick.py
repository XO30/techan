# import
import numpy as np
from datetime import datetime


# noinspection PyPropertyDefinition
class CandleStick:
    def __init__(
            self,
            date_time: str,
            open: float,
            high: float,
            low: float,
            close: float,
            volume: int or None = None,
            spread: int or None = None
    ):
        self.open: float = open
        self.high: float = high
        self.low: float = low
        self.close: float = close
        self.date_time: str = date_time
        self.volume: int or None = volume
        self.spread: int or None = spread
        self._validate_candle()

    def __repr__(self):
        return f"Candle({self.date_time}, {self.open}, {self.high}, {self.low}, {self.close}, {self.volume})"

    def __str__(self):
        return f"DT: {self.date_time}, O: {self.open}, H: {self.high}, L: {self.low}, C: {self.close}, V: {self.volume}"

    @property
    def date_time(self) -> str:
        """
        forwards the date and time of the candlestick
        :return: str: date and time
        """
        return self._date_time

    @property
    def open(self) -> float:
        """
        forwards the open price of the candlestick
        :return: float: open price
        """
        return self._open

    @property
    def high(self) -> float:
        """
        forwards the high of the candlestick
        :return: float: high
        """
        return self._high

    @property
    def low(self) -> float:
        """
        forwards the low of the candlestick
        :return: float: low
        """
        return self._low

    @property
    def close(self) -> float:
        """
        forwards the close price of the candlestick
        :return: float: close price
        """
        return self._close

    @property
    def volume(self) -> int or None:
        """
        forwards the open Volume of the candlestick
        :return: int: Volume
        """
        return self._volume

    @property
    def spread(self) -> int or None:
        """
        forwards the spread of the candlestick
        :return: int: spread
        """
        return self._spread

    @date_time.setter
    def date_time(self, value: str) -> None:
        """
        method to validate the date_time
        :param value: str: date_time
        :return: None
        """
        if not isinstance(value, (str, datetime)):
            raise TypeError("date_time must be str or datetime not {}".format(type(value)))
        self._date_time: str = value
        return None

    @open.setter
    def open(self, value: float) -> None:
        """
        method to validate the open price
        :param value: float: open price
        :return: None
        """
        if not isinstance(value, (int, float)):
            raise TypeError("open must be int or float not {}".format(type(value)))
        if value < 0:
            raise ValueError("open must be positive")
        self._open: float = value
        return None

    @high.setter
    def high(self, value: float) -> None:
        """
        method to validate the high
        :param value: float: high
        :return: None
        """
        if not isinstance(value, (int, float)):
            raise TypeError("high must be int or float not {}".format(type(value)))
        if value < 0:
            raise ValueError("high must be positive")
        self._high: float = value
        return None

    @low.setter
    def low(self, value: float) -> None:
        """
        method to validate the low
        :param value: float: low
        :return: None
        """
        if not isinstance(value, (int, float)):
            raise TypeError("low must be int or float not {}".format(type(value)))
        if value < 0:
            raise ValueError("Low must be positive")
        self._low: float = value
        return None

    @close.setter
    def close(self, value: float) -> None:
        """
        method to validate the close price
        :param value: float: close price
        :return: None
        """
        if not isinstance(value, (int, float)):
            raise TypeError("close must be int or float not {}".format(type(value)))
        if value < 0:
            raise ValueError("close must be positive")
        self._close: float = value
        return None

    @volume.setter
    def volume(self, value: int) -> None:
        """
        method to validate the volume
        :param value: int: volume
        :return: None
        """
        if not isinstance(value, (int, float, type(None))):
            raise TypeError("volume must be int, float or NoneType not {}".format(type(value)))
        if value is not None:
            if value < 0:
                raise ValueError("volume must be positive")
        self._volume: int or None = value
        return None

    @spread.setter
    def spread(self, value: int) -> None:
        """
        method to validate the spread
        :param value: int: spread
        :return: None
        """
        if not isinstance(value, (int, float, type(None))):
            raise TypeError("spread must be int, float or NoneType not {}".format(type(value)))
        if value is not None:
            if value < 0:
                raise ValueError("spread must be positive")
        self._spread: int or None = value
        return None

    def _validate_candle(self) -> None:
        """
        method to validate the candlestick
        :return: None
        """
        if self.open > self.high:
            raise ValueError("open cannot be greater than high")
        if self.open < self.low:
            raise ValueError("open cannot be less than low")
        if self.close > self.high:
            raise ValueError("close cannot be greater than high")
        if self.close < self.low:
            raise ValueError("close cannot be less than low")

    def type(self) -> str:
        """
        method to determine the type of the candlestick
        :return: str: type of the candlestick
        """
        if self.open < self.close:
            return 'bullish'
        elif self.open > self.close:
            return 'bearish'
        else:
            return 'doji'

    def cs_size(self) -> float:
        """
        method to determine the size of the candlestick
        :return: float: size of the candlestick
        """
        return abs(self.high - self.low)

    def upper_shadow_size(self) -> float:
        """
        method to determine the size of the upper shadow
        :return: float: size of the upper shadow
        """
        return self.high - max(self.open, self.close)

    def lower_shadow_size(self) -> float:
        """
        method to determine the size of the lower shadow
        :return: float: size of the lower shadow
        """
        return min(self.open, self.close) - self.low

    def body_size(self) -> float:
        """
        method to determine the size of the body
        :return: float: size of the body
        """
        return abs(self.close - self.open)

    def is_bullish(self) -> bool:
        """
        method to determine if the candlestick is bullish
        :return: bool: True if bullish, False otherwise
        """
        return self.type() == 'bullish'

    def is_bearish(self) -> bool:
        """
        method to determine if the candlestick is bearish
        :return: bool: True if bearish, False otherwise
        """
        return self.type() == 'bearish'

    def is_doji(self) -> bool:
        """
        method to determine if the candlestick is a doji
        :return: bool: True if doji, False otherwise
        """
        return self.type() == 'doji'

    def cs_body_ratio(self) -> float:
        """
        method to determine the ratio of the body to the candlestick
        :return: float: ratio of the body to the candlestick, range [0, 1]
        """
        return self.body_size() / self.cs_size() if self.cs_size() > 0 else 0

    def body_upper_shadow_ratio(self) -> float:
        """
        method to determine the ratio of the upper shadow to the body
        can be between 0 and infinity if the body is 0 (doji)
        shows how big the upper shadow is compared to the body size
        :return: float: ratio of the upper shadow to the body, range [0, ∞]
        """
        return self.upper_shadow_size() / self.body_size() if self.body_size() > 0 else np.inf

    def body_lower_shadow_ratio(self) -> float:
        """
        method to determine the ratio of the lower shadow to the body
        can be between 0 and infinity if the body is 0 (doji)
        shows how big the lower shadow is compared to the body size
        :return: float: ratio of the lower shadow to the body, range [0, ∞)
        """
        return self.lower_shadow_size() / self.body_size() if self.body_size() > 0 else np.inf

    def body_position(self) -> float:
        """
        method to determine the position of the body
        can be between -1 and 1
        -1 = body totally at the bottom of cs, 0 = middle, 1 = body totally at the top of cs
        :return: float: position of the body, range [-1, 1]
        """
        upper_shadow: float = self.high - max(self.open, self.close)
        lower_shadow: float = min(self.open, self.close) - self.low
        shadows: float = upper_shadow + lower_shadow
        # -1 = lower shadow, 0 = middle, 1 = upper shadow
        return (2 * lower_shadow) / shadows - 1 if shadows != 0 else 0
