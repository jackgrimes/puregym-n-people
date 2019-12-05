import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

from configs import DAYS_OF_WEEK


def read_and_process_data(data_path):
    files = os.listdir(os.path.join(data_path, "data_n_people"))
    full_file_paths = [
        os.path.join(os.path.join(data_path, "data_n_people"), file)
        for file in files
        if (".csv" in file)
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
    return n_people


def plotter(n_people, time_str, DATA_PATH):
    fig, ax = plt.subplots(figsize=(24, 8))
    plt.plot(n_people, label="Number of people in the gym")
    ax.set_ylim(bottom=0)
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of people in gym")
    plt.tight_layout()
    plt.savefig(
        os.path.join(
            os.path.join(DATA_PATH, "graphs"), time_str + "_all_time_graph.png"
        )
    )


def plotter_by_day(n_people, time_str, data_path):
    n_people_df = n_people.reset_index(drop=False)
    n_people_df["date"] = n_people_df.time.dt.strftime("%Y_%m_%d")
    n_people_df["time_decimal"] = (
        n_people_df["time"].dt.hour
        + (n_people_df["time"].dt.minute / 60)
        + n_people_df["time"].dt.second / 3600
    )

    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot each day's data
    for date in (
        list(n_people_df.date.unique())[2:] + list(n_people_df.date.unique())[:1]
    ):
        day = pd.to_datetime(date, format="%Y_%m_%d").strftime(format="%A")
        n_people_df_this_date = n_people_df[n_people_df["date"] == date]
        n_people_df_this_date = n_people_df_this_date[
            ["n_people", "time", "time_decimal"]
        ]
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
    ax.set_xlabel("Time of day")
    ax.set_ylabel("Number of people in gym")
    plt.tight_layout()
    plt.savefig(
        os.path.join(os.path.join(data_path, "graphs"), time_str + "_by_day_graph.png")
    )


def get_decimal_time_and_day_of_week(n_people):
    n_people_df = n_people.reset_index(drop=False)
    n_people_df["date"] = n_people_df.time.dt.strftime("%Y_%m_%d")

    fig, ax = plt.subplots(figsize=(12, 8))

    n_people_df["day"] = n_people_df.time.dt.strftime("%A")

    n_people_df["time_decimal"] = (
        n_people_df["time"].dt.hour
        + (n_people_df["time"].dt.minute / 60)
        + n_people_df["time"].dt.second / 3600
    )

    return n_people_df, fig, ax


def put_all_data_for_this_day_of_week_on_a_single_day(day, data_by_day_of_week):
    this_day_of_week_data = data_by_day_of_week[day]

    this_day_of_week_data_on_single_date = this_day_of_week_data.set_index(
        "time_decimal", drop=False
    ).sort_index()
    this_day_of_week_data_on_single_date[
        "hours"
    ] = this_day_of_week_data_on_single_date["time"].dt.strftime("%H")
    this_day_of_week_data_on_single_date[
        "minutes"
    ] = this_day_of_week_data_on_single_date["time"].dt.strftime("%M")
    this_day_of_week_data_on_single_date[
        "seconds"
    ] = this_day_of_week_data_on_single_date["time"].dt.strftime("%S.%f")

    this_day_of_week_data_on_single_date["year"] = 2000
    this_day_of_week_data_on_single_date["month"] = 1
    this_day_of_week_data_on_single_date["day"] = 1
    this_day_of_week_data_on_single_date["dttime"] = pd.to_datetime(
        this_day_of_week_data_on_single_date[
            ["year", "month", "day", "hours", "minutes", "seconds"]
        ]
    )
    this_day_of_week_data_on_single_date.set_index("dttime", drop=True, inplace=True)

    return this_day_of_week_data_on_single_date


def get_and_plot_data_by_day_of_week(n_people_df, plotting):
    data_by_day_of_week = {}

    for day in DAYS_OF_WEEK:
        this_day_of_week_data = n_people_df[n_people_df["day"] == day]
        this_day_of_week_data.set_index("time_decimal", drop=True)
        data_by_day_of_week[day] = this_day_of_week_data

        if plotting:
            marker = "o"
        else:
            marker = ""

        plt.plot(
            this_day_of_week_data["time_decimal"],
            this_day_of_week_data["n_people"],
            marker=marker,
            markersize=2,
            ls="",
            label=day,
            alpha=0.3,
        )

    return data_by_day_of_week


def linear_interpolation(this_day_of_week_data_on_single_date):
    oidx = this_day_of_week_data_on_single_date.index
    nidx = pd.date_range(oidx.min(), oidx.max(), freq="1000s")

    interpolated = (
        this_day_of_week_data_on_single_date["n_people"]
        .reindex(oidx.union(nidx))
        .interpolate("linear")
        .reindex(nidx)
    )

    interpolated = pd.DataFrame(interpolated)
    interpolated["time_decimal"] = (
        interpolated.index.hour
        + (interpolated.index.minute / 60)
        + interpolated.index.second / 3600
    )

    return interpolated


def spline_interpolation(interpolated):
    times = np.linspace(
        interpolated["time_decimal"].min(), interpolated["time_decimal"].max(), 3000,
    )

    spl = make_interp_spline(
        interpolated["time_decimal"], interpolated["n_people"], k=3
    )  # type: BSpline
    power_smooth = spl(times)

    return times, power_smooth


def tidy_legend(ax):
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


def tidy_axes(ax):
    plt.xticks(np.arange(0, 24, 1))
    labels = ax.get_xticks().tolist()
    labels = [(str(label) + ":00") for label in labels]
    ax.set_xticklabels(labels)
    plt.grid(b=True, which="major", color="grey", linestyle="-")
    ax.set_ylim(bottom=0)
    ax.set_xlim([5, 24])
    ax.legend()
    ax.set_xlabel("Time of day")
    ax.set_ylabel("Number of people in gym")


def plotter_by_day_average(n_people, time_str, data_path, plotting):
    n_people_df, fig, ax = get_decimal_time_and_day_of_week(n_people)

    data_by_day_of_week = get_and_plot_data_by_day_of_week(n_people_df, plotting)

    for day in data_by_day_of_week.keys():
        this_day_of_week_data_on_single_date = put_all_data_for_this_day_of_week_on_a_single_day(
            day, data_by_day_of_week
        )
        interpolated = linear_interpolation(this_day_of_week_data_on_single_date)
        times, power_smooth = spline_interpolation(interpolated)
        plt.plot(times, power_smooth, label=day)

    tidy_legend(ax)
    tidy_axes(ax)

    if plotting:
        figure_path = os.path.join(
            os.path.join(data_path, "graphs"),
            time_str + "_by_day_average_graph_with_points.png",
        )
    else:
        figure_path = os.path.join(
            os.path.join(data_path, "graphs"), time_str + "_by_day_average_graph.png"
        )

    plt.tight_layout()
    plt.savefig(figure_path)


def plot_time_per_visit(durations, DATA_PATH, time_str):
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.plot(
        durations["date"],
        durations["duration"],
        marker="o",
        markersize=2,
        ls="",
        alpha=1,
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Time spent in gym (minutes)")
    plt.tight_layout()
    plt.savefig(
        os.path.join(
            os.path.join(DATA_PATH, "graphs"), time_str + "_duration_per_visit.png"
        )
    )


def plot_time_per_week(durations, DATA_PATH, time_str):
    durations_grouped = (
        durations.groupby([pd.Grouper(key="date", freq="W-SUN")])
        .sum()
        .reset_index()
        .sort_values("date")
    )
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlabel("Date")
    ax.set_ylabel("Time spent in gym over week (minutes)")
    plt.plot(
        durations_grouped["date"], durations_grouped["duration"],
    )
    plt.tight_layout()
    plt.savefig(
        os.path.join(
            os.path.join(DATA_PATH, "graphs"), time_str + "_duration_per_week.png"
        )
    )


def plot_durations_histogram(durations, DATA_PATH, time_str):
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.hist(durations["duration"], bins=20)
    ax.set_xlabel("Time spent in gym over week (minutes)")
    ax.set_ylabel("Count")
    plt.tight_layout()
    plt.savefig(
        os.path.join(
            os.path.join(DATA_PATH, "graphs"), time_str + "_histogram_of_durations.png"
        )
    )
