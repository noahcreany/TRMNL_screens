#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 18:27:31 2025

@author: noahcreany
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from astral import Observer, sun
import pytz
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
    



def daylength(latitude,longitude,elevation,timezone_str,city_name):
    observer = Observer(latitude, longitude, elevation)
    timezone = pytz.timezone(timezone_str)
    now = datetime.now(timezone)
    
    df = pd.DataFrame()
    df['Date'] = pd.date_range(start = now - relativedelta(months=6,),
                               end =  now + relativedelta(months=6),
                  freq = 'D')
    
    df['Today'] = np.where(df['Date'].dt.strftime('%Y-%m-%d')==now.strftime('%Y-%m-%d'),True,False)
    
    
    df['Daylength'] = pd.Series()
    for idx,row in df.iterrows():
            daylight = sun.daylight(observer, date = row['Date'])
            daylight = daylight[1] - daylight[0]
            df.loc[idx,'Daylength'] = daylight
    
    df['Date'] = pd.to_datetime(df['Date'])
    df['Daylength'] = pd.to_timedelta(df['Daylength']).dt.total_seconds() / 3600
        
    #Plot     
    fig,ax = plt.subplots(figsize=(8,4.8), dpi = 100)
    plt.style.use('default')
    
    ax.plot(df['Date'], df['Daylength'], linewidth = 3, alpha = .5,color='black')
    
    ax.scatter(df[df.Today==True]['Date'],
               df[df.Today==True]['Daylength'],
               color = 'black',
               s = 125,
               zorder=9)
    
    # 4. Format the X-axis (Date)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.DayLocator(bymonthday=[7,14,21,28]))
    # ax.xaxis.set_minor_locator(mdates.AutoDateLocator(interval_multiples=3))
    
    formatter = mdates.ConciseDateFormatter(ax.xaxis.get_major_locator())
    ax.xaxis.set_major_formatter(formatter)
    
    
    
    # 5. Format the Y-axis (Daylength)
    # Formatter function: float hours (14.5) -> string "14:30"
    def hours_to_hhm(hours, pos):
        h = int(hours)
        m = int((hours - h) * 60)
        return f'{h:02d}hr'
    
    hhm_formatter = ticker.FuncFormatter(hours_to_hhm)
    ax.yaxis.set_major_formatter(hhm_formatter)
    
    # Major ticks every 1 hour, minor ticks every 0.5 hours (30 min)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1.0))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.5))
    
    ax.grid(True, which='major', linestyle='-', linewidth=1.5, axis='y', alpha =1)
    ax.grid(True, which='minor', linestyle='-', linewidth=.75, axis='y', alpha = 1)
    
    # 6. Finalize plot
    ax.set_title(f'{city_name} Day Length: {df.Date.min().strftime("%m/%-d/%y")}-{df.Date.max().strftime("%m/%-d/%y")}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Length of Day')
    ax.spines['top'].set_visible(False) 
    ax.spines['right'].set_visible(False)
    fig.autofmt_xdate()
    plt.tight_layout()
    plt.savefig('Images/daylength.png')
    plt.show()
    


latitude = 40.5853
longitude = -105.084
elevation = 1525
timezone = 'America/Denver'
city_name = 'Fort Collins, CO'

daylength(latitude,longitude,elevation, timezone, city_name)