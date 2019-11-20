import datetime
import json
import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

from configs import PATHS, LOGIN_URL, LOGIN_API_URL, MEMBERS_URL, TIME_BETWEEN_SCRAPES, \
    TIME_BETWEEN_RETRIES
from utils import get_paths, print_updates

CSV_PATH, CREDENTIALS_PATH, GRAPH_PATH, BY_DAY_GRAPH_PATH = get_paths(PATHS)


def read_n_people(people_counts, credentials, file_path):
    with requests.Session() as session:
        s = session.get(LOGIN_URL)
        soup = BeautifulSoup(s.text, 'html.parser')
        tag = soup.find("input", {'name': '__RequestVerificationToken'})
        token = tag['value']

        payload = {'email': credentials['email'],  # replace with email
                   'pin': credentials['pin']}  # replace with pin

        headers = {'__RequestVerificationToken': token}

        session.post(LOGIN_API_URL, headers=headers, data=payload)
        response = session.get(MEMBERS_URL)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the member count on the page
    count = soup.find('span', 'heading heading--level3 secondary-color margin-none')

    members = count.text.split()

    if members[0] == 'Fewer':
        # Fewer than 20 people
        heads = 20
    else:
        heads = int(members[0])

    now = datetime.datetime.now()

    this_count = pd.Series(heads, index=[now])
    print(this_count)
    print("")

    people_counts = pd.concat([people_counts, this_count])

    people_counts.to_csv(file_path, header=False)

    return people_counts


def main():
    with open(CREDENTIALS_PATH, "r") as read_file:
        credentials = json.load(read_file)

    people_counts = pd.Series()

    file_path = os.path.join(CSV_PATH,
                             datetime.datetime.now().strftime("gym_people_counts_run_starting_%Y_%m_%d__%H_%M.csv"))

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


if __name__ == '__main__':
    main()
