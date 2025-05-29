from pytz import timezone


def add_UTC_Datetime(df):
    aus_tz = timezone('Australia/Sydney')
    df['Datetime'] = df['Datetime'].dt.tz_localize(aus_tz, ambiguous='NaT', nonexistent='NaT')
    df = df[~df['Datetime'].isna()]
    df['UTC_Datetime'] = df['Datetime'].dt.tz_convert('UTC')

    return df


def add_Australia_Datetime(df):
    aus_tz = timezone('Australia/Sydney')
    df = df[~df['UTC_Datetime'].isna()]
    if df['UTC_Datetime'].dt.tz is None:
        df['UTC_Datetime'] = df['UTC_Datetime'].dt.tz_localize('UTC')
    df['Datetime'] = df['UTC_Datetime'].dt.tz_convert(aus_tz)

    return df
