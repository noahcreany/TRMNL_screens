#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  1 09:20:51 2025

@author: noahcreany
"""


import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pytz
from astral import LocationInfo
from astral.sun import sun
from astral.moon import phase
from zoneinfo import ZoneInfo
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

def create_date_figure():
    """Creates a 640x400 figure displaying date, day/week of year, and sunrise/sunset info."""

    # Figure setup
    fig, ax = plt.subplots(figsize=((800 / 100), (480 / 100)),dpi=100)  # 640x400 pixels

    # Date and time
    denver_tz = ZoneInfo("America/Denver")
    now = datetime.now(denver_tz)
    
    date_str = now.strftime("%a %-d %b %y")


    # Location info for Fort Collins
    city = LocationInfo("Fort Collins", "USA", "America/Denver", 40.5853, -105.084)
    s = sun(city.observer, date=now.date(), tzinfo=city.timezone)

    sunrise = s["sunrise"].strftime("%I:%M %p").lstrip('0')
    sunset = s["sunset"].strftime("%I:%M %p").lstrip('0')


    # Calculate daylight hours
    daylight_duration = s["sunset"] - s["sunrise"]
    hours = daylight_duration.seconds // 3600
    minutes = (daylight_duration.seconds % 3600) // 60
    daylight = f"{hours}h {minutes}m"
    
    
    # Day Progress
    day_progress = f"{(now - s['sunrise']).total_seconds()/(daylight_duration.total_seconds()):.0%}"
    
    # Tomorrow Sunrise/Sunset
    tomorrow = now + timedelta(days=1)
    tomorrow = s = sun(city.observer, date=tomorrow, tzinfo=city.timezone)
    
    tomorrow_sunrise = tomorrow["sunrise"].strftime("%I:%M %p").lstrip('0')
    tomorrow_sunset = tomorrow["sunset"].strftime("%I:%M %p").lstrip('0')
    
    # font = 'Arial'
    
    # Date    
    ax.text(0.5, 0.9, date_str, fontsize=40, va='top', ha = 'center', fontweight='semibold', color = 'black', family = font)

    
    # --- Alignment Coordinates ---
    x_label_end = 0.20    
    x_value_start = 0.225
    x_icons = .58
    
    
    # --- Text Properties ---
    label_fontsize = 15 
    value_fontsize = 28
    label_fontweight = 'regular'
    value_fontweight = 'medium'
    va = 'center' 
    
    # --- Y Positions ---
    y_sunrise = 0.65
    y_sunset = 0.55
    y_daylight = 0.7
    y_progress = .41

    
    # --- Plotting the Text ---
    # Sunrise
    ax.text(x_label_end, y_sunrise, 'Sunrise:', fontsize=label_fontsize, va=va, ha='right', fontweight=label_fontweight, family = font)
    ax.text(x_value_start, y_sunrise, f'{sunrise}', fontsize=value_fontsize, va=va, ha='left', fontweight=value_fontweight, family = font)
    
    # Sunset
    ax.text(x_label_end, y_sunset, 'Sunset:', fontsize=label_fontsize, va=va, ha='right', fontweight=label_fontweight, family = font)
    ax.text(x_value_start, y_sunset, f'{sunset}', fontsize=value_fontsize, va=va, ha='left', fontweight=value_fontweight, family = font)
    
    # Daylight
    ax.text(.695, y_daylight, 'Daylight:', fontsize=label_fontsize, va=va, ha='center', fontweight=label_fontweight, family = font)
    ax.text(.695, y_daylight -.12, f'{daylight}', fontsize=value_fontsize+20, va=va, ha='center', fontweight=value_fontweight, family = font)
    
    # Day Progress
    ax.text(.325,y_progress,'Day Progress:', fontsize = label_fontsize, va = va, ha = 'center', fontweight = label_fontweight, family = font)
    ax.text(.325,y_progress-.15,day_progress, fontsize = value_fontsize+20, va = va, ha = 'center', fontweight = value_fontweight, family = font)
    
    # Tomorrow
    ax.text(.695,y_progress,'Tomorrow:', fontsize = label_fontsize, va = va, ha = 'center', fontweight = label_fontweight, family = font)

    sunrise_icon = mpimg.imread('icons/sunrise.png')
    sunset_icon = mpimg.imread('icons/sunset.png')
    
    sunrise_icon = OffsetImage(sunrise_icon, zoom=0.2)  # Adjust zoom as needed
    sunrise_icon = AnnotationBbox(sunrise_icon, (x_icons, y_progress-.095), frameon=False) 
    
    sunset_icon = OffsetImage(sunset_icon, zoom=0.2)  # Adjust zoom as needed
    sunset_icon = AnnotationBbox(sunset_icon, (x_icons, y_progress-.195), frameon=False) 

    ax.add_artist(sunrise_icon)
    ax.add_artist(sunset_icon)
    ax.text(x_icons+.035, y_progress-.1, tomorrow_sunrise, fontsize=value_fontsize, va=va, ha='left', fontweight=value_fontweight, family = font)
    ax.text(x_icons+.035, y_progress-.2, tomorrow_sunset, fontsize=value_fontsize, va=va, ha='left', fontweight=value_fontweight, family = font)
    
    
    
    

    # Figure formatting
    ax.axis('off')  # Turn off axes

    plt.tight_layout() #prevents text from being cut off.
    plt.savefig('Images/sunrise.png')
    plt.show()


create_date_figure()