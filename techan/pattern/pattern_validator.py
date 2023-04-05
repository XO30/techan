from techan.core.candle_stick_frame import CandleStickFrame
from tqdm import tqdm
import pandas as pd


class PatternValidator:
    def __init__(self, candle_stick_frame: CandleStickFrame, pattern_df: pd.DataFrame, past_window: int = 10, future_window:int = 10, min_wl_ratio: float = 1.0, mode: str = 'tp'):
        self.candle_stick_frame: CandleStickFrame = candle_stick_frame
        self.pattern_df: pd.DataFrame = pattern_df
        self.validation_df: pd.DataFrame = pattern_df.copy()
        self.past_window: int = past_window  # how far into the past should the pattern be validated
        self.future_window: int = future_window  # how far into the future should the pattern be validated
        self.min_wl_ratio: float = min_wl_ratio  # minimum wl ratio
        self.mode: str = mode  # determines if the sl or tb should be modified to meet the min_wl_ratio

    def _get_past_high_low(self, index: int) -> (float, float) or (None, None):
        window: list or None = self.candle_stick_frame[index-self.past_window+1:index+1] if index > self.past_window else None
        if window is not None:
            return max(candle_stick.high for candle_stick in window), min(candle_stick.low for candle_stick in window)
        else:
            return None, None

    def _get_future_window(self, index: int) -> list or None:
        window: list or None = self.candle_stick_frame[index+1:index+self.future_window + 1] if index < len(self.candle_stick_frame)-self.future_window else None
        if window is not None:
            return window
        else:
            return None

    def _set_stats(self, cs_pattern: any, is_valid: bool or None, tp: float, sl: float, wl_ratio: float, v_iv_after: int or None) -> None:
        cs_pattern.is_valid = is_valid
        cs_pattern.tp = tp
        cs_pattern.sl = sl
        cs_pattern.wl_ratio = wl_ratio
        cs_pattern.v_iv_after = v_iv_after

    def _validate(self, cs_pattern: any, past_high: float, past_low: float, future_window: list) -> bool or None:
        is_valid: bool = False
        is_invalid: bool = False
        if cs_pattern.pattern_type == 'bullish':
            if cs_pattern.pattern[-1].close - past_low == 0:
                self._set_stats(cs_pattern, False, past_high, past_low, 0, 0)
                return False
            wl_ratio = (past_high - cs_pattern.pattern[-1].close) / (cs_pattern.pattern[-1].close - past_low)
            if wl_ratio < self.min_wl_ratio:
                if self.mode == 'tp':
                    past_high = cs_pattern.pattern[-1].close + (cs_pattern.pattern[-1].close - past_low) * self.min_wl_ratio
                    wl_ratio = (past_high - cs_pattern.pattern[-1].close) / (cs_pattern.pattern[-1].close - past_low)
                elif self.mode == 'sl':
                    past_low = cs_pattern.pattern[-1].close - (past_high - cs_pattern.pattern[-1].close) / self.min_wl_ratio
                    wl_ratio = (past_high - cs_pattern.pattern[-1].close) / (cs_pattern.pattern[-1].close - past_low)
            if past_high - cs_pattern.pattern[-1].close == 0 or cs_pattern.pattern[-1].close - past_low == 0:
                self._set_stats(cs_pattern, False, past_high, past_low, wl_ratio, 0)
                return False
            if cs_pattern.pattern[-1].low == past_low:
                pass  # the sl is at the low of the pattern
            counter = 1
            if future_window is None:
                self._set_stats(cs_pattern, None, past_high, past_low, wl_ratio, None)
                return None
            for candle_stick in future_window:
                if candle_stick.high >= past_high:
                    is_valid = True
                if candle_stick.low <= past_low:
                    is_invalid = True
                if is_valid:
                    self._set_stats(cs_pattern, True, past_high, past_low, wl_ratio, counter)
                    return True
                elif is_invalid:
                    self._set_stats(cs_pattern, False, past_high, past_low, wl_ratio, counter)
                    return False
                counter += 1
            self._set_stats(cs_pattern, False, past_high, past_low, wl_ratio, counter)
            return False
        elif cs_pattern.pattern_type == 'bearish':
            if past_high - cs_pattern.pattern[-1].close == 0:
                self._set_stats(cs_pattern, False, past_low, past_high, 0, 0)
                return False
            wl_ratio = (cs_pattern.pattern[-1].close - past_low) / (past_high - cs_pattern.pattern[-1].close)
            if wl_ratio < self.min_wl_ratio:
                if self.mode == 'tp':
                    past_low = cs_pattern.pattern[-1].close - (past_high - cs_pattern.pattern[-1].close) * self.min_wl_ratio
                    wl_ratio = (cs_pattern.pattern[-1].close - past_low) / (past_high - cs_pattern.pattern[-1].close)
                elif self.mode == 'sl':
                    past_high = cs_pattern.pattern[-1].close + (cs_pattern.pattern[-1].close - past_low) / self.min_wl_ratio
                    wl_ratio = (cs_pattern.pattern[-1].close - past_low) / (past_high - cs_pattern.pattern[-1].close)
            if cs_pattern.pattern[-1].close - past_low == 0 or past_high - cs_pattern.pattern[-1].close == 0:
                self._set_stats(cs_pattern, False, past_low, past_high, wl_ratio, 0)
                return False
            if cs_pattern.pattern[-1].high == past_high:
                pass  # the sl is at the high of the pattern
            counter = 1
            if future_window is None:
                self._set_stats(cs_pattern, None, past_low, past_high, wl_ratio, None)
                return None
            for candle_stick in future_window:
                if candle_stick.high >= past_high:
                    is_invalid = True
                if candle_stick.low <= past_low:
                    is_valid = True
                if is_valid:
                    self._set_stats(cs_pattern, True, past_low, past_high, wl_ratio, counter)
                    return True
                elif is_invalid:
                    self._set_stats(cs_pattern, False, past_low, past_high, wl_ratio, counter)
                    return False
                counter += 1
            self._set_stats(cs_pattern, False, past_low, past_high, wl_ratio, counter)
            return False
        else:
            cs_pattern.is_valid = None
            return False # tbd, trend continuation pattern

    def _validate_new(self, cs_pattern: any, past_high: float, past_low: float, index: int) -> bool or None:
        is_valid: bool = False
        is_invalid: bool = False
        if cs_pattern.pattern_type == 'bullish':
            p_loss = cs_pattern.pattern[-1].close - past_low
            p_win = past_high - cs_pattern.pattern[-1].close
            if p_loss >= p_win:
                past_high = cs_pattern.pattern[-1].close + p_loss / 0.618
            else:
                past_low = cs_pattern.pattern[-1].close - p_win * 0.618
            wl_ratio = (past_high - cs_pattern.pattern[-1].close) / (cs_pattern.pattern[-1].close - past_low)
            while is_valid is False and is_invalid is False:
                index += 1
                if index >= len(self.candle_stick_frame):
                    self._set_stats(cs_pattern, None, past_high, past_low, wl_ratio, index)
                    return None
                if self.candle_stick_frame[index].close >= past_high:
                    is_valid = True
                elif self.candle_stick_frame[index].close <= past_low:
                    is_invalid = True
            if is_valid:
                self._set_stats(cs_pattern, True, past_high, past_low, wl_ratio, index)
                return True
            elif is_invalid:
                self._set_stats(cs_pattern, False, past_high, past_low, wl_ratio, index)
                return False
        elif cs_pattern.pattern_type == 'bearish':
            p_loss = past_high - cs_pattern.pattern[-1].close
            p_win = cs_pattern.pattern[-1].close - past_low
            if p_loss >= p_win:
                past_low = cs_pattern.pattern[-1].close - p_loss / 0.618
            else:
                past_high = cs_pattern.pattern[-1].close + p_win * 0.618
            wl_ratio = (cs_pattern.pattern[-1].close - past_low) / (past_high - cs_pattern.pattern[-1].close)
            while is_valid is False and is_invalid is False:
                index += 1
                if index >= len(self.candle_stick_frame):
                    self._set_stats(cs_pattern, None, past_high, past_low, wl_ratio, index)
                    return None
                if self.candle_stick_frame[index].close >= past_high:
                    is_invalid = True
                elif self.candle_stick_frame[index].close <= past_low:
                    is_valid = True
            if is_valid:
                self._set_stats(cs_pattern, True, past_high, past_low, wl_ratio, index)
                return True
            elif is_invalid:
                self._set_stats(cs_pattern, False, past_high, past_low, wl_ratio, index)
                return False
        else:
            cs_pattern.is_valid = None
            return False  # tbd, trend continuation pattern


    def validate(self) -> pd.DataFrame:
        for index, row in tqdm(self.pattern_df.iterrows(), total=self.pattern_df.shape[0], desc='Validating Candle Stick Pattern'):
            for pattern in self.pattern_df.columns:
                if self.pattern_df.loc[index, pattern].is_pattern:
                    past_high, past_low = self._get_past_high_low(index)
                    #future_window = self._get_future_window(index)
                    if past_high is not None and past_low is not None: # and future_window is not None
                        self.validation_df.loc[index, pattern] = self._validate_new(self.pattern_df.loc[index, pattern], past_high, past_low, index)
                    else:
                        self.validation_df.loc[index, pattern] = None
                else:
                    self.validation_df.loc[index, pattern] = None
        return self.validation_df
    