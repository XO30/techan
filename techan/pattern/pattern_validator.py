from techan.core.candle_stick_frame import CandleStickFrame
from tqdm import tqdm
import pandas as pd


class PatternValidator:
    def __init__(self, candle_stick_frame: CandleStickFrame, pattern_df: pd.DataFrame, past_window: int = 10, future_window:int = 10):
        self.candle_stick_frame: CandleStickFrame = candle_stick_frame
        self.pattern_df: pd.DataFrame = pattern_df
        self.validation_df: pd.DataFrame = pattern_df.copy()
        self.past_window: int = past_window
        self.future_window: int = future_window

    def get_past_high_low(self, index: int) -> (float, float) or (None, None):
        window: list or None = self.candle_stick_frame[index-self.past_window+1:index+1] if index > self.past_window else None
        if window is not None:
            return max(candle_stick.high for candle_stick in window), min(candle_stick.low for candle_stick in window)
        else:
            return None, None

    def get_future_window(self, index: int) -> list or None:
        window: list or None = self.candle_stick_frame[index+1:index+self.future_window + 1] if index < len(self.candle_stick_frame)-self.future_window else None
        if window is not None:
            return window
        else:
            return None

    def _validate(self, cs_pattern: any, past_high: float, past_low: float, future_window: list) -> bool:
        is_valid: bool = False
        is_invalid: bool = False
        if cs_pattern.pattern_type == 'bullish':
            if cs_pattern.pattern[-1].low == past_low:
                pass  # the sl is at the low of the pattern
            for candle_stick in future_window:
                if candle_stick.high >= past_high:
                    is_valid = True
                if candle_stick.low <= past_low:
                    is_invalid = True
                if is_valid:
                    cs_pattern.is_valid = True
                    return True
                elif is_invalid:
                    cs_pattern.is_valid = False
                    return False
        elif cs_pattern.pattern_type == 'bearish':
            if cs_pattern.pattern[-1].high == past_high:
                pass  # the sl is at the high of the pattern
            for candle_stick in future_window:
                if candle_stick.high >= past_high:
                    is_invalid = True
                if candle_stick.low <= past_low:
                    is_valid = True
                if is_valid:
                    cs_pattern.is_valid = True
                    return True
                elif is_invalid:
                    cs_pattern.is_valid = False
                    return False
        else:
            cs_pattern.is_valid = None
            return False # tbd

    def validate(self):
        for index, row in tqdm(self.pattern_df.iterrows()):
            for pattern in self.pattern_df.columns:
                if self.pattern_df.loc[index, pattern].is_pattern:
                    past_high, past_low = self.get_past_high_low(index)
                    future_window = self.get_future_window(index)
                    if past_high is not None and past_low is not None and future_window is not None:
                        if self._validate(self.pattern_df.loc[index, pattern], past_high, past_low, future_window):
                            self.validation_df.loc[index, pattern] = True
                        else:
                            self.validation_df.loc[index, pattern] = False
                    else:
                        self.validation_df.loc[index, pattern] = None
                else:
                    self.validation_df.loc[index, pattern] = None
        return self.validation_df
    