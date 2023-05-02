from typing import Optional

import pandas as pd
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

DAYS = {
    'd': 1,
    'w': 7,
    'm': 30,
    'y': 365
}

UNITS = ['h', 's']


def check_period(f: str, p: int) -> (str, int):
    # here we calc if freq is 'Y' or 'M' or 'm' or '31D'
    if f[-1].lower() in DAYS.keys():
        number = p * DAYS[f[-1].lower()] * (1 if len(f[:-1]) == 0 else int(f[:-1]))
        return 'D', number
    if f[-1].lower() in UNITS:
        number = p * (1 if len(f[:-1]) == 0 else int(f[:-1]))
        return f[-1].lower(), number
    return f, p


class TimeSeriesExponentialSmoothingForecaster:
    def fit(self,
            target_df: pd.DataFrame,
            target_col: str):
        self.history_end = target_df.index.max()
        self.model = SimpleExpSmoothing(target_df[target_col], initialization_method="estimated").fit()
        return self

    def predict(self,
                period: int,
                freq: str,
                target_col_as: Optional[str] = "ets_prediction"):
        default_freq = freq
        default_period = period
        freq, period = check_period(freq, period)
        print(f'{default_freq=} {default_period=} | {freq=} {period=}')
        predicted = self.model.forecast(default_period)
        forecast_start = self.history_end + pd.Timedelta(1, unit=freq)
        forecast_end = self.history_end + pd.Timedelta(period, unit=freq)
        forecast_dates = pd.date_range(start=forecast_start, end=forecast_end, freq=default_freq)
        result = pd.DataFrame(predicted, columns=[target_col_as])
        result['_time'] = forecast_dates.view('int64') // 1000000000
        return result
