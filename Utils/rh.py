def handle_exceeding_rh(df):
    # Find MaxRH for each site and date
    df['Date'] = df.apply(lambda row: row['Datetime'].date(), axis=1)
    df['MaxRH'] = df.groupby(['SiteID', 'Date'])['RH'].transform('max')

    # Find MaxRH95 for each site
    df['MaxRH95'] = df.groupby(['SiteID'])['MaxRH'].transform(lambda x: x.quantile(0.95))

    # Apply correction the RH values. If RH is greater than MaxRH95, RH = 100, else RH = RH*100/MaxRH95
    df['RH'] = df.apply(
        lambda row: (
            100
            if (row['RH'] > row['MaxRH95']) | (row['RH'] < 0)
            else row['RH'] * 100 / row['MaxRH95']
        ),
        axis=1,
    )

    df.drop(columns=['MaxRH', 'MaxRH95', 'Date'], inplace=True)
    return df
