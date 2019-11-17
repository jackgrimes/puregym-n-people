import os
import platform

import pandas as pd
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter

from configs import PATHS
from utils import get_paths

if platform.system() == "Windows":
    pd.plotting.register_matplotlib_converters()

CSV_PATH, CREDENTIALS_PATH, GRAPH_PATH = get_paths(PATHS)

def read_and_process_data(CSV_PATH):
    files = os.listdir(CSV_PATH)
    full_file_paths = [os.path.join(CSV_PATH, file) for file in files if ('.csv' in file)]
    df = pd.concat(
        [pd.read_csv(full_file_path, index_col=0, names=['time', 'n_people']) for full_file_path in full_file_paths],
        axis=0)

    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    n_people = df['n_people']
    rolling = n_people.rolling(7).mean(center=True)

    oidx = df.index
    nidx = pd.date_range(oidx.min(), oidx.max(), freq='s')
    interpolated = df['n_people'].reindex(oidx.union(nidx)).interpolate('cubic').reindex(nidx)

    return n_people, rolling, interpolated


n_people, rolling, interpolated = read_and_process_data(CSV_PATH)


def plotter(n_people, rolling, interpolated):
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.plot(n_people, label="Number of people in the gym")
    plt.plot(rolling, label="Rolling average")
    plt.plot(interpolated, label="Interpolated")
    fig.autofmt_xdate(bottom=0.2, rotation=30, ha='right')
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_formatter(DateFormatter("%H:%M"))
    ax.legend()
    plt.tight_layout()
    plt.savefig(GRAPH_PATH)
    plt.show()


plotter(n_people, rolling, interpolated)
