import pandas as pd
from pytz import timezone


def add_UTC_Datetime(df):
    # Ensure datetime type
    if not pd.api.types.is_datetime64_any_dtype(df['Datetime']):
        df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce')

    # Check for at least one valid datetime
    valid_sample = df['Datetime'].dropna()
    if valid_sample.empty:
        raise ValueError("Datetime column has no valid datetimes")

    sample = valid_sample.iloc[0]
    if sample.tzinfo is None:
        aus_tz = timezone('Australia/Sydney')
        df['Datetime'] = df['Datetime'].dt.tz_localize(aus_tz, ambiguous='NaT', nonexistent='NaT')

    # Add UTC_Datetime
    df['UTC_Datetime'] = df['Datetime'].dt.tz_convert('UTC')

    df['UTC_Datetime'] = df['UTC_Datetime'].dt.tz_localize(None)
    df['Datetime'] = df['Datetime'].dt.tz_localize(None)

    return df


def add_Canberra_Datetime(df):
    # Ensure datetime type
    if not pd.api.types.is_datetime64_any_dtype(df['UTC_Datetime']):
        df['UTC_Datetime'] = pd.to_datetime(df['UTC_Datetime'], errors='coerce')

    # Check for at least one valid datetime
    valid_sample = df['UTC_Datetime'].dropna()
    if valid_sample.empty:
        raise ValueError("UTC_Datetime column has no valid datetimes")

    sample = valid_sample.iloc[0]
    if sample.tzinfo is None:
        df['UTC_Datetime'] = df['UTC_Datetime'].dt.tz_localize('UTC')

    # Add Canberra Datetime
    aus_tz = timezone('Australia/Sydney')
    df['Datetime'] = df['UTC_Datetime'].dt.tz_convert(aus_tz)

    df['Datetime'] = df['Datetime'].dt.tz_localize(None)
    df['UTC_Datetime'] = df['UTC_Datetime'].dt.tz_localize(None)

    return df
