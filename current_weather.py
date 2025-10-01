#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 14:03:10 2025

@author: noahcreany
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as patheffects
import numpy as np
import matplotlib as mpl
from matplotlib.colors import Normalize
from datetime import datetime, timedelta
from matplotlib.table import Table
import  matplotlib.ticker as ticker
import io
from PIL import Image, ImageEnhance


df = pd.read_pickle('Data/meteogram_data.pkl')


def get_degree_x_position(text_length):
    """Calculates x position for the degree symbol based on text length."""
    if text_length == 1:
        return 0.245
    elif text_length == 2:
        return 0.345
    else:
        return 0.475

def create_weather_display(df):
    """
    Creates a weather display with temperature, humidity, wind, and other info.

    Args:
        df (DataFrame): DataFrame containing weather information.
    """
    current_time = datetime.now().replace(minute=0, second=0, microsecond=0)

    weather_data = df[df.time == current_time].squeeze(axis=0)

    fig = plt.figure(figsize=(6.4, 4))  # Adjusted figure width

    # Main subplot (non-polar)
    ax1 = fig.add_axes([0, 0, .8, 1])  # Adjusted width for temperature bar
    ax1.axis('off')

    cmap = mpl.colormaps['Spectral_r']
    norm = Normalize(vmin=-10, vmax=110)
    get_color = lambda temp: mpl.colors.to_hex(cmap((temp - norm.vmin) / (norm.vmax - norm.vmin)))

    # Display time
    time_stamp = datetime.now()
    time_stamp = time_stamp.strftime('%a %-d %b %-I:%M %p')
    ax1.text(0.035, 0.9, time_stamp, fontsize=18, fontweight='bold')

    # Temperature
    temp = f"{int(weather_data['temperature'])}"
    temp_color = get_color(weather_data['temperature'])
    ax1.text(0.05, 0.8, 'Temp:', fontsize=18, va='top')
    ax1.text(0.075, 0.7, temp, fontsize=80, color=temp_color, va='top',
             path_effects=[patheffects.withStroke(linewidth=3, foreground='black')])
    ax1.text(get_degree_x_position(len(temp)), 0.7, '°', fontsize=35, color=temp_color, va='top',
             path_effects=[patheffects.withStroke(linewidth=2, foreground='black')])

    # Display feels like temperature
    feels_like = f"{int(weather_data['felttemperature'])}"
    feel_color = get_color(weather_data['felttemperature'])
    ax1.text(0.05, 0.4, 'Feels Like:', fontsize=16, va='top')
    ax1.text(0.075, 0.3, feels_like, fontsize=70, color=feel_color, va='top',
             path_effects=[patheffects.withStroke(linewidth=3, foreground='black')])
    ax1.text(get_degree_x_position(len(feels_like))-.04, 0.3, '°', fontsize=35, color=feel_color, va='top',
             path_effects=[patheffects.withStroke(linewidth=2, foreground='black')])

    # Daily High/Low
    daily_weather = df[df.date == weather_data['date']]
    daily_high = daily_weather['temperature'].max()
    daily_low = daily_weather['temperature'].min()
    
    prev_hour = datetime.now().replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
    prev_hour = df[df.time == prev_hour].copy()

    # Temperature Bar
    ax3 = fig.add_axes([0.485, 0.1, 0.025, 0.75])  # Position and size of the bar
    ax3.set_ylim(daily_low - 5, daily_high + 5)  # Set temperature range
    # ax3.yaxis.set_ticks(np.arange(daily_low *.8, daily_high *1.2, 10))  # Set ticks
    ax3.yaxis.tick_right()  # Ticks on the right

    # Draw colored bar
    ax3.axvspan(-1, 1, facecolor='gainsboro', alpha=0.5)

    # Mark current, high, and low temperatures
    ax3.plot(-1.2, weather_data['temperature']-1, marker=5, color='black', clip_on=False, markersize=12) #Triangle marker
    # Previous Hour
    ax3.plot(-1.2, prev_hour['temperature']-1, marker=5, color='dimgrey', alpha = 0.85 , clip_on=False, markersize=12) #Triangle marker
    
    ax3.axhline(daily_high, color='red', linestyle='-', linewidth=4)
    ax3.axhline(daily_low, color='blue', linestyle='-', linewidth=4)
    #Format axes
    ax3.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax3.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax3.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: '%d' % y))
    ax3.tick_params(axis='y', which='major', labelbottom=False, labeltop=True, labelsize=16,
                         color = 'black', length=4, width=1.5)
    ax3.tick_params(axis='y', which='minor', labelbottom=False, color ='dimgrey', length=2, width=1)
    ax3.set_xticks([])

    table_data = [["Humidity", f"{weather_data['relativehumidity']}%"],
                  ["Prcp. prob", f"{weather_data['precipitation_probability'].round(0)}%"],
                  ["UV Index", f"{weather_data['uvindex']}/11"],
                  ["Wind", f"{weather_data['windspeed'].astype(int)} mph"]]

    table = Table(ax1, bbox=[0.775, 0.525, 0.425, 0.4])  # Adjusted table width
    table.auto_set_font_size(False) # Disable auto font size
    for i, row in enumerate(table_data):
        for j, cell in enumerate(row):
            if j == 0:
                cell_obj = table.add_cell(i, j, width=0.22, height=0.295, text=cell, loc='right')
            else:
                cell_obj = table.add_cell(i, j, width=0.2, height=0.295, text=cell, loc='center')

            cell_obj.get_text().set_fontsize(14)  # set fontsize here.

        ax1.add_table(table)

    # Polar subplot for wind direction
    ax2 = fig.add_axes([0.55, 0.075, 0.5, 0.35], projection='polar')
    wind_dir = np.radians(weather_data['winddirection']+180)
    wind_source = np.radians(weather_data['winddirection'])
    wind_speed = weather_data['windspeed']

    ax2.arrow(wind_dir,0,0,wind_speed , head_width=0.3, length_includes_head = True,lw=2, head_length=wind_speed*.25,  fc='black',zorder =9) #, ec='black')
    ax2.arrow(wind_source,0,0,wind_speed , head_width=0.0, length_includes_head = True,lw=2, head_length=0, fc='black', zorder =9) #, ec='black')
    ax2.set_theta_zero_location("N")
    ax2.set_theta_direction(-1)
    ax2.set_rmax(wind_speed *1.25)
    ax2.set_xticks(np.radians([0,90,180,270]) , labels = ['N','E','S','W'])
    ax2.set_xticks(np.radians([45,135,225,315]), minor=True)
    
    if 0 < wind_speed <5:
        ax2.set_rticks([])
    elif 5 <= wind_speed < 25:
        ax2.set_rticks([10])
        ax2.set_rlabel_position(weather_data['winddirection']+180)
    elif 25 < wind_speed:
        ax2.set_rticks([20])
        ax2.set_rlabel_position(weather_data['winddirection']+180)
    elif wind_speed > 35 :
        ax2.set_rticks([15,30])
        ax2.set_rlabel_position(weather_data['winddirection']+180)

    
    ax2.tick_params(axis='x', which='major', labelsize=13, pad=1, color = 'black', length=4, width=1.5)
    ax2.tick_params(axis='y', which='major', labelsize=10, color = 'lightgrey', length=4, width=1.5)
    
    tick = [ax2.get_rmax(),ax2.get_rmax()*0.95]
    for t  in np.deg2rad(np.arange(0,360,45)):
        ax2.plot([t,t], tick, lw=2, color="k")
    for t  in np.deg2rad(np.arange(0,360,15)):
        ax2.plot([t,t], tick, lw=.75, color="gray")
    # plt.savefig('/home/noah/Documents/current_conditions.png', dpi = 100)
    
    buf = io.BytesIO()
    plt.savefig(buf, format = 'png')
    buf.seek(0) # Rewind the buffer to the beginning
    
    img = Image.open(buf)
    img = ImageEnhance.Color(img).enhance(0)
    # img.save('Images/current_weather.png')
    img.show()

create_weather_display(df)
