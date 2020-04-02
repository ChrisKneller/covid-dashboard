import requests
import pandas as pd
import io


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

try:
    # DATA FROM SOURCE 1
    BASE_API_URL = 'https://coronavirus-tracker-api.herokuapp.com/v2/'
    locations = BASE_API_URL + 'locations'
    r = requests.get(locations)
    s1_data = r.json()
    df1 = pd.json_normalize(s1_data['locations'])
except:
    df1 = 0

# DATA FROM SOURCE 2
INFO_URL = 'https://datahub.io/core/covid-19/datapackage.json'
r = requests.get(INFO_URL)

resources = {}

for i in range(len(r.json()['resources'])):
    if r.json()['resources'][i]['name'] == 'time-series-19-covid-combined_json':
        CURRENT_API = r.json()['resources'][i]['path']
    res_name = r.json()['resources'][i]['name']
    res_path = r.json()['resources'][i]['path']
    resources[res_name] = res_path

def df_from_path(path):
    if "csv" in path:
        new_r = requests.get(path).content
        df = pd.read_csv(io.StringIO(new_r.decode('utf-8')))
    elif "json" in path:
        new_r = requests.get(path)
        df = pd.json_normalize(new_r.json())
    return df

r = requests.get(CURRENT_API)
s2_data = r.json()
df2 = pd.json_normalize(r.json())