import requests
import pandas as pd
import io
import datetime

class Country:
    def __init__(self, data):
        self.country = data['country']
        self.population = data['country_population']
        self.coords = (data['coordinates']['latitude'],data['coordinates']['longitude'])
        self.confirmed = data['latest']['confirmed']
        self.deaths = data['latest']['deaths']

    def __str__(self):
        return self.country


# def filter_df(df, column, value):
#     return df.loc[df[column] == value]

DATA_SOURCE = 'https://datahub.io/core/covid-19/datapackage.json'


def get_resources(url=DATA_SOURCE):
    r = requests.get(url)
    resources = {}

    for i in range(len(r.json()['resources'])):
        if r.json()['resources'][i]['name'] == 'time-series-19-covid-combined_json':
            current_api = r.json()['resources'][i]['path']
        res_name = r.json()['resources'][i]['name']
        res_path = r.json()['resources'][i]['path']
        resources[res_name] = res_path

    return resources, current_api


def get_df(api):
    # api should be the current_api returned from get_resources
    r = requests.get(api)
    s2_data = r.json()
    df = pd.json_normalize(r.json())
    return df


def df_from_path(path):
    if "csv" in path:
        new_r = requests.get(path).content
        df = pd.read_csv(io.StringIO(new_r.decode('utf-8')))
    elif "json" in path:
        new_r = requests.get(path)
        df = pd.json_normalize(new_r.json())
    return df

# def xth_infection_date(country, x, df=df_from_path(resources['countries-aggregated'])):
#     country_df = filter_df(df, 'Country', country)
#     for i in range(len(country_df)):
#         if country_df.iloc[i][2] >= x:
#             return country_df.iloc[i][0]
#     return False


# def xth_date(country, x, data="cases", df=df_from_path(resources['countries-aggregated'])):
#     country_df = filter_df(df, 'Country', country)

#     if data == "cases":
#         j = 2
#     elif data == "recoveries":
#         j = 3
#     elif data == "deaths":
#         j = 4
#     else:
#         raise ValueError("'data' variable must be equal to 'cases', 'recoveries' or 'deaths'")

#     for i in range(len(country_df)):
#         if country_df.iloc[i][j] >= x:
#             return country_df.iloc[i][0]
#     return False
