# Raspi Meteogram

## Future Features:
- [X] Increase saturation of image display
- [X] Implement precipitation data into figure
- [X] Insert current hourly temp on figure
- [X] Update color ramp to be more consistent with meteoblue
----
Transfer Files from Pi to Mac:

`sudo scp noah@pizero.local:/home/noah/meteogram.py /Volumes/980_EVO/Python/Meteogram/meteogram_pi.py`

Transfer Files from Mac to Pi:

`sudo scp /Volumes/980_EVO/Python/Meteogram/meteogram_pi.py noah@pizero.local:/home/noah/meteogram.py `


sudo scp /Volumes/980_EVO/Python/PiZero/date_figure_pi.py noah@pizero.local:/home/noah/date_figure_pi.py 

---

Get latests weather data:

`sudo scp noah@pizero.local:/home/noah/Documents/meteogram_data.pkl /Volumes/980_EVO/Python/Meteogram/meteogram_data.pkl`

Get Definition DF:
`sudo scp /Volumes/980_EVO/Python/PiZero/definition_pi.py noah@pizero.local:/home/noah/Documents/definition_pi.py`

sudo scp /Volumes/980_EVO/Python/Meteogram/current_weather.py noah@pizero.local:/home/noah/current_weather.py 

# Configuration for Display

1. Create *.sh* file for script

```
#!/bin/bash

source venv/bin/activate

python3 meteogram.py

```

2. Make executable:
In Terminal:
```
chmod +x runner.sh
```

3. Schedule with chrontab

