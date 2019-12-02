import datetime
import json
import os
import time

import pandas as pd

from configs import (
    PATHS,
    TIME_BETWEEN_SCRAPES,
    TIME_BETWEEN_RETRIES,
)
from utils.scrape_utils import get_paths, print_updates, read_n_people

DATA_PATH = get_paths(PATHS)

def main():

    credentials_path = os.path.join(DATA_PATH, "puregym_credentials.json")

    with open(credentials_path, "r") as read_file:
        credentials = json.load(read_file)

    people_counts = pd.Series()

    file_path = os.path.join(
        os.path.join(DATA_PATH, "data"),
        datetime.datetime.now().strftime(
            "gym_people_counts_run_starting_%Y_%m_%d__%H_%M.csv"
        ),
    )

    errors_this_run = 0
    start_time = time.time()

    while True:
        try:
            people_counts = read_n_people(people_counts, credentials, file_path)
            print_updates(start_time, errors_this_run)
            time.sleep(TIME_BETWEEN_SCRAPES)
        except Exception as e:
            errors_this_run += 1
            print(e)
            print_updates(start_time, errors_this_run)
            time.sleep(TIME_BETWEEN_RETRIES)


if __name__ == "__main__":
    main()
