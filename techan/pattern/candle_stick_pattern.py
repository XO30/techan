# import
import numpy as np
import pandas as pd
from tqdm import tqdm
from typing import List
from techan.core.candle_stick import CandleStick
from techan.core.candle_stick_frame import CandleStickFrame
from techan.util.param import Parameter


class CandleStickPattern:
    def __init__(self, candle_stick_frame: CandleStickFrame):
        self.candle_stick_frame = self._validate_csf(candle_stick_frame)

    @staticmethod
    def _validate_csf(candle_stick_frame: CandleStickFrame):
        """
        method to validate the candle stick frame
        :param candle_stick_frame: CandleStickFrame: candle stick frame to validate
        :return: CandleStickFrame: validated candle stick frame
        """
        if not isinstance(candle_stick_frame, CandleStickFrame):
            raise TypeError("candle_stick_frame must be CandleStickFrame not {}".format(type(candle_stick_frame)))
        if len(candle_stick_frame) < 1:
            raise ValueError("candle_stick_frame must have at least 1 candle stick")
        return candle_stick_frame

    def _prepare_window(self, index: int, window: int) -> CandleStickFrame:
        """
        method to prepare the window for the candle stick frame
        :param index: int: index of the candle stick
        :param window: int: window to look back
        :return: CandleStickFrame: window of candle sticks
        """
        if window < 1:
            raise ValueError("window must be greater than 0")
        if window > len(self.candle_stick_frame):
            raise ValueError("window must be less than or equal to the length of the candle stick frame")
        return self.candle_stick_frame[index-window:index]

    def z_score_cs(self, index: int, window: int = 10) -> None or List[float]:
        """
        method to calculate the z score of the candle sticks in the window
        cs size normal scaled in respect to the cs of the candle sticks in the window
        can be in range [-inf, inf] with a mean of 0 and standard deviation of 1
        :param index: int: index of the candle stick to calculate the z score of
        :param window: int: window to calculate the z score over
        :return: list of float or None: z score of the candle sticks of the window [-inf, inf]
        """
        cs_window = self._prepare_window(index, window)
        if len(cs_window) < window or index < 0:
            return None
        else:
            mean = np.mean([cs.cs_size() for cs in cs_window])
            std = np.std([cs.cs_size() for cs in cs_window])
            # cs size normal scaled in respect to the cs of the candle sticks in the window
            scaled_cs = list(map(lambda cs: (cs.cs_size() - mean) / std, cs_window))
            return scaled_cs

    def z_score_body(self, index: int, window: int = 11) -> None or List[float]:
        """
        method to calculate the z score of the bodies in the window
        body size normal scaled in respect to the bodies of the candle sticks in the window
        can be in range [-inf, inf] with a mean of 0 and standard deviation of 1
        :param index: int: index of the candle stick to calculate the z score of
        :param window: int: window to calculate the z score over
        :return: list of float or None: z score of the bodies of the window [-inf, inf]
        """
        # the current cs should be included in the window -> += 1
        index += 1
        cs_window = self._prepare_window(index, window)
        if len(cs_window) < window or index < 0:
            return None
        else:
            mean = np.mean([cs.body_size() for cs in cs_window])
            std = np.std([cs.body_size() for cs in cs_window])
            # body size normal scaled in respect to the bodies of the candle sticks in the window
            scaled_bodies = list(map(lambda cs: (cs.body_size() - mean) / std, cs_window))
            return scaled_bodies

    def min_max_cs(self, index: int, window: int = 11) -> None or List[float]:
        """
        method to calculate the min max of the candle sticks in the window
        cs size min max scaled in respect to the cs of the candle sticks in the window
        can be in range [0, 1]
        :param index: int: index of the candle stick to calculate the min max of
        :param window: int: window to calculate the min max over
        :return: list of float or None: min max of the candle sticks in the window [0, 1]
        """
        # the current cs should be included in the window -> += 1
        index += 1
        cs_window = self._prepare_window(index, window)
        if len(cs_window) < window or index < 0:
            return None
        else:
            min = np.min([cs.cs_size() for cs in cs_window])
            max = np.max([cs.cs_size() for cs in cs_window])
            # cs size min max scaled in respect to the cs of the candle sticks in the window
            scaled_cs = list(map(lambda cs: (cs.cs_size() - min) / (max - min), cs_window))
            return scaled_cs

    def min_max_body(self, index: int, window: int = 11) -> None or List[float]:
        """
        method to calculate the min max of the bodies in the window
        body size min max scaled in respect to the bodies of the candle sticks in the window
        can be in range [0, 1]
        :param index: int: index of the candle stick to calculate the min max of
        :param window: int: window to calculate the min max over
        :return: list of float or None: min max of the bodies in the Window [0, 1]
        """
        # the current cs should be included in the window -> += 1
        index += 1
        cs_window = self._prepare_window(index, window)
        if len(cs_window) < window or index < 0:
            return None
        else:
            min = np.min([cs.body_size() for cs in cs_window])
            max = np.max([cs.body_size() for cs in cs_window])
            # body size min max scaled in respect to the bodies of the candle sticks in the window
            scaled_bodies = list(map(lambda cs: (cs.body_size() - min) / (max - min), cs_window))
            return scaled_bodies

    def trend(self, index: int, window: int = 10) -> None or float:
        """
        method to calculate the trend of the candle stick at index
        can be in range [-1, 1] with -1 being down and 1 being up
        :param index: int: index of the candle stick to calculate the trend of
        :param window: int: window to calculate the trend over
        :return: float or None: trend of the candle stick at index [-1, 1]
        """
        cs_window = self._prepare_window(index, window)
        if len(cs_window) < window or index < 0:
            return None
        trend, sum = 0, 0
        for cs in cs_window:
            sum += cs.cs_size()
            if cs.type() == 'bullish':
                trend += cs.cs_size()
            elif cs.type() == 'bearish':
                trend -= cs.cs_size()
        # weighted average of the trend
        return trend / sum

    class PatternTemplate:
        def __init__(self, param: dict, pattern_name: str, pattern_type: str, trend_strength: float, pattern: list):
            self.param = param
            self.pattern_name = pattern_name
            self.pattern_type = pattern_type
            self.trend_strength = trend_strength
            self.pattern = pattern
            self.is_pattern = False
            self.is_valid = None

        def __str__(self):
            return f'{self.pattern_name} -> ({self.is_pattern})'

        def __repr__(self):
            return f'{self.pattern_name} -> ({self.is_pattern})'



    # Bullish Reversal Candlestick Patterns classes:
    # Hammer (1)
    class Hammer(PatternTemplate):
        def __init__(self, trend: float, cs: CandleStick, param: dict):
            super().__init__(param, 'Hammer', 'bullish', trend, [cs])
            self._cs = cs
            self.is_pattern = self._is_hammer()

        def _is_hammer(self) -> None or bool:
            """
            method to check if the candle stick is a hammer
            :return: bool: True if the candle stick is a hammer, False otherwise
            """
            if self.trend_strength is None:
                return None
            con_01: bool = self.trend_strength <= self.param['trend_strength']
            con_02: bool = self._cs.type() == 'bullish'
            con_03: bool = self._cs.body_position() >= self.param['cs_body_position']
            con_04: bool = self._cs.body_lower_shadow_ratio() >= self.param['body_ls_ratio']
            con_05: bool = self._cs.body_upper_shadow_ratio() <= self.param['body_us_ratio']
            if con_01 and con_02 and con_03 and con_04 and con_05:
                return True
            return False

    # Bullish Piercing (2)
    class Piercing(PatternTemplate):
        def __init__(self, trend: float, cs: CandleStick, cs_m1: CandleStick, param: dict):
            super().__init__(param, 'Piercing', 'bullish', trend, [cs_m1, cs])
            self._cs = cs
            self._cs_m1 = cs_m1
            self.is_pattern = self._is_piercing()

        def _is_piercing(self) -> None or bool:
            """
            method to check if the candle stick is a piercing
            :return: bool: True if the candle stick is a piercing, False otherwise
            """
            if self.trend_strength is None:
                return None
            con_01: bool = self.trend_strength <= self.param['trend_strength']
            con_02: bool = self._cs.type() == 'bullish'
            con_03: bool = self._cs_m1.type() == 'bearish'
            con_04: bool = self._cs.open < self._cs_m1.close
            con_05: bool = self._cs_m1.open - self._cs_m1.body_size() / 2 < self._cs.close < self._cs_m1.open
            if con_01 and con_02 and con_03 and con_04 and con_05:
                return True
            return False

    # Bullish Engulfing (3)
    class BullishEngulfing(PatternTemplate):
        def __init__(self, trend: float, cs: CandleStick, cs_m1: CandleStick, param: dict):
            super().__init__(param, 'BullishEngulfing', 'bullish', trend, [cs_m1, cs])
            self._cs = cs
            self._cs_m1 = cs_m1
            self.is_pattern = self._is_bullish_engulfing()

        def _is_bullish_engulfing(self) -> None or bool:
            """
            method to check if the candle stick is a bullish engulfing
            :return: bool: True if the candle stick is a bullish engulfing, False otherwise
            """
            if self.trend_strength is None:
                return None
            con_01: bool = self.trend_strength <= self.param['trend_strength']
            con_02: bool = self._cs.type() == 'bullish'
            con_03: bool = self._cs_m1.type() == 'bearish'
            con_04: bool = self._cs.open < self._cs_m1.close
            con_05: bool = self._cs.close > self._cs_m1.open
            if con_01 and con_02 and con_03 and con_04 and con_05:
                return True
            return False

    # Morning Star (4)
    class MorningStar(PatternTemplate):
        def __init__(self, trend: float, relative_size: list, cs: CandleStick, cs_m1: CandleStick, cs_m2: CandleStick, param: dict):
            super().__init__(param, 'MorningStar', 'bullish', trend, [cs_m2, cs_m1, cs])
            self._relative_size = relative_size
            self._cs = cs
            self._cs_m1 = cs_m1
            self._cs_m2 = cs_m2
            self.is_pattern = self._is_morning_star()

        def _is_morning_star(self) -> None or bool:
            """
            method to check if the candle stick is a morning star
            :return: bool: True if the candle stick is a morning star, False otherwise
            """
            if self.trend_strength is None:
                return None
            con_01: bool = self.trend_strength <= self.param['trend_strength']
            con_02: bool = self._cs_m2.type() == 'bearish'
            con_03: bool = self._cs_m2.cs_body_ratio() >= self.param['cs_m2_body_ratio']
            con_04: bool = self._relative_size[-3] >= self.param['cs_m2_relative_size']
            con_05: bool = self._cs_m1.cs_body_ratio() <= self.param['cs_m1_body_ratio']
            con_06: bool = self._cs.type() == 'bullish'
            con_07: bool = self._cs.cs_body_ratio() >= self.param['cs_body_ratio']
            con_08: bool = self._relative_size[-1] >= self.param['cs_relative_size']
            if con_01 and con_02 and con_03 and con_04 and con_05 and con_06 and con_07 and con_08:
                return True
            return False

    # Three White Soldiers (5)
    class ThreeWhiteSoldiers(PatternTemplate):
        def __init__(self, trend: float, relative_size: list, cs: CandleStick, cs_m1: CandleStick, cs_m2: CandleStick, param: dict):
            super().__init__(param, 'ThreeWhiteSoldiers', 'bullish', trend, [cs_m2, cs_m1, cs])
            self._relative_size = relative_size
            self._cs = cs
            self._cs_m1 = cs_m1
            self._cs_m2 = cs_m2
            self.is_pattern = self._is_three_white_soldiers()

        def _is_three_white_soldiers(self) -> None or bool:
            """
            method to check if the candle stick is a three white soldiers
            :return: bool: True if the candle stick is a three white soldiers, False otherwise
            """
            if self.trend_strength is None:
                return None
            con_1: bool = self.trend_strength <= self.param['trend_strength']
            con_2: bool = self._cs_m2.type() == 'bullish'
            con_3: bool = self._cs_m2.cs_body_ratio() >= self.param['cs_m2_body_ratio']
            con_4: bool = self._relative_size[-3] >= self.param['cs_m2_relative_size']
            con_5: bool = self._cs_m1.type() == 'bullish'
            con_6: bool = self._cs_m1.cs_body_ratio() >= self.param['cs_m1_body_ratio']
            con_7: bool = self._relative_size[-2] >= self.param['cs_m1_relative_size']
            con_8: bool = self._cs.type() == 'bullish'
            con_9: bool = self._cs.cs_body_ratio() >= self.param['cs_body_ratio']
            con_10: bool = self._relative_size[-1] >= self.param['cs_relative_size']
            if con_1 and con_2 and con_3 and con_4 and con_5 and con_6 and con_7 and con_8 and con_9 and con_10:
                return True
            return False

    # Bullish Marubozu (6)
    class BullishMarubozu(PatternTemplate):
        def __init__(self, trend: float, relative_size: list, cs: CandleStick, param: dict):
            super().__init__(param, 'BullishMarubozu', 'bullish', trend, [cs])
            self._relative_size = relative_size
            self._cs = cs
            self.is_pattern = self._is_bullish_marubozu()

        def _is_bullish_marubozu(self) -> None or bool:
            """
            method to check if the candle stick is a bullish marubozu
            :return: bool: True if the candle stick is a bullish marubozu, False otherwise
            """
            if self.trend_strength is None:
                return None
            con_01: bool = self.trend_strength <= self.param['trend_strength']
            con_02: bool = self._cs.type() == 'bullish'
            con_03: bool = self._cs.cs_body_ratio() >= self.param['cs_body_ratio']
            con_04: bool = self._relative_size[-1] >= self.param['cs_relative_size']
            if con_01 and con_02 and con_03 and con_04:
                return True
            return False

    # Three Inside Up (7)
    class ThreeInsideUp(PatternTemplate):
        def __init__(self, trend: float, relative_size: list, cs: CandleStick, cs_m1: CandleStick, cs_m2: CandleStick, param: dict):
            super().__init__(param, 'ThreeInsideUp', 'bullish', trend, [cs_m2, cs_m1, cs])
            self._relative_size = relative_size
            self._cs = cs
            self._cs_m1 = cs_m1
            self._cs_m2 = cs_m2
            self.is_pattern = self._is_three_inside_up()

        def _is_three_inside_up(self) -> None or bool:
            """
            method to check if the candle stick is a three inside up
            :return: bool: True if the candle stick is a three inside up, False otherwise
            """
            if self.trend_strength is None:
                return None
            con_01: bool = self.trend_strength <= self.param['trend_strength']
            con_02: bool = self._cs_m2.type() == 'bearish'
            con_03: bool = self._cs_m2.cs_body_ratio() >= self.param['cs_m2_body_ratio']
            con_04: bool = self._relative_size[-3] >= self.param['cs_m2_relative_size']
            con_05: bool = self._cs_m1.type() == 'bullish'
            con_06: bool = self._cs_m1.open <= self._cs_m2.close
            con_07: bool = self._cs.type() == 'bullish'
            con_08: bool = self._cs.cs_body_ratio() >= self.param['cs_body_ratio']
            con_09: bool = self._relative_size[-1] >= self.param['cs_relative_size']
            con_10: bool = self._cs.open >= self._cs_m1.close
            if con_01 and con_02 and con_03 and con_04 and con_05 and con_06 and con_07 and con_08 and con_09 and con_10:
                return True
            return False

    # Bullish Harami (8)
    class BullishHarami(PatternTemplate):
        def __init__(self, trend: float, relative_size: list, cs: CandleStick, cs_m1: CandleStick, param: dict):
            super().__init__(param, 'BullishHarami', 'bullish', trend, [cs_m1, cs])
            self._relative_size = relative_size
            self._cs = cs
            self._cs_m1 = cs_m1
            self.is_pattern = self._is_bullish_harami()

        def _is_bullish_harami(self) -> None or bool:
            """
            method to check if the candle stick is a bullish harami
            :return: bool: True if the candle stick is a bullish harami, False otherwise
            """
            if self.trend_strength is None:
                return None
            con_01: bool = self.trend_strength <= self.param['trend_strength']
            con_02: bool = self._cs_m1.type() == 'bearish'
            con_03: bool = self._cs_m1.cs_body_ratio() >= self.param['cs_m1_body_ratio']
            con_04: bool = self._relative_size[-2] >= self.param['cs_m1_relative_size']
            con_05: bool = self._cs.type() == 'bullish'
            con_06: bool = self._cs.cs_body_ratio() >= self.param['cs_body_ratio']
            con_07: bool = self._relative_size[-1] <= self.param['cs_relative_size']
            con_08: bool = self._cs.open >= self._cs_m1.close
            con_09: bool = self._cs.close <= self._cs_m1.open
            if con_01 and con_02 and con_03 and con_04 and con_05 and con_06 and con_07 and con_08 and con_09:
                return True
            return False

    # Tweezer Bottom (9)
    class TweezerBottom(PatternTemplate):
        def __init__(self, trend: float, relative_size: list, cs: CandleStick, cs_m1: CandleStick, param: dict):
            super().__init__(param, 'TweezerBottom', 'bullish', trend, [cs, cs_m1])
            self._relative_size = relative_size
            self._cs = cs
            self._cs_m1 = cs_m1
            self.is_pattern = self._is_tweezer_bottom()

        def _is_tweezer_bottom(self) -> None or bool:
            """
            method to check if the candle stick is a tweezer bottom
            :return: bool: True if the candle stick is a tweezer bottom, False otherwise
            """
            if self.trend_strength is None:
                return None
            con_01: bool = self.trend_strength <= self.param['trend_strength']
            con_02: bool = self._cs_m1.type() == 'bearish'
            con_03: bool = self._cs_m1.cs_body_ratio() >= self.param['cs_m1_body_ratio']
            con_04: bool = self._relative_size[-2] >= self.param['cs_m1_relative_size']
            con_05: bool = self._cs.type() == 'bullish'
            con_06: bool = self._cs.cs_body_ratio() <= self.param['cs_body_ratio']
            con_07: bool = self._cs.body_position() <= self.param['cs_body_position']
            if con_01 and con_02 and con_03 and con_04 and con_05 and con_06 and con_07:
                return True
            return False


    # Bearish Reversal Candlestick Patterns Classes:
    # Hanging Man (14)
    class HangingMan(PatternTemplate):
        def __init__(self, trend: float, cs: CandleStick, param: dict):
            super().__init__(param, 'HangingMan', 'bearish', trend, [cs])
            self._cs = cs
            self.is_pattern = self._is_hanging_man()

        def _is_hanging_man(self) -> None or bool:
            """
            method to check if the candle stick is a hanging man
            :return: bool: True if the candle stick is a hanging man, False otherwise
            """
            if self.trend_strength is None:
                return None
            con_01: bool = self.trend_strength >= self.param['trend_strength']
            con_02: bool = self._cs.type() == 'bearish'
            con_03: bool = self._cs.body_position() <= self.param['cs_body_position']
            con_04: bool = self._cs.body_lower_shadow_ratio() <= self.param['body_ls_ratio']
            con_05: bool = self._cs.body_upper_shadow_ratio() >= self.param['body_us_ratio']
            if con_01 and con_02 and con_03 and con_04 and con_05:
                return True
            return False

    # Dark Cloud (15)
    class DarkCloud(PatternTemplate):
        def __init__(self, trend: float, cs: CandleStick, cs_m1: CandleStick, param: dict):
            super().__init__(param, 'DarkCloud', 'bearish', trend, [cs_m1, cs])
            self._cs = cs
            self._cs_m1 = cs_m1
            self.is_pattern = self._is_dark_cloud()

        def _is_dark_cloud(self) -> None or bool:
            """
            method to check if the candle stick is a dark cloud
            :return: bool: True if the candle stick is a dark cloud, False otherwise
            """
            if self.trend_strength is None:
                return None
            con_01: bool = self.trend_strength >= self.param['trend_strength']
            con_02: bool = self._cs.type() == 'bearish'
            con_03: bool = self._cs_m1.type() == 'bullish'
            con_04: bool = self._cs.open > self._cs_m1.close
            con_05: bool = self._cs_m1.open + self._cs_m1.body_size() / 2 > self._cs.close > self._cs_m1.open
            if con_01 and con_02 and con_03 and con_04 and con_05:
                return True
            return False

    # Bearish Engulfing (16)
    class BearishEngulfing(PatternTemplate):
        def __init__(self, trend: float, cs: CandleStick, cs_m1: CandleStick, param: dict):
            super().__init__(param, 'BearishEngulfing', 'bearish', trend, [cs_m1, cs])
            self._cs = cs
            self._cs_m1 = cs_m1
            self.is_pattern = self._is_bearish_engulfing()

        def _is_bearish_engulfing(self) -> None or bool:
            """
            method to check if the candle stick is a bearish engulfing
            :return: bool: True if the candle stick is a bearish engulfing, False otherwise
            """
            if self.trend_strength is None:
                return None
            con_01: bool = self.trend_strength >= self.param['trend_strength']
            con_02: bool = self._cs.type() == 'bearish'
            con_03: bool = self._cs_m1.type() == 'bullish'
            con_04: bool = self._cs.open > self._cs_m1.close
            con_05: bool = self._cs.close < self._cs_m1.open
            if con_01 and con_02 and con_03 and con_04 and con_05:
                return True
            return False

    # Evening Star (17)
    class EveningStar(PatternTemplate):
        def __init__(self, trend: float, relative_size: list, cs: CandleStick, cs_m1: CandleStick, cs_m2: CandleStick, param: dict):
            super().__init__(param, 'EveningStar', 'bearish', trend, [cs_m2, cs_m1, cs])
            self._relative_size = relative_size
            self._cs = cs
            self._cs_m1 = cs_m1
            self._cs_m2 = cs_m2
            self.is_pattern = self._is_evening_star()

        def _is_evening_star(self) -> None or bool:
            """
            method to check if the candle stick is an evening star
            :return: bool: True if the candle stick is an evening star, False otherwise
            """
            if self.trend_strength is None:
                return None
            con_01: bool = self.trend_strength >= self.param['trend_strength']
            con_02: bool = self._cs_m2.type() == 'bullish'
            con_03: bool = self._cs_m2.cs_body_ratio() >= self.param['cs_m2_body_ratio']
            con_04: bool = self._relative_size[-3] >= self.param['cs_m2_relative_size']
            con_05: bool = self._cs_m1.cs_body_ratio() <= self.param['cs_m1_body_ratio']
            con_06: bool = self._cs.type() == 'bearish'
            con_07: bool = self._cs.cs_body_ratio() >= self.param['cs_body_ratio']
            con_08: bool = self._relative_size[-1] >= self.param['cs_relative_size']
            if con_01 and con_02 and con_03 and con_04 and con_05 and con_06 and con_07 and con_08:
                return True
            return False

    # Three Black Crows (18)
    class ThreeBlackCrows(PatternTemplate):
        def __init__(self, trend: float, relative_size: list, cs: CandleStick, cs_m1: CandleStick, cs_m2: CandleStick, param: dict):
            super().__init__(param, 'ThreeBlackCrows', 'bearish', trend, [cs_m2, cs_m1, cs])
            self._relative_size = relative_size
            self._cs = cs
            self._cs_m1 = cs_m1
            self._cs_m2 = cs_m2
            self.is_pattern = self._is_three_black_crows()

        def _is_three_black_crows(self) -> None or bool:
            """
            method to check if the candle stick is a three black crows
            :return: bool: True if the candle stick is a three black crows, False otherwise
            """
            if self.trend_strength is None:
                return None
            con_01: bool = self.trend_strength >= self.param['trend_strength']
            con_02: bool = self._cs_m2.type() == 'bearish'
            con_03: bool = self._cs_m2.cs_body_ratio() >= self.param['cs_m2_body_ratio']
            con_04: bool = self._relative_size[-3] >= self.param['cs_m2_relative_size']
            con_05: bool = self._cs_m1.type() == 'bearish'
            con_06: bool = self._cs_m1.cs_body_ratio() >= self.param['cs_m1_body_ratio']
            con_07: bool = self._relative_size[-2] >= self.param['cs_m1_relative_size']
            con_08: bool = self._cs.type() == 'bearish'
            con_09: bool = self._cs.cs_body_ratio() >= self.param['cs_body_ratio']
            con_10: bool = self._relative_size[-1] >= self.param['cs_relative_size']
            if con_01 and con_02 and con_03 and con_04 and con_05 and con_06 and con_07 and con_08 and con_09 and con_10:
                return True
            return False

    # Bearish Marubozu (19)
    class BearishMarubozu(PatternTemplate):
        def __init__(self, trend: float, relative_size: list, cs: CandleStick, param: dict):
            super().__init__(param, 'BearishMarubozu', 'bearish', trend, [cs])
            self._relative_size = relative_size
            self._cs = cs
            self.is_pattern = self._is_bearish_marubozu()

        def _is_bearish_marubozu(self) -> None or bool:
            """
            method to check if the candle stick is a bearish marubozu
            :return: bool: True if the candle stick is a bearish marubozu, False otherwise
            """
            if self.trend_strength is None:
                return None
            con_01: bool = self.trend_strength >= self.param['trend_strength']
            con_02: bool = self._cs.type() == 'bearish'
            con_03: bool = self._cs.cs_body_ratio() >= self.param['cs_body_ratio']
            con_04: bool = self._relative_size[-1] >= self.param['cs_relative_size']
            if con_01 and con_02 and con_03 and con_04:
                return True
            return False

    # Three Inside Down (20)
    class ThreeInsideDown(PatternTemplate):
        def __init__(self, trend: float, relative_size: list, cs: CandleStick, cs_m1: CandleStick, cs_m2: CandleStick, param: dict):
            super().__init__(param, 'ThreeInsideDown', 'bearish', trend, [cs_m2, cs_m1, cs])
            self._relative_size = relative_size
            self._cs = cs
            self._cs_m1 = cs_m1
            self._cs_m2 = cs_m2
            self.is_pattern = self._is_three_inside_down()

        def _is_three_inside_down(self) -> None or bool:
            """
            method to check if the candle stick is a three inside down
            :return: bool: True if the candle stick is a three inside down, False otherwise
            """
            if self.trend_strength is None:
                return None
            con_01: bool = self.trend_strength >= self.param['trend_strength']
            con_02: bool = self._cs_m2.type() == 'bullish'
            con_03: bool = self._cs_m2.cs_body_ratio() >= self.param['cs_m2_body_ratio']
            con_04: bool = self._relative_size[-3] >= self.param['cs_m2_relative_size']
            con_05: bool = self._cs_m1.type() == 'bearish'
            con_06: bool = self._cs_m1.open <= self._cs_m2.close
            con_07: bool = self._cs.type() == 'bearish'
            con_08: bool = self._cs.cs_body_ratio() >= self.param['cs_body_ratio']
            con_09: bool = self._relative_size[-1] >= self.param['cs_relative_size']
            con_10: bool = self._cs.open >= self._cs_m1.close
            if con_01 and con_02 and con_03 and con_04 and con_05 and con_06 and con_07 and con_08 and con_09 and con_10:
                return True
            return False

    # BearishHarami (21)
    class BearishHarami(PatternTemplate):
        def __init__(self, trend: float, relative_size: list, cs: CandleStick, cs_m1: CandleStick, param: dict):
            super().__init__(param, 'BearishHarami', 'bearish', trend, [cs_m1, cs])
            self._relative_size = relative_size
            self._cs = cs
            self._cs_m1 = cs_m1
            self.is_pattern = self._is_bearish_harami()

        def _is_bearish_harami(self) -> None or bool:
            """
            method to check if the candle stick is a bearish harami
            :return: bool: True if the candle stick is a bearish harami, False otherwise
            """
            if self.trend_strength is None:
                return None
            con_01: bool = self.trend_strength >= self.param['trend_strength']
            con_02: bool = self._cs_m1.type() == 'bullish'
            con_03: bool = self._cs_m1.cs_body_ratio() >= self.param['cs_m1_body_ratio']
            con_04: bool = self._relative_size[-2] >= self.param['cs_m1_relative_size']
            con_05: bool = self._cs.type() == 'bearish'
            con_06: bool = self._cs.cs_body_ratio() >= self.param['cs_body_ratio']
            con_07: bool = self._relative_size[-1] <= self.param['cs_relative_size']
            con_08: bool = self._cs.close >= self._cs_m1.open
            con_09: bool = self._cs.open <= self._cs_m1.close
            if con_01 and con_02 and con_03 and con_04 and con_05 and con_06 and con_07 and con_08 and con_09:
                return True
            return False

    # Tweezer Top (22)
    class TweezerTop(PatternTemplate):
        def __init__(self, trend: float, relative_size: list, cs: CandleStick, cs_m1: CandleStick, param: dict):
            super().__init__(param, 'TweezerTop', 'bearish', trend, [cs_m1, cs])
            self._relative_size = relative_size
            self._cs = cs
            self._cs_m1 = cs_m1
            self.is_pattern = self._is_tweezer_top()

        def _is_tweezer_top(self) -> None or bool:
            """
            method to check if the candle stick is a tweezer top
            :return: bool: True if the candle stick is a tweezer top, False otherwise
            """
            if self.trend_strength is None:
                return None
            con_01: bool = self.trend_strength >= self.param['trend_strength']
            con_02: bool = self._cs_m1.type() == 'bullish'
            con_03: bool = self._cs_m1.cs_body_ratio() >= self.param['cs_m1_body_ratio']
            con_04: bool = self._relative_size[-2] >= self.param['cs_m1_relative_size']
            con_05: bool = self._cs.type() == 'bearish'
            con_06: bool = self._cs.cs_body_ratio() <= self.param['cs_body_ratio']
            con_07: bool = self._cs.body_position() >= self.param['cs_body_position']
            if con_01 and con_02 and con_03 and con_04 and con_05 and con_06 and con_07:
                return True
            return False


    # Bullish Reversal Candlestick Patterns methods:
    # Hammer (1)
    def is_hammer(self, param: dict = None, is_boolean: bool = False) -> list:
        if param is None:
            param = Parameter.candle_stick_pattern['bullish']['hammer']
        result = []
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i, param['trend_window'])
            if is_boolean:
                result.append(self.Hammer(trend, self.candle_stick_frame[i], param).is_pattern)
            else:
                result.append(self.Hammer(trend, self.candle_stick_frame[i], param))
        return result

    # Piercing (2)
    def is_piercing(self, param: dict = None, is_boolean: bool = False) -> list:
        if param is None:
            param = Parameter.candle_stick_pattern['bullish']['piercing']
        result = []
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i-1, param['trend_window'])
            if is_boolean:
                result.append(self.Piercing(trend, self.candle_stick_frame[i], self.candle_stick_frame[i-1], param).is_pattern)
            else:
                result.append(self.Piercing(trend, self.candle_stick_frame[i], self.candle_stick_frame[i-1], param))
        return result

    # Bullish Engulfing (3)
    def is_bullish_engulfing(self, param: dict = None, is_boolean: bool = False) -> list:
        if param is None:
            param = Parameter.candle_stick_pattern['bullish']['bullish_engulfing']
        result = []
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i-1, param['trend_window'])
            if is_boolean:
                result.append(self.BullishEngulfing(trend, self.candle_stick_frame[i], self.candle_stick_frame[i-1], param).is_pattern)
            else:
                result.append(self.BullishEngulfing(trend, self.candle_stick_frame[i], self.candle_stick_frame[i-1], param))
        return result

    # Morning Star (4)
    def is_morning_star(self, param: dict = None, is_boolean: bool = False) -> list:
        if param is None:
            param = Parameter.candle_stick_pattern['bullish']['morning_star']
        result = []
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i-2, param['trend_window'])
            relative_size = self.min_max_body(i, param['relative_size_window'])
            if is_boolean:
                result.append(self.MorningStar(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], self.candle_stick_frame[i-2], param).is_pattern)
            else:
                result.append(self.MorningStar(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], self.candle_stick_frame[i-2], param))
        return result

    # Tree White Soldiers (5)
    def is_three_white_soldiers(self, param: dict = None, is_boolean: bool = False) -> list:
        if param is None:
            param = Parameter.candle_stick_pattern['bullish']['three_white_soldiers']
        result = []
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i-2, param['trend_window'])
            relative_size = self.min_max_body(i, param['relative_size_window'])
            if is_boolean:
                result.append(self.ThreeWhiteSoldiers(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], self.candle_stick_frame[i-2], param).is_pattern)
            else:
                result.append(self.ThreeWhiteSoldiers(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], self.candle_stick_frame[i-2], param))
        return result

    # Bullish Marubozu (6)
    def is_bullish_marubozu(self, param: dict = None, is_boolean: bool = False) -> list:
        if param is None:
            param = Parameter.candle_stick_pattern['bullish']['bullish_marubozu']
        result = []
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i, param['trend_window'])
            relative_size = self.min_max_body(i, param['relative_size_window'])
            if is_boolean:
                result.append(self.BullishMarubozu(trend, relative_size, self.candle_stick_frame[i], param).is_pattern)
            else:
                result.append(self.BullishMarubozu(trend, relative_size, self.candle_stick_frame[i], param))
        return result

    # Tree Inside Up (7)
    def is_three_inside_up(self, param: dict = None, is_boolean: bool = False) -> list:
        if param is None:
            param = Parameter.candle_stick_pattern['bullish']['three_inside_up']
        result = []
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i-2, param['trend_window'])
            relative_size = self.min_max_body(i, param['relative_size_window'])
            if is_boolean:
                result.append(self.ThreeInsideUp(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], self.candle_stick_frame[i-2], param).is_pattern)
            else:
                result.append(self.ThreeInsideUp(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], self.candle_stick_frame[i-2], param))
        return result

    # Bullish Harami (8)
    def is_bullish_harami(self, param: dict = None, is_boolean: bool = False) -> list:
        if param is None:
            param = Parameter.candle_stick_pattern['bullish']['bullish_harami']
        result = []
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i-1, param['trend_window'])
            relative_size = self.min_max_body(i, param['relative_size_window'])
            if is_boolean:
                result.append(self.BullishHarami(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], param).is_pattern)
            else:
                result.append(self.BullishHarami(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], param))
        return result

    # Tweezer Bottom (9)
    def is_tweezer_bottom(self, param: dict = None, is_boolean: bool = False) -> list:
        if param is None:
            param = Parameter.candle_stick_pattern['bullish']['tweezer_bottom']
        result = []
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i, param['trend_window'])
            relative_size = self.min_max_body(i, param['relative_size_window'])
            if is_boolean:
                result.append(self.TweezerBottom(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], param).is_pattern)
            else:
                result.append(self.TweezerBottom(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], param))
        return result


    # Bearish Reversal Candlestick Patterns Classes:
    # Hanging Man (14)
    def is_hanging_man(self, param: dict = None, is_boolean: bool = False) -> list:
        if param is None:
            param = Parameter.candle_stick_pattern['bearish']['hanging_man']
        result = []
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i, param['trend_window'])
            if is_boolean:
                result.append(self.HangingMan(trend, self.candle_stick_frame[i], param).is_pattern)
            else:
                result.append(self.HangingMan(trend, self.candle_stick_frame[i], param))
        return result

    # Dark Cloud Cover (15)
    def is_dark_cloud(self, param: dict = None, is_boolean: bool = False) -> list:
        if param is None:
            param = Parameter.candle_stick_pattern['bearish']['dark_cloud']
        result = []
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i-1, param['trend_window'])
            if is_boolean:
                result.append(self.DarkCloud(trend, self.candle_stick_frame[i], self.candle_stick_frame[i-1], param).is_pattern)
            else:
                result.append(self.DarkCloud(trend, self.candle_stick_frame[i], self.candle_stick_frame[i-1], param))
        return result

    # Bearish Engulfing (16)
    def is_bearish_engulfing(self, param: dict = None, is_boolean: bool = False) -> list:
        if param is None:
            param = Parameter.candle_stick_pattern['bearish']['bearish_engulfing']
        result = []
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i-1, param['trend_window'])
            if is_boolean:
                result.append(self.BearishEngulfing(trend, self.candle_stick_frame[i], self.candle_stick_frame[i-1], param).is_pattern)
            else:
                result.append(self.BearishEngulfing(trend, self.candle_stick_frame[i], self.candle_stick_frame[i-1], param))
        return result

    # Evening Star (17)
    def is_evening_star(self, param: dict = None, is_boolean: bool = False) -> list:
        if param is None:
            param = Parameter.candle_stick_pattern['bearish']['evening_star']
        result = []
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i-1, param['trend_window'])
            relative_size = self.min_max_body(i, param['relative_size_window'])
            if is_boolean:
                result.append(self.EveningStar(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], self.candle_stick_frame[i-2], param).is_pattern)
            else:
                result.append(self.EveningStar(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], self.candle_stick_frame[i-2], param))
        return result

    # Three Black Crows (18)
    def is_three_black_crows(self, param: dict = None, is_boolean: bool = False) -> list:
        if param is None:
            param = Parameter.candle_stick_pattern['bearish']['three_black_crows']
        result = []
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i-1, param['trend_window'])
            relative_size = self.min_max_body(i, param['relative_size_window'])
            if is_boolean:
                result.append(self.ThreeBlackCrows(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], self.candle_stick_frame[i-2], param).is_pattern)
            else:
                result.append(self.ThreeBlackCrows(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], self.candle_stick_frame[i-2], param))
        return result

    # Bearish Marubozu (19)
    def is_bearish_marubozu(self, param: dict = None, is_boolean: bool = False) -> list:
        if param is None:
            param = Parameter.candle_stick_pattern['bearish']['bearish_marubozu']
        result = []
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i-1, param['trend_window'])
            relative_size = self.min_max_body(i, param['relative_size_window'])
            if is_boolean:
                result.append(self.BearishMarubozu(trend, relative_size, self.candle_stick_frame[i], param).is_pattern)
            else:
                result.append(self.BearishMarubozu(trend, relative_size, self.candle_stick_frame[i], param))
        return result

    # Three Inside Down (20)
    def is_three_inside_down(self, param: dict = None, is_boolean: bool = False) -> list:
        if param is None:
            param = Parameter.candle_stick_pattern['bearish']['three_inside_down']
        result = []
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i-1, param['trend_window'])
            relative_size = self.min_max_body(i, param['relative_size_window'])
            if is_boolean:
                result.append(self.ThreeInsideDown(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], self.candle_stick_frame[i-2], param).is_pattern)
            else:
                result.append(self.ThreeInsideDown(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], self.candle_stick_frame[i-2], param))
        return result

    # Bearish Harami (21)
    def is_bearish_harami(self, param: dict = None, is_boolean: bool = False) -> list:
        if param is None:
            param = Parameter.candle_stick_pattern['bearish']['bearish_harami']
        result = []
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i-1, param['trend_window'])
            relative_size = self.min_max_body(i, param['relative_size_window'])
            if is_boolean:
                result.append(self.BearishHarami(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], param).is_pattern)
            else:
                result.append(self.BearishHarami(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], param))
        return result

    # Tweezer Top (22)
    def is_tweezer_top(self, param: dict = None, is_boolean: bool = False) -> list:
        if param is None:
            param = Parameter.candle_stick_pattern['bearish']['tweezer_top']
        result = []
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i-1, param['trend_window'])
            relative_size = self.min_max_body(i, param['relative_size_window'])
            if is_boolean:
                result.append(self.TweezerTop(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], param).is_pattern)
            else:
                result.append(self.TweezerTop(trend, relative_size, self.candle_stick_frame[i], self.candle_stick_frame[i-1], param))
        return result

    def find(self, type: str = 'all', is_boolean: bool = True) -> pd.DataFrame:
        """
        Find candle stick pattern
        :param type: str: 'all', 'bullish' or 'bearish' (default: 'all')
        :param is_boolean: Boolean: True or False (default: True)
        :return: pd.DataFrame: DataFrame of candle stick pattern
        """
        if type not in ['all', 'bullish', 'bearish']:
            raise Exception('Invalid type: type must be "all", "bullish" or "bearish"')
        pattern_dict = {
            'bullish': {
                'hammer': self.is_hammer,
                'piercing': self.is_piercing,
                'bullish_engulfing': self.is_bullish_engulfing,
                'mornin_star': self.is_morning_star,
                'three_white_soldiers': self.is_three_white_soldiers,
                'bullish_maru_bozu': self.is_bullish_marubozu,
                'three_inside_up': self.is_three_inside_up,
                'bullish_harami': self.is_bullish_harami,
                'tweezer_bottom': self.is_tweezer_bottom,
            },
            'bearish': {
                'hanging_man': self.is_hanging_man,
                'dark_cloud': self.is_dark_cloud,
                'bearish_engulfing': self.is_bearish_engulfing,
                'evening_star': self.is_evening_star,
                'three_black_crows': self.is_three_black_crows,
                'bearish_marubozu': self.is_bearish_marubozu,
                'three_inside_down': self.is_three_inside_down,
                'bearish_harami': self.is_bearish_harami,
                'tweezer_top': self.is_tweezer_top,
            }
        }
        if type == 'all':
            pattern_list = list(pattern_dict['bullish'].values()) + list(pattern_dict['bearish'].values())
            columns = list(pattern_dict['bullish'].keys()) + list(pattern_dict['bearish'].keys())
        elif type == 'bullish':
            pattern_list = list(pattern_dict['bullish'].values())
            columns = list(pattern_dict['bullish'].keys())
        elif type == 'bearish':
            pattern_list = list(pattern_dict['bearish'].values())
            columns = list(pattern_dict['bearish'].keys())
        result = []
        for pattern in tqdm(pattern_list, desc='Finding Candle Stick Pattern'):
            result.append(pattern(is_boolean=is_boolean))
        result = pd.DataFrame(result).T
        result.columns = columns
        result.reset_index(drop=True, inplace=True)
        return result
