from techan.core.candle_stick_frame import CandleStickFrame


class ATR:
    def __init__(self, csf: CandleStickFrame, time_steps: int = 15):
        self.csf: CandleStickFrame = csf
        self.time_steps: int = time_steps

    def compute(self, index: int) -> float:
        """
        method to compute the ATR for the given index
        :param index: int: index of interest
        :return: float: ATR value
        """
        if index < self.time_steps:
            return None
        index_counter: int = index
        true_ranges: list = list()
        for cs in self.csf[index - self.time_steps + 1:index + 1]:
            variant_1: float = cs.cs_size()
            variant_2: float = abs(cs.high - self.csf[index_counter - 1].close)
            variant_3: float = abs(cs.low - self.csf[index_counter - 1].close)
            true_ranges.append(max(variant_1, variant_2, variant_3))
            index_counter += 1
        if self.time_steps != len(true_ranges):
            raise Exception("ATR: time_steps != len(true_ranges)")
        return sum(true_ranges) / self.time_steps
