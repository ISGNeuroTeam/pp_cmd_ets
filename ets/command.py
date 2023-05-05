import pandas as pd

from otlang.sdk.syntax import Keyword, Positional, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax
from .tsforecaster import TimeSeriesExponentialSmoothingForecaster


class EtsCommand(BaseCommand):
    # define syntax of your command here
    syntax = Syntax(
        [
            Keyword("target_col", required=True, otl_type=OTLType.STRING),
            Keyword("time_col", required=False, otl_type=OTLType.STRING),
            Keyword("trend", required=False, otl_type=OTLType.STRING),
            Keyword("periods", required=True, otl_type=OTLType.INTEGER),
            Keyword("time_epoch", required=False, otl_type=OTLType.BOOLEAN)
        ],
    )
    use_timewindow = False  # Does not require time window arguments
    idempotent = True  # Does not invalidate cache

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.log_progress('Start ets command')

        target_col = self.get_arg('target_col').value
        periods = self.get_arg("periods").value

        time_field = self.get_arg('time_col').value or '_time'
        if time_field not in df.columns:
            raise ValueError(f'Time column "{time_field}" not exist')

        trend = self.get_arg('trend').value or None
        time_epoch = self.get_arg('time_epoch').value or False
        unit = 's'
        if not time_epoch:
            unit = None

        df['dt'] = pd.to_datetime(df[time_field], unit=unit)
        df = df.set_index('dt')
        if not df.index.is_monotonic_increasing:
            df.sort_values(by='dt', inplace=True)

        freq = pd.infer_freq(df.index)

        model = TimeSeriesExponentialSmoothingForecaster().fit(target_df=df, target_col=target_col,
                                                               trend=trend, freq=freq)
        predicted_df = model.predict(period=periods, freq=freq, target_col_as=f'ets_prediction')

        return predicted_df
