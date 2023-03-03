from techan.core.candle_stick_frame import CandleStickFrame
import pandas as pd


class PatternValidator:
    def __init__(self, candle_stick_frame: CandleStickFrame, pattern_df: pd.DataFrame, past_window: int = 10, future_window:int = 10):
        self.candle_stick_frame: CandleStickFrame = candle_stick_frame
        self.pattern_df: pd.DataFrame = pattern_df
        self.validation_df: pd.DataFrame = pattern_df.copy()
        self.past_window: int = past_window
        self.future_window: int = future_window

    def get_past_high_low(self, index: int) -> (float, float) or (None, None):
        window: list or None = self.candle_stick_frame[index-self.past_window:index] if index > self.past_window else None
        if window is not None:
            return max(candle_stick.high for candle_stick in window), min(candle_stick.low for candle_stick in window)
        else:
            return None, None

    def get_future_high_low(self, index: int) -> (float, float) or (None, None):
        window: list or None = self.candle_stick_frame[index:index+self.future_window] if index < len(self.candle_stick_frame)-self.future_window else None
        if window is not None:
            return max(candle_stick.high for candle_stick in window), min(candle_stick.low for candle_stick in window)
        else:
            return None, None

    def _validate(self, cs_pattern: any, past_high: float, past_low: float, future_high: float, future_low: float) -> bool:
        if cs_pattern.pattern_type == 'bullish':
            if future_high >= past_high and future_low >= past_low:
                cs_pattern.is_valid = True
                return True
            else:
                cs_pattern.is_valid = False
                return False
        elif cs_pattern.pattern_type == 'bearish':
            if future_high <= past_high and future_low <= past_low:
                cs_pattern.is_valid = True
                return True
            else:
                cs_pattern.is_valid = False
                return False
        else:
            cs_pattern.is_valid = None
            return False # tbd

    def validate(self):
        for index, row in self.pattern_df.iterrows():
            for pattern in self.pattern_df.columns:
                if self.pattern_df.loc[index, pattern].is_pattern:
                    past_high, past_low = self.get_past_high_low(index)
                    future_high, future_low = self.get_future_high_low(index)
                    if past_high is not None and past_low is not None and future_high is not None and future_low is not None:
                        if self._validate(self.pattern_df.loc[index, pattern], past_high, past_low, future_high, future_low):
                            self.validation_df.loc[index, pattern] = True
                        else:
                            self.validation_df.loc[index, pattern] = False
                    else:
                        self.validation_df.loc[index, pattern] = None
                else:
                    self.validation_df.loc[index, pattern] = None
        return self.validation_df
    