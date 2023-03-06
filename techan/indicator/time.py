from techan import CandleStickFrame
import numpy as np
import math


class Time:
    def __init__(self, candle_stick_frame: CandleStickFrame):
        self.candle_stick_frame: CandleStickFrame = candle_stick_frame

