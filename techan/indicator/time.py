from techan import CandleStickFrame
import math
import numpy as np
import pandas as pd


class Time:
    def __init__(self, candle_stick_frame: CandleStickFrame, date_time_format: str = 'YYYY%MM%DD'):
        self.df_date_time = pd.DataFrame([candle_stick.date_time for candle_stick in candle_stick_frame])
        self.date_time_format = self._strip_datetime_format(date_time_format)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.df_date_time}, {self.date_time_format})'

    def __str__(self):
        return f'{self.__class__.__name__}({self.df_date_time}, {self.date_time_format})'

    def _strip_datetime_format(self, date_time_format: str) -> dict:
        date_time_format_dict: dict = {'Year': [], 'Month': [], 'Day': [], 'Hour': [], 'Minute': []}
        for idx, symbol in enumerate(date_time_format):
            if symbol == '%':
                continue
            if symbol == 'Y':
                date_time_format_dict['Year'].append(idx)
                continue
            if symbol == 'M':
                date_time_format_dict['Month'].append(idx)
                continue
            if symbol == 'D':
                date_time_format_dict['Day'].append(idx)
                continue
            if symbol == 'h':
                date_time_format_dict['Hour'].append(idx)
                continue
            if symbol == 'm':
                date_time_format_dict['Minute'].append(idx)
                continue
            raise ValueError('{} ist not a valid symbol for date_time_format'.format(symbol))
        return date_time_format_dict

    def _seperate_datetime(self):
        self.df_date_time['Year'] = None
        self.df_date_time['Month'] = None
        self.df_date_time['Day'] = None
        self.df_date_time['Hour'] = None
        self.df_date_time['Minute'] = None
        for key, value in self.date_time_format.items():
            window = value
            if len(window) == 0:
                continue
            for index, row in self.df_date_time.iterrows():
                self.df_date_time.loc[index, key] = int(row[0][window[0]:window[-1]+1])
        return None

    def _normalize(self, x: pd.Series) -> list:
        return list(2 * math.pi * x / x.max())

    def _sine(self, x_normal: pd.Series) -> np.array:
        return np.sin(self._normalize(x_normal))

    def _cosine(self, x_normal: pd.Series) -> np.array:
        return np.cos(self._normalize(x_normal))

    def _transform(self, x: pd.Series, name) -> np.array:
        sine = self._sine(x)
        cosine = self._cosine(x)
        self.df_date_time[f'Sine_{name}'] = sine
        self.df_date_time[f'Cosine_{name}'] = cosine
        return np.array([sine, cosine]).T

    def transform_hour(self) -> np.array:
        return self._transform(self.df_date_time['Hour'], 'Hour')

    def transform_minute(self) -> np.array:
        return self._transform(self.df_date_time['Minute'], 'Minute')

    def transform_day(self) -> np.array:
        return self._transform(self.df_date_time['Day'], 'Day')

    def transform_month(self) -> np.array:
        return self._transform(self.df_date_time['Month'], 'Month')

    def transform_year(self) -> np.array:
        return self._transform(self.df_date_time['Year'], 'Year')

    def transform_all(self) -> np.array:
        return np.concatenate([self.transform_hour(), self.transform_minute(), self.transform_day(), self.transform_month(), self.transform_year()], axis=1)