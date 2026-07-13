#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  7 11:09:07 2025

@author: noahcreany
"""

import pandas as pd
import os



# Get the API token from the environment variable
api_key = os.getenv('API_KEY')

# Check if the token was found
if not api_key:
    raise ValueError("API token not found. Please set the API_KEY secret.")


conf = {'key' : api_key,
        'lat' : 46.73239,
        'lon': -117.00017,
        'asl' : 786,
        'fmt' : 'csv',
        'unit_temp': 'F',
        'unit_wind' : 'mph',
        'unit_pcp' : 'inch',
        'city':'Moscow',
        'state':'ID'}


url = f"""https://my.meteoblue.com/packages/basic-1h?apikey={conf['key']}&
lat={conf['lat']}&
lon={conf['lon']}&
asl={conf['asl']}&
format={conf['fmt']}&
temperature={conf['unit_temp']}&
windspeed={conf['unit_wind']}&
precipitationamount={conf['unit_pcp']}&
tz=America%2FDenver&forecast_days=5"""


url = ''.join(url.splitlines())
# Getting Data
print('Fetching Data')

# Loading from File to save credits
def get_data(url): 
    df = pd.read_csv(url)
    df['time'] = pd.to_datetime(df.time)
    df['date'] = df.time.dt.date
    return df

df = get_data(url)

df = df.rename(columns={'time':'DateTime'})
df.set_index('DateTime', inplace = True)

df.to_pickle('Data/meteogram_data.pkl')
