import pandas as pd


def get_daily_extreme_observation(df, variable, date_column_name, option):
    # Remove rows of the first and last dates of each site because those days lack some hours
    first_last_dates = df.groupby('SiteID')[date_column_name].agg(['min', 'max']).reset_index()
    df = df.merge(first_last_dates, on='SiteID', how='left')
    df_date_filtered = df[(df[date_column_name] != df['min']) & (df[date_column_name] != df['max'])]
    df_date_filtered = df_date_filtered.drop(columns=['min', 'max'])

    # Select only rows with min soil_mois of the day
    extreme_value_column_name = 'Day_' + option + '_' + variable.lower()
    df_date_filtered[variable] = pd.to_numeric(df_date_filtered[variable], errors='coerce')
    df_date_filtered[extreme_value_column_name] = df_date_filtered.groupby(
        ['SiteID', date_column_name]
    )[variable].transform(option)

    return df_date_filtered[
        df_date_filtered[variable] == df_date_filtered[extreme_value_column_name]
    ]
