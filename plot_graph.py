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

(
    CSV_PATH,
    CREDENTIALS_PATH,
    GRAPH_PATH,
    BY_DAY_GRAPH_PATH,
    BY_DAY_AVERAGE_GRAPH_PATH,
) = get_paths(PATHS)


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


def plotter_by_day(n_people):
    n_people_df = n_people.reset_index(drop=False)
    n_people_df["date"] = n_people_df.time.dt.strftime("%Y_%m_%d")
    n_people_df["time_decimal"] = (
        n_people_df["time"].dt.hour
        + (n_people_df["time"].dt.minute / 60)
        + n_people_df["time"].dt.second / 3600
    )

    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot each day's data
    for date in n_people_df.date.unique():
        day = pd.to_datetime(date, format="%Y_%m_%d").strftime(format="%A")
        n_people_df_this_date = n_people_df[n_people_df["date"] == date]
        n_people_df_this_date = n_people_df_this_date[
            ["n_people", "time", "time_decimal"]
        ]
        plt.plot(
            n_people_df_this_date["time_decimal"],
            n_people_df_this_date["n_people"],
            # marker='o',
            # markersize=2,
            # ls='',
            label=day,
            # alpha=0.2,
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


def plotter_by_day_average(n_people):
    n_people_df = n_people.reset_index(drop=False)
    n_people_df["date"] = n_people_df.time.dt.strftime("%Y_%m_%d")

    fig, ax = plt.subplots(figsize=(12, 8))

    n_people_df["day"] = n_people_df.time.dt.strftime("%A")

    n_people_df["time_decimal"] = (
        n_people_df["time"].dt.hour
        + (n_people_df["time"].dt.minute / 60)
        + n_people_df["time"].dt.second / 3600
    )

    data_by_day_of_week = {}

    for day in n_people_df["day"].unique():
        this_day_of_week_data = n_people_df[n_people_df["day"] == day]
        this_day_of_week_data.set_index("time_decimal", drop=True)
        data_by_day_of_week[day] = this_day_of_week_data

        plt.plot(
            this_day_of_week_data["time_decimal"],
            this_day_of_week_data["n_people"],
            marker="o",
            markersize=2,
            ls="",
            label=day,
            alpha=0.3,
        )

    for day in data_by_day_of_week.keys():
        this_day_of_week_data = data_by_day_of_week[day]

        x = this_day_of_week_data.set_index("time_decimal", drop=False).sort_index()
        x["hours"] = x["time"].dt.strftime("%H")
        x["minutes"] = x["time"].dt.strftime("%M")
        x["seconds"] = x["time"].dt.strftime("%S.%f")

        x["year"] = 2000
        x["month"] = 1
        x["day"] = 1
        x["dttime"] = pd.to_datetime(
            x[["year", "month", "day", "hours", "minutes", "seconds"]]
        )
        x.set_index("dttime", drop=True, inplace=True)

        oidx = x.index
        nidx = pd.date_range(oidx.min(), oidx.max(), freq="1000s")

        interpolated = (
            x["n_people"].reindex(oidx.union(nidx)).interpolate("linear").reindex(nidx)
        )

        interpolated = pd.DataFrame(interpolated)
        interpolated["time_decimal"] = (
            interpolated.index.hour
            + (interpolated.index.minute / 60)
            + interpolated.index.second / 3600
        )
        #
        # from scipy.interpolate import UnivariateSpline
        # x = interpolated["time_decimal"]
        # y = interpolated["n_people"]
        # plt.plot(x, y, 'ro', ms=5)

        from scipy.interpolate import make_interp_spline, BSpline

        xnew = np.linspace(
            interpolated["time_decimal"].min(), interpolated["time_decimal"].max(), 300
        )

        spl = make_interp_spline(
            interpolated["time_decimal"], interpolated["n_people"], k=3
        )  # type: BSpline
        power_smooth = spl(xnew)

        plt.plot(xnew, power_smooth, label=day)

        # plt.plot(
        #     interpolated["time_decimal"],
        #     interpolated["n_people"],
        #     label=day,
        # )

    # Make sure different lines for the same day of week share a colour and label
    names = []
    for i, p in enumerate(ax.get_lines()):
        # this is the loop to change Labels and colors
        if p.get_label() in names[:i]:  # check for Name already exists
            idx = names.index(p.get_label())  # find ist index
            p.set_c(ax.get_lines()[idx].get_c())  # set color
            # p.set_label("_" + p.get_label())
        names.append(p.get_label())

    names = []
    for i, p in enumerate(ax.get_lines()):
        # this is the loop to change Labels and colors
        if "_" + p.get_label() not in names[:i]:  # check for Name already exists
            # idx = names.index(p.get_label())  # find ist index
            # p.set_c(ax.get_lines()[idx].get_c())  # set color
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
    plt.savefig(BY_DAY_AVERAGE_GRAPH_PATH)
    plt.show()


if __name__ == "__main__":
    plotter(n_people, rolling, interpolated)
    plotter_by_day(n_people)
    plotter_by_day_average(n_people)
