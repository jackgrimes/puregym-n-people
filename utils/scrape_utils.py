import datetime
import json
import platform
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

from configs import (
    LOGIN_URL,
    LOGIN_API_URL,
    MEMBERS_URL,
    ACTIVITY_URL,
)


def get_paths(paths):
    if platform.system() == "Windows":
        paths_this_os = paths["Windows"]
    else:
        paths_this_os = paths["Linux"]
    data_path = paths_this_os["DATA_PATH"]
    return data_path


def print_updates(start_time, errors_this_run):
    print("Time is: " + datetime.datetime.now().strftime("%H:%M:%S"))
    print("Errors in this run: " + str(errors_this_run))
    print(
        "Running for "
        + str(datetime.timedelta(seconds=(time.time() - start_time)))
        + "\n"
    )


def read_n_people(people_counts, credentials, file_path):
    with requests.Session() as session:
        s = session.get(LOGIN_URL)
        soup = BeautifulSoup(s.text, "html.parser")
        tag = soup.find("input", {"name": "__RequestVerificationToken"})
        token = tag["value"]

        payload = {
            "email": credentials["email"],  # replace with email
            "pin": credentials["pin"],
        }  # replace with pin

        headers = {"__RequestVerificationToken": token}

        session.post(LOGIN_API_URL, headers=headers, data=payload)
        response = session.get(MEMBERS_URL)

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the member count on the page
    count = soup.find("span", "heading heading--level3 secondary-color margin-bottom")

    members = count.text.split()

    if members[0] == "Fewer":
        # Fewer than 20 people
        heads = 20
    else:
        heads = int(members[0])

    now = datetime.datetime.now()

    this_count = pd.Series(heads, index=[now])
    print("Count is: " + str(list(this_count)[0]))

    people_counts = pd.concat([people_counts, this_count])
    people_counts.to_csv(file_path, header=False)

    return people_counts


def read_my_durations(credentials):
    with requests.Session() as session:
        s = session.get(LOGIN_URL)
        soup = BeautifulSoup(s.text, "html.parser")
        tag = soup.find("input", {"name": "__RequestVerificationToken"})
        token = tag["value"]

        payload = {
            "email": credentials["email"],  # replace with email
            "pin": credentials["pin"],
        }  # replace with pin

        headers = {"__RequestVerificationToken": token}

        session.post(LOGIN_API_URL, headers=headers, data=payload)
        response = session.get(ACTIVITY_URL)

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the durations on the page
    durations = (
        str(soup)
        .split(
            '<a class="tabs-mobile__link" href="/members/member-benefits/">Benefits</a>'
        )[1]
        .split("var jsonData = ")[1]
        .split(";")[0]
    )

    durations = json.loads(durations)
    durations = pd.DataFrame(durations)
    durations.rename(columns={"count": "duration"}, inplace=True)

    durations["date"] = pd.to_datetime(durations["date"], format="%Y-%m-%d")
    return durations


def process_new_durations(scraped_durations, durations):
    new_durations = scraped_durations[scraped_durations["date"] >= max(durations["date"])].copy()

    new_durations["concat"] = new_durations.loc[:, "date"].dt.strftime(
        "%Y_%m_%d__"
    ) + (new_durations.loc[:, "duration"].astype(str))

    durations["concat"] = durations.loc[:, "date"].dt.strftime("%Y_%m_%d__") + (
        durations.loc[:, "duration"].astype(str)
    )

    new_durations = new_durations[~new_durations["concat"].isin(durations["concat"])]
    new_durations = new_durations[["date", "duration"]]
    new_durations = new_durations.sort_values("date", ascending=True)
    return new_durations
