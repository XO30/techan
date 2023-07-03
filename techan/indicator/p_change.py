from techan.core.candle_stick_frame import CandleStickFrame
from techan.core.candle_stick import CandleStick

def p_change(csf: CandleStickFrame) -> list:
    """
    function to calculate the percentual change of the close price of one CandleStick to the next
    :param csf: CandleStickFrame: CandleStickFrame of interest
    :return: list: list of percentual changes
    """
    cs_m1: CandleStick or None = None
    res: list = list()
    for cs in csf:
        if cs_m1 is not None:
            change = cs.close - cs_m1.close
            percentual_change = change / cs_m1.close
            res.append(percentual_change)
        else:
            res.append(None)
        cs_m1 = cs
    return res

