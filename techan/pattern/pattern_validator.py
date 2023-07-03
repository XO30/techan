from techan.core.candle_stick_frame import CandleStickFrame
from tqdm import tqdm
import pandas as pd
from techan.indicator.atr import ATR


class PatternValidator:
    def __init__(self,
                 candle_stick_frame: CandleStickFrame,
                 pattern_df: pd.DataFrame,
                 mode: str = 'atr',
                 past_window: int = 10,
                 wl_ratio: float = 1.618,
                 ):
        self.candle_stick_frame: CandleStickFrame = candle_stick_frame
        self.pattern_df: pd.DataFrame = pattern_df
        self.validation_df: pd.DataFrame = pattern_df.copy()
        self.mode: str = mode  # 'atr' or 'hl'
        self.past_window: int = past_window  # how far into the past should the pattern be validated
        self.wl_ratio: float = wl_ratio  # stop loss ratio

    def _get_past_high_low(self, index: int) -> (float, float) or (None, None):
        window: list or None = self.candle_stick_frame[index-self.past_window+1:index+1] if index > self.past_window else None
        if window is not None:
            return max(candle_stick.high for candle_stick in window), min(candle_stick.low for candle_stick in window)
        else:
            return None, None

    def _set_stats(self, cs_pattern: any, is_valid: bool or None, tp: float, sl: float, wl_ratio: float, v_iv_after: int or None) -> None:
        cs_pattern.is_valid = is_valid
        cs_pattern.tp = tp
        cs_pattern.sl = sl
        cs_pattern.wl_ratio = wl_ratio
        cs_pattern.v_iv_after = v_iv_after

    def _validate_hl(self, cs_pattern: any, past_high: float, past_low: float, index: int) -> bool or None:
        is_valid: bool = False
        is_invalid: bool = False
        if cs_pattern.pattern_type == 'bullish':
            p_loss = cs_pattern.pattern[-1].close - past_low
            p_win = past_high - cs_pattern.pattern[-1].close
            if p_loss >= p_win:
                past_high = cs_pattern.pattern[-1].close + p_loss * self.wl_ratio
            else:
                past_low = cs_pattern.pattern[-1].close - p_win / self.wl_ratio
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
                past_low = cs_pattern.pattern[-1].close - p_loss * self.wl_ratio
            else:
                past_high = cs_pattern.pattern[-1].close + p_win / self.wl_ratio
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

    def _validate_atr(self, cs_pattern: any, index: int, atr: float) -> bool or None:
        if cs_pattern.pattern_type == 'bullish':
            last_low = cs_pattern.pattern[-1].close - atr
            last_high = cs_pattern.pattern[-1].close + atr * self.wl_ratio
        elif cs_pattern.pattern_type == 'bearish':
            last_low = cs_pattern.pattern[-1].close - atr * self.wl_ratio
            last_high = cs_pattern.pattern[-1].close + atr
        else:
            cs_pattern.is_valid = None
            return False  # tbd, trend continuation pattern
        return self._validate_hl(cs_pattern, last_high, last_low, index)


    def validate(self) -> pd.DataFrame:
        atr_obj = ATR(self.candle_stick_frame, self.past_window)
        for index, row in tqdm(self.pattern_df.iterrows(), total=self.pattern_df.shape[0], desc='Validating Candle Stick Pattern'):
            for pattern in self.pattern_df.columns:
                if self.pattern_df.loc[index, pattern].is_pattern:
                    if self.mode == 'hl':
                        past_high, past_low = self._get_past_high_low(index)
                        if past_high is not None and past_low is not None:
                            self.validation_df.loc[index, pattern] = self._validate_hl(self.pattern_df.loc[index, pattern], past_high, past_low, index)
                        else:
                            self.validation_df.loc[index, pattern] = None
                    elif self.mode == 'atr':
                        atr = atr_obj.compute(index)
                        if atr is not None:
                            self.validation_df.loc[index, pattern] = self._validate_atr(self.pattern_df.loc[index, pattern], index, atr)
                        else:
                            self.validation_df.loc[index, pattern] = None
                else:
                    self.validation_df.loc[index, pattern] = None
        return self.validation_df
    