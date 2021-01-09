def filter_df(df, column, value):
    return df.loc[df[column] == value]


def xth_date(df, country, x, data="cases"):
    # df should be df_from_path(resources['countries-aggregated'])
    country_df = filter_df(df, 'Country', country)

    if data == "cases":
        j = 2
    elif data == "recoveries":
        j = 3
    elif data == "deaths":
        j = 4
    else:
        raise ValueError("'data' variable must be equal to 'cases', 'recoveries' or 'deaths'")

    for i in range(len(country_df)):
        if country_df.iloc[i][j] >= x:
            return country_df.iloc[i][0]
    return False
