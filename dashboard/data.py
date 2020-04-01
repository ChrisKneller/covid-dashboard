import requests
import pandas as pd


class Country:
    def __init__(self, data):
        self.country = data['country']
        self.population = data['country_population']
        self.coords = (data['coordinates']['latitude'],data['coordinates']['longitude'])
        self.confirmed = data['latest']['confirmed']
        self.deaths = data['latest']['deaths']

    def __str__(self):
        return self.country


def filter_df(df,column,value):
    return df.loc[df[column] == value]

# DATA FROM SOURCE 1
BASE_API_URL = 'https://coronavirus-tracker-api.herokuapp.com/v2/'
locations = BASE_API_URL + 'locations'
r = requests.get(locations)
s1_data = r.json()
df1 = pd.json_normalize(s1_data['locations'])

# DATA FROM SOURCE 2
INFO_URL = 'https://datahub.io/core/covid-19/datapackage.json'
# AGGREGRATED_COUNTRIES_JSON = 'https://pkgstore.datahub.io/core/covid-19/countries-aggregated_json/data/54fd5d25097dbb94f12e6724473b3fc7/countries-aggregated_json.json'
# COMBINED_JSON = 'https://pkgstore.datahub.io/core/covid-19/time-series-19-covid-combined_json/data/698009a8089880f873ec98c967e12fb3/time-series-19-covid-combined_json.json'
r = requests.get(INFO_URL)

for i in range(len(r.json()['resources'])):
    if r.json()['resources'][i]['name'] == 'time-series-19-covid-combined_json':
        CURRENT_API = r.json()['resources'][i]['path']

r = requests.get(CURRENT_API)
s2_data = r.json()
df2 = pd.json_normalize(r.json())