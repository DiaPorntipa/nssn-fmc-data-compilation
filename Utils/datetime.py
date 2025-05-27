from pytz import timezone


def add_UTC_Datetime(df):
    aus_tz = timezone('Australia/Sydney')
    df['Datetime'] = df['Datetime'].dt.tz_localize(aus_tz, ambiguous='NaT', nonexistent='NaT')
    df = df[~df['Datetime'].isna()]
    df['UTC_Datetime'] = df['Datetime'].dt.tz_convert('UTC')

    return df
