# import
import numpy as np
import itertools
import tqdm
from techan.pattern.candle_stick_pattern import CandleStickPattern


class CandleStickPatternFinder(CandleStickPattern):
    def __init__(self, candle_stick_frame):
        super().__init__(candle_stick_frame)
        self.patterns = list()

    def _get_n_cs_pattern(self, n_cs, trend_window, permutation, ts_confirm):
        cs_body_ratio = list()
        cs_relative_size = list()
        cs_body_position = list()
        body_ls_ratio = list()
        body_us_ratio = list()

        for n in permutation:
            cs_body_ratio.append(n[0])
            cs_relative_size.append(n[1])
            cs_body_position.append(n[2])
            body_ls_ratio.append(n[3])
            body_us_ratio.append(n[4])

        bearish_results = list()
        bullish_results = list()
        for i in range(len(self.candle_stick_frame)):
            trend = self.trend(i-n_cs, trend_window)
            last_n_cs = self.candle_stick_frame[i-n_cs:i]
            boolean_results = list()
            for n in range(len(last_n_cs)):
                try:
                    if last_n_cs[n].body_position() >= cs_body_position[n] and \
                            last_n_cs[n].cs_body_ratio() >= cs_body_ratio[n] and \
                            last_n_cs[n].cs_size() >= cs_relative_size[n] * self._average_candle_stick_size and \
                            last_n_cs[n].body_lower_shadow_ratio() >= body_ls_ratio[n] and \
                            last_n_cs[n].body_upper_shadow_ratio() >= body_us_ratio[n]:
                        boolean_results.append(True)
                    else:
                        boolean_results.append(False)
                except:
                    boolean_results.append(False)

            if trend == 'up' and all(boolean_results):
                bearish_results.append(True)
                bullish_results.append(False)
            elif trend == 'down' and all(boolean_results):
                bullish_results.append(True)
                bearish_results.append(False)
            else:
                bearish_results.append(False)
                bullish_results.append(False)
        confirmations = self._evaluate_cs_pattern((bearish_results, bullish_results), ts_confirm)
        return confirmations

    def _evaluate_cs_pattern(self, results, ts_confirm):
        bearish_confirmation_counter = 0
        bullish_confirmation_counter = 0
        for i in range(len(self.candle_stick_frame)):
            if results[0][i] is True:
                if self.trend(i-ts_confirm, ts_confirm) == 'down':
                    bearish_confirmation_counter += 1
            elif results[1][i] is True:
                if self.trend(i-ts_confirm, ts_confirm) == 'up':
                    bullish_confirmation_counter += 1
        return bearish_confirmation_counter, bullish_confirmation_counter


    def find_n_cs_pattern(self,
                          n_cs=1,
                          trend_window=10,
                          cs_body_ratio=[(0, 1, 0.2)],
                          cs_relative_size=[(0, 1, 0.2)],
                          cs_body_position=[(-1, 1, 0.2)],
                          body_ls_ratio=[(0, 1, 0.2)],
                          body_us_ratio=[(0, 1, 0.2)],
                          ts_confirm=10,
                          ):
        permutations = list()
        for n in range(n_cs):
            # permutation of all parametes with the given bordes and step size
            permutations.append(list(itertools.product(*[np.arange(*cs_body_ratio[n]),
                                                         np.arange(*cs_relative_size[n]),
                                                         np.arange(*cs_body_position[n]),
                                                         np.arange(*body_ls_ratio[n]),
                                                         np.arange(*body_us_ratio[n])])))

        # combine all permutations
        permutations = list(itertools.product(*permutations))
        print(len(permutations))

        for permutation in tqdm.tqdm(permutations):
            confirmations = self._get_n_cs_pattern(n_cs, trend_window, permutation, ts_confirm)
            self.patterns.append(('bearish', permutation, confirmations[0]))
            self.patterns.append(('bullish', permutation, confirmations[1]))
        return self.patterns
