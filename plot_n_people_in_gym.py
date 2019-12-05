import datetime
import platform

import pandas as pd

from configs import PATHS
from utils.plot_utils import (
    read_and_process_data,
    plotter,
    plotter_by_day,
    plotter_by_day_average,
)
from utils.scrape_utils import get_paths

if platform.system() == "Windows":
    pd.plotting.register_matplotlib_converters()

data_path = get_paths(PATHS)
time_str = datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")

n_people = read_and_process_data(data_path)

if __name__ == "__main__":
    plotter(n_people, time_str, data_path)
    plotter_by_day(n_people, time_str, data_path)
    plotter_by_day_average(n_people, time_str, data_path, True)
    plotter_by_day_average(n_people, time_str, data_path, False)
