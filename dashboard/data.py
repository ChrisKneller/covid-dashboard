import requests
import pandas as pd
# from pandas.io.json import json_normalize

BASE_API_URL = 'https://coronavirus-tracker-api.herokuapp.com/v2/'

locations = BASE_API_URL + 'locations'

r = requests.get(locations)

mydata = r.json()

class Country:
    def __init__(self, data):
        self.country = data['country']
        self.population = data['country_population']
        self.coords = (data['coordinates']['latitude'],data['coordinates']['longitude'])
        self.confirmed = data['latest']['confirmed']
        self.deaths = data['latest']['deaths']

    def __str__(self):
        return self.country

df = pd.json_normalize(mydata['locations'])

# country_data = []

# for i in mydata['locations']:
#     country_object = Country(i)
#     country_data.append(country_object)

# print(country_data)

# print(len(data['locations']))
# print(data['locations'][1])

