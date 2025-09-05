import pandas as pd


conf = {'key' : 'Rh4cdAK3t0H9SoCg',
        'lat' : 40.5853,
        'lon': -105.084,
        'asl' : 1525,
        'fmt' : 'csv',
        'unit_temp': 'F',
        'unit_wind' : 'mph',
        'unit_pcp' : 'inch',
        'city':'Fort Collins',
        'state':'CO'}


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

def get_data(url): 
    df = pd.read_csv(url)
    df['time'] = pd.to_datetime(df.time)
    df['date'] = df.time.dt.date
    return df

df = get_data(url)

df.to_pickle('/home/noah/Documents/meteogram_data.pkl')