import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict, OrderedDict
data = pd.read_excel("../data/queues1.xlsx")
wait_time_bins = []

def plot_arrival_histogram(hist,date):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_title(f'Wating time vs Number of calls for {date}/10')
    ax.set_ylabel('Number of clients')
    ax.set_xlabel('Hour of the day')
    plt.bar(hist.keys(), hist.values())
    plt.show()

days = ["03","04","05","06","07",10,11, 12, 13, 14, 17, 18,19, 20, 21, 24, 25, 26, 27, 28,31]
avgs = 0
for day in days:
    rest_count = 0
    mask = data['Date in Text'].str.startswith(f"10/{day}/2021").fillna(value=False)
    #print(data[mask])
    d = defaultdict(int)
    avg = data[mask]
    c = 0
    t = 0

    for index, row in data[mask].iterrows():

        c += 1
        t += row["Wait"]
        time_bin = f'{int(row["Wait"] // 60)}.{str((round((row["Wait"] / 60) * 2) / 2)).split(".")[1]}'
        d[time_bin] += 1
        if row['Queue'] == 'מסעדות':
            rest_count += 1
    d1 = OrderedDict(sorted(d.items(), key=lambda x: float(x[0])))
    # print(dict(d))
    print(f"avg wait time for day {day}-{t/c}")
    avgs += t/c
    print(rest_count, dict(d1))
    rest_count = 0
    plot_arrival_histogram(dict(d1), day)
print(avgs / len(days))


