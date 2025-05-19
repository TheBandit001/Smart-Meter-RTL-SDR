import subprocess
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta

plt.figure(figsize=(12, 6))

timestamps = []
values = []

def read_rtlamr():
    return subprocess.Popen(
        # CHANGE -filterid=64259716 <--  TO YOUR METER ID
        ["rtlamr", "-filterid=64259716", "-format=json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

proc = read_rtlamr()

def get_rounded_hour(dt):
    return dt.replace(minute=0, second=0, microsecond=0)

start_time = get_rounded_hour(datetime.now())
end_time = start_time + timedelta(hours=12)

latest_value_text = None

def update(frame):
    global proc, start_time, end_time

    line = proc.stdout.readline()
    if line:
        try:
            data = json.loads(line)
            reading = int(data['Message']['Consumption'])
            ts = datetime.now()

            timestamps.append(ts)
            values.append(reading)

            if len(values) > 100:
                timestamps.pop(0)
                values.pop(0)

            if ts >= end_time:
                start_time += timedelta(hours=1)
                end_time += timedelta(hours=1)

            ax = plt.gca()
            ax.clear()
            ax.plot(timestamps, values, marker='o', linestyle='-')

            ax.set_title("NB Power Live Meter Reading")
            ax.set_xlabel("Time")
            ax.set_ylabel("Consumption")

            min_val = min(values)
            max_val = max(values)
            ax.set_ylim(min_val - 10, max_val + 10)
            ax.set_xlim(start_time, end_time)

            ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))

            plt.gcf().autofmt_xdate()
            plt.tight_layout()

            # Always re-add latest value text on every frame
            ax.text(
                0.01, 1.02, f"Latest Reading: {reading}",
                transform=ax.transAxes,
                ha='left', va='bottom',
                fontsize=12, color='blue'
            )

        except (json.JSONDecodeError, KeyError):
            pass


plt.plot([], [])
plt.title("Live Meter Reading")
plt.xlabel("Time")
plt.ylabel("Consumption")
plt.tight_layout()
plt.show(block=False)

ani = FuncAnimation(plt.gcf(), update, interval=60000)

plt.show()
