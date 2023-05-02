import pandas as pd

from otlang.sdk.syntax import Keyword, Positional, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax
from .tsforecaster import TimeSeriesExponentialSmoothingForecaster


class EtsCommand(BaseCommand):
    # define syntax of your command here
    syntax = Syntax(
        [
            Positional("target_col", required=True, otl_type=OTLType.STRING),
            Keyword("future", required=True, otl_type=OTLType.INTEGER),
            Keyword("period", required=True, otl_type=OTLType.TEXT),
            Keyword("to_file", required=False, otl_type=OTLType.TEXT)
        ],
    )
    use_timewindow = False  # Does not require time window arguments
    idempotent = True  # Does not invalidate cache

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.log_progress('Start ets command')

        target_col = self.get_arg('target_col').value
        future = self.get_arg("future").value
        freq = self.get_arg("period").value

        time_field = self.get_arg('time_field').value or '_time'
        if time_field not in df.columns:
            raise ValueError(f'Time column "{time_field}" not exist')

        df['dt'] = pd.to_datetime(df[time_field])
        df = df.set_index('dt')

        copy_df = df.copy()

        model = TimeSeriesExponentialSmoothingForecaster().fit(copy_df[[target_col]], target_col)
        predicted_df = model.predict(period=future, freq=freq, target_col_as=f'ets_prediction')

        if (out_file := self.get_arg('to_file').value) is not None:
            predicted_df.to_parquet(path=out_file)

        return predicted_df
