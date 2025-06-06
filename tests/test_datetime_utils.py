import sys

import pandas as pd

sys.path.append('..')
from Utils.datetime import add_Canberra_Datetime, add_UTC_Datetime


def test_add_UTC_Datetime_naive_input():
    dt = pd.to_datetime(['2024-01-01 00:00', '2024-01-01 12:00'])
    df = pd.DataFrame({'Datetime': dt})

    result = add_UTC_Datetime(df.copy())

    assert 'UTC_Datetime' in result.columns
    assert result['UTC_Datetime'].iloc[0].hour == 13  # +11 hours for Canberra in Jan
    assert pd.api.types.is_datetime64_dtype(result['UTC_Datetime'])


def test_add_Canberra_Datetime_naive_utc_input():
    dt = pd.to_datetime(['2024-01-01 00:00', '2024-01-01 12:00'])
    df = pd.DataFrame({'UTC_Datetime': dt})

    result = add_Canberra_Datetime(df.copy())

    assert 'Datetime' in result.columns
    assert result['Datetime'].iloc[0].hour == 11  # +11 offset
    assert result['UTC_Datetime'].iloc[0].hour == 0


def test_add_Canberra_Datetime_with_utc_aware_input():
    dt = pd.to_datetime(['2024-06-01 00:00', '2024-06-01 12:00']).tz_localize('UTC')
    df = pd.DataFrame({'UTC_Datetime': dt})

    result = add_Canberra_Datetime(df.copy())

    assert result['Datetime'].iloc[0].hour == 10  # +10 offset
    assert result['UTC_Datetime'].iloc[0].hour == 0
