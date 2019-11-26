import os
import platform

import numpy as np
import pandas as pd
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter

from configs import PATHS
from utils import get_paths

if platform.system() == "Windows":
    pd.plotting.register_matplotlib_converters()

CSV_PATH, CREDENTIALS_PATH, GRAPH_PATH, BY_DAY_GRAPH_PATH = get_paths(PATHS)


def read_and_process_data(CSV_PATH):
    files = os.listdir(CSV_PATH)
    full_file_paths = [
        os.path.join(CSV_PATH, file) for file in files if (".csv" in file)
    ]
    df = pd.concat(
        [
            pd.read_csv(full_file_path, index_col=0, names=["time", "n_people"])
            for full_file_path in full_file_paths
        ],
        axis=0,
    )

    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    n_people = df["n_people"]
    rolling = n_people.rolling(7).mean(center=True)

    oidx = df.index
    nidx = pd.date_range(oidx.min(), oidx.max(), freq="s")
    interpolated = (
        df["n_people"].reindex(oidx.union(nidx)).interpolate("cubic").reindex(nidx)
    )

    return n_people, rolling, interpolated


n_people, rolling, interpolated = read_and_process_data(CSV_PATH)


def plotter(n_people, rolling, interpolated):
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.plot(n_people, label="Number of people in the gym")
    plt.plot(rolling, label="Rolling average")
    plt.plot(interpolated, label="Interpolated")

    ax.tick_params(which="major", width=1.00, length=15)
    ax.tick_params(which="minor", width=0.75, length=2.5, labelsize=10)

    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    xfmt = mdates.DateFormatter("%A")
    ax.xaxis.set_major_formatter(xfmt)
    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_minor_formatter(DateFormatter("%H"))

    ax.set_ylim(bottom=0)

    ax.legend()
    plt.tight_layout()

    plt.savefig(GRAPH_PATH)
    plt.show()


# plotter(n_people, rolling, interpolated)


def plotter_by_day(n_people):
    n_people_df = n_people.reset_index(drop=False)
    n_people_df["date"] = n_people_df.time.dt.strftime("%Y_%m_%d")

    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot each day's data
    for date in n_people_df.date.unique():
        day = pd.to_datetime(date, format="%Y_%m_%d").strftime(format="%A")
        n_people_df_this_date = n_people_df[n_people_df["date"] == date]
        n_people_df_this_date = n_people_df_this_date[["n_people", "time"]]
        n_people_df_this_date["time_decimal"] = (
            n_people_df_this_date["time"].dt.hour
            + (n_people_df_this_date["time"].dt.minute / 60)
            + n_people_df_this_date["time"].dt.second / 3600
        )
        plt.plot(
            n_people_df_this_date["time_decimal"],
            n_people_df_this_date["n_people"],
            label=day,
        )

    # Make sure different lines for the same day of week share a colour and label
    names = []
    for i, p in enumerate(ax.get_lines()):
        # this is the loop to change Labels and colors
        if p.get_label() in names[:i]:  # check for Name already exists
            idx = names.index(p.get_label())  # find ist index
            p.set_c(ax.get_lines()[idx].get_c())  # set color
            p.set_label("_" + p.get_label())
        names.append(p.get_label())

    # Axes configuration
    plt.xticks(np.arange(0, 24, 1))
    labels = ax.get_xticks().tolist()
    labels = [(str(label) + ":00") for label in labels]
    ax.set_xticklabels(labels)
    plt.grid(b=True, which="major", color="grey", linestyle="-")
    ax.set_ylim(bottom=0)
    ax.set_xlim([5, 24])
    ax.legend()
    plt.tight_layout()
    plt.savefig(BY_DAY_GRAPH_PATH)
    plt.show()


plotter_by_day(n_people)
