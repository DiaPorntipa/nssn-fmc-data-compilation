import pandas as pd
from pytz import timezone


def add_UTC_Datetime(df):
    aus_tz = timezone('Australia/Sydney')
    df['Datetime'] = df['Datetime'].dt.tz_localize(aus_tz, ambiguous='NaT', nonexistent='NaT')
    df = df[~df['Datetime'].isna()]
    df['UTC_Datetime'] = df['Datetime'].dt.tz_convert('UTC')

    df['Datetime'] = df['Datetime'].apply(lambda t: pd.to_datetime(t).tz_localize(None))
    df['UTC_Datetime'] = df['UTC_Datetime'].apply(lambda t: pd.to_datetime(t).tz_localize(None))

    return df


def add_Canberra_Datetime(df):
    aus_tz = timezone('Australia/Sydney')
    df = df[~df['UTC_Datetime'].isna()]
    if df['UTC_Datetime'].dt.tz is None:
        df['UTC_Datetime'] = df['UTC_Datetime'].dt.tz_localize('UTC')
    df['Datetime'] = df['UTC_Datetime'].dt.tz_convert(aus_tz)

    df['Datetime'] = df['Datetime'].apply(lambda t: pd.to_datetime(t).tz_localize(None))
    df['UTC_Datetime'] = df['UTC_Datetime'].apply(lambda t: pd.to_datetime(t).tz_localize(None))

    return df
