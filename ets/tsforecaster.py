from typing import Optional

import pandas as pd
from pandas import DatetimeIndex, Timestamp
from statsmodels.tsa.exponential_smoothing.ets import ETSModel


class TimeSeriesExponentialSmoothingForecaster:

    def __init__(self):
        self.model = None
        self.history_end = None

    def fit(self,
            target_df: pd.DataFrame,
            target_col: str,
            trend: str,
            freq: str):
        self.history_end = target_df.index.max()
        self.model = ETSModel(target_df[target_col], trend=trend, freq=freq).fit()

        return self

    def predict(self,
                period: int,
                freq: str,
                target_col_as: Optional[str] = "ets_prediction"):
        predicted = self.model.forecast(period)
        result = predicted.to_frame(name=target_col_as)
        result.index = result.index.view('int64') // 1000000000

        return result
