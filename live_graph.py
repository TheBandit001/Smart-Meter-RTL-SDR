import subprocess
import json
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta

plt.figure(figsize=(12, 6))

timestamps = []
values = []

def read_rtlamr():
    return subprocess.Popen(
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
stats_text_obj = None
instruction_text_obj = None  # <-- For "Press E to save"

def save_csv():
    with open('meter_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Timestamp', 'Consumption'])
        for t, v in zip(timestamps, values):
            writer.writerow([t.strftime('%Y-%m-%d %I:%M:%S %p'), v])
    print("CSV file saved as 'meter_data.csv'")

def save_image():
    plt.savefig('meter_reading.png')
    print("Graph image saved as 'meter_reading.png'")

def on_key(event):
    if event.key == 'e':
        save_csv()
        save_image()

def update(frame):
    global proc, start_time, end_time, latest_value_text, stats_text_obj, instruction_text_obj

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

            plt.cla()
            plt.plot(timestamps, values, marker='o', linestyle='-')

            plt.title("NB Power Live Meter Reading")
            plt.xlabel("Time")
            plt.ylabel("Consumption")

            min_val = min(values)
            max_val = max(values)
            plt.ylim(min_val - 10, max_val + 10)
            plt.xlim(start_time, end_time)

            plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))

            plt.gcf().autofmt_xdate()
            plt.tight_layout()

            # Remove previous texts before drawing new ones
            if latest_value_text:
                latest_value_text.remove()
            if stats_text_obj:
                stats_text_obj.remove()
            if instruction_text_obj:
                instruction_text_obj.remove()

            latest_value_text = plt.gca().text(
                0.01, 1.02, f"Latest Reading: {reading}",
                transform=plt.gca().transAxes, ha='left', va='bottom', fontsize=12, color='blue'
            )

            if len(values) > 1:
                avg_usage = (values[-1] - values[0]) / (len(values) - 1)
            else:
                avg_usage = 0

            estimated_daily_total = avg_usage * 1440

            stats_text = f"Avg usage: {avg_usage:.2f}\nEst. daily total: {estimated_daily_total:.2f}"
            stats_text_obj = plt.gca().text(
                0.01, 0.90, stats_text,
                transform=plt.gca().transAxes, ha='left', va='bottom', fontsize=10, color='green'
            )

            instruction_text_obj = plt.gca().text(
                0.01, 0.02, "Press E to save",
                transform=plt.gca().transAxes, ha='left', va='bottom', fontsize=10, color='gray'
            )

            # Save on every update (optional)
            # save_csv()
            # save_image()

        except (json.JSONDecodeError, KeyError):
            pass

plt.plot([], [])
plt.title("Live Meter Reading")
plt.xlabel("Time")
plt.ylabel("Consumption")
plt.tight_layout()

plt.gcf().canvas.mpl_connect('key_press_event', on_key)

plt.show(block=False)

ani = FuncAnimation(plt.gcf(), update, interval=60000)  # update every minute

plt.show()
