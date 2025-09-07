#! home/noah/venv/bin/activate
import datetime
print(f"Timestamp: {datetime.datetime.now().strftime('%b %d,%Y %-I:%M %p')}")

print('Loading Libraries')
import os
import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import Normalize
from matplotlib import patheffects
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.dates as mdates
from matplotlib import patches
from matplotlib.ticker import MultipleLocator
from matplotlib.collections import LineCollection
from matplotlib.path import Path
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.image import imread
import matplotlib.dates as mdates
from matplotlib import patheffects
from zoneinfo import ZoneInfo
import io

#%% Load Data

data_path = 'Data/meteogram_data.pkl'

df = pd.read_pickle(data_path)


conf = {'lat' : 40.5853,
        'lon': -105.084,
        'asl' : 1525,
        'fmt' : 'csv',
        'unit_temp': 'F',
        'unit_wind' : 'mph',
        'unit_pcp' : 'inch',
        'city':'Fort Collins',
        'state':'CO'}


#%% Make Meteogram
def meteogram(df, conf):
    """Generates a meteogram plot with weather icons and temperature data."""

    print('Building Meteogram')

    # Create figure with two subplots: icons (top) and temperature (bottom)
    fig, (ax_icons, ax_temp) = plt.subplots(nrows=2,
                                            ncols=1,
                                            figsize=((800 / 100), (480 / 100)),
                                            dpi=100,
                                            gridspec_kw={'height_ratios': [1, 7]})
                                            # sharex=True)
    fig.subplots_adjust(hspace=0)  # Reduce space between subplots

    ax_temp.set_facecolor('whitesmoke')

    # Plot temperature
    ax_temp.plot(df.time, df.temperature, color='dimgrey', zorder=9)
    ax_temp.set_xlim(df.time.min(), df.time.max())

    # Daylight shading
    y_max = ax_temp.get_ylim()[1]
    for d in df.date.unique():
        ax_temp.fill_between(
            df[(df.date == d) & (df.isdaylight == 1)]['time'],
            y1=df[(df.date == d) & (df.isdaylight == 1)]['temperature'],
            y2=y_max,
            color='#FFD903', alpha=0.2, zorder=1,
        )

    # Annotate daily max/min temperatures
    for d in df.date.unique():
        day_data = df[df.date == d]
        if day_data.shape[0] > 23:
            max_temp = day_data[day_data.isdaylight == 1]['temperature'].max()
            max_time = day_data.loc[day_data[day_data.isdaylight == 1]['temperature'].idxmax(), 'time']
            min_temp = day_data[day_data.isdaylight == 0]['temperature'].min()
            min_time = day_data.loc[day_data[day_data.isdaylight == 1]['temperature'].idxmin(), 'time']

            for temp, time, offset in [(max_temp, max_time, (-12.5, -1)), (min_temp, min_time, (0, -10))]:
                ax_temp.annotate(
                    f"{temp:.0f}°", xy=(time, temp), xytext=offset,
                    textcoords="offset points", ha="center", va="center",
                    path_effects=[patheffects.withStroke(linewidth=4, foreground='whitesmoke')],
                    fontsize=9, fontweight='bold', color='black', zorder=10,
                )

    # Current time line and annotation
    current_time = datetime.datetime.now()
    nearest_hour = pd.Timestamp.now().round('60min').to_pydatetime()
    current_temp = df[df.time == nearest_hour]['temperature'].values[0]
    temp_yloc = np.mean([current_temp, df.temperature.min()])

    ax_temp.axvline(current_time, color='black', alpha=0.5, linestyle='--', linewidth=1.5, zorder=10)
    ax_temp.annotate(
        f"{current_temp:.0f}°F", xy=(current_time, temp_yloc), xytext=(0, 10),
        textcoords="offset points", path_effects=[patheffects.withStroke(linewidth=4, foreground='whitesmoke')],
        fontsize=14, fontweight='bold', ha='center', va='bottom', zorder=11,
    )

    # Weather icons (top subplot)
    icon_folder = 'icons/meteo_icons'
    # ax_icons.set_axis_off()  # Turn off axes for icons
    
    ax_icons.set_xlim(ax_temp.get_xlim())
    
    # Create the secondary x-axis (top)
    # Format x-axis for icons (date on top)
    ax_icons.xaxis.set_major_locator(mdates.HourLocator(byhour=11, interval = 1))
    ax_icons.xaxis.set_major_formatter(mdates.DateFormatter('%a %-d %b')) # Format as 'Wed 5 Feb'
    ax_icons.tick_params(axis='x', which='major', labelbottom=False, labeltop=True, labelsize=12,
                         length=0, width=0)
    ax_icons.get_yaxis().set_ticks([])

    for pos in ['top','right','bottom','left']:
        ax_icons.spines[pos].set_visible(False)
    

    for i, row in df.iterrows():
        if row['time'].hour ==12 :  # Check for 12 AM and 12 PM
            pict_code = f"{row['pictocode']:02d}"
            icon_path = os.path.join(icon_folder, f"{pict_code}_{'day' if row['isdaylight'] else 'night'}.png")
    
            if os.path.exists(icon_path):
                try:
                    img = imread(icon_path)
                    im = OffsetImage(img, zoom = 1.2)
                    ab = AnnotationBbox(im, (mdates.date2num(row['time']),0.25), xycoords='data', frameon=False)
                    ax_icons.add_artist(ab)
                except Exception as e:
                    print(f"Error loading icon: {e}")

    # Temperature color bands
    cmap = mpl.colormaps['Spectral_r']
    norm = Normalize(vmin=-10, vmax=110)
    get_color = lambda t: mpl.colors.to_hex(cmap((t - norm.vmin) / (norm.vmax - norm.vmin)))

    y_lim = ax_temp.get_ylim()[0]
    t_grads = np.arange((y_lim // 5) * 5, df.temperature.max() + 5, 5)

    for t in t_grads:
        clipped_upper = np.minimum(df.temperature, t + 5)
        ax_temp.fill_between(
            df.time, t, clipped_upper,
            where=(df.temperature + 0.5 >= t) & (df.temperature >= t - 5),
            color=get_color(t), alpha=1, step=None, interpolate=True, zorder=1, edgecolor='none',
        )

    # Format axes
    ax_temp.xaxis.set_minor_locator(mdates.HourLocator(interval=6))
    ax_temp.xaxis.set_minor_formatter(mdates.DateFormatter('%-H'))
    ax_temp.xaxis.set_major_locator(mdates.DayLocator())
    ax_temp.xaxis.set_major_formatter(mdates.DateFormatter('%a'))
    ax_temp.tick_params(axis='x', which='major', length=8, width=1.5, color='black', labelsize=11, pad=5)
    ax_temp.tick_params(axis='x', which='minor', length=4, width=.75, color='black', labelsize=9)

    ax_temp.yaxis.set_minor_locator(MultipleLocator(base=1))
    ax_temp.yaxis.set_major_formatter(lambda x, pos: f'{x:.0f}°')
    ax_temp.tick_params(axis='y', which='major', length=5, width=1.5, color='dimgrey', labelsize=11, pad=3)
    ax_temp.tick_params(axis='y', which='minor', length=3, width=1, color='lightgrey')

    for pos in ['top','right']:
        ax_temp.spines[pos].set_visible(False)

    # fig.autofmt_xdate(ha='center', rotation=0)

    # Title and subtitle
    
    ## Get Forecast Time
    mod_timestamp = os.path.getmtime(data_path)
    utc_time = datetime.datetime.fromtimestamp(mod_timestamp, tz=datetime.timezone.utc)
    local_tz = ZoneInfo("America/Denver")
    local_time = utc_time.astimezone(local_tz)
    forecast_time = local_time.strftime("%-d %b %-I:%M %p")
    
    title_string = f"{conf['city']}, {conf['state']} - ({conf['lat']:.2f}, {conf['lon']:.2f}) {conf['asl']}m\nForecast Time: {forecast_time}"
    
    plt.suptitle(title_string,fontsize=13, x=0.0735, y=0.95, ha='left', fontweight='bold')

    # plt.tight_layout()
    plt.subplots_adjust(top = .9, bottom=.001, hspace=0, wspace=0)
    plt.tight_layout(h_pad=-.5)
    
    # Save Fig to in-memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format = 'png')
    buf.seek(0) # Rewind the buffer to the beginning
    
    img = Image.open(buf)
    img = ImageEnhance.Color(img).enhance(0)
    img.save('Images/meteogram.png')
    
        
meteogram(df, conf)


