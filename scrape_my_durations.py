import json
import os

import pandas as pd

from configs import PATHS
from utils.scrape_utils import get_paths, read_my_durations

DATA_PATH = get_paths(PATHS)


def main():

    credentials_path = os.path.join(DATA_PATH, "puregym_credentials.json")

    with open(credentials_path, "r") as read_file:
        credentials = json.load(read_file)

    file_path = os.path.join(os.path.join(DATA_PATH, "data_durations"), "durations.csv")

    if os.path.isfile(file_path):
        durations = pd.read_csv(file_path)
        durations["date"] = pd.to_datetime(durations["date"], format="%Y-%m-%d")
    else:
        durations = pd.DataFrame()

    new_durations = read_my_durations(credentials)
    durations = pd.concat([durations, new_durations], sort=True)
    durations = durations.drop_duplicates()
    durations = durations[["date", "duration"]]
    durations = durations.sort_values("date", ascending=True)

    durations.to_csv(file_path, index=False)


if __name__ == "__main__":
    main()
