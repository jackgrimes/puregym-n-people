import json
import os

import pandas as pd

from configs import PATHS
from utils.scrape_utils import get_paths, read_my_durations, process_new_durations
import datetime

DATA_PATH = get_paths(PATHS)


def main():

    credentials_path = os.path.join(DATA_PATH, "puregym_credentials.json")

    with open(credentials_path, "r") as read_file:
        credentials = json.load(read_file)

    file_path = os.path.join(os.path.join(DATA_PATH, "data_durations"))

    previous_scrapings = [
        os.path.join(file_path, file)
        for file in os.listdir(file_path)
        if (".csv" in file)
    ]
    durations = pd.concat([pd.read_csv(path) for path in previous_scrapings])
    durations["date"] = pd.to_datetime(durations["date"], format="%Y-%m-%d")

    scraped_durations = read_my_durations(credentials)

    new_durations = process_new_durations(scraped_durations, durations)

    new_durations.to_csv(
        os.path.join(
            file_path,
            "durations_scraped_"
            + datetime.datetime.now().strftime("%Y_%m_%d")
            + ".csv",
        ),
        index=False,
    )


if __name__ == "__main__":
    main()
