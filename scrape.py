import datetime
import json
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

from configs import CSV_PATH, CREDENTIALS_PATH, LOGIN_URL, LOGIN_API_URL, MEMBERS_URL, TIME_BETWEEN_SCRAPES, \
    TIME_BETWEEN_RETRIES


def read_n_people(people_counts, credentials):
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
    people_counts = pd.concat([people_counts, this_count])

    people_counts.to_csv(CSV_PATH, header=False)

    print(people_counts)
    print("")

    return people_counts


def main():
    with open(CREDENTIALS_PATH, "r") as read_file:
        credentials = json.load(read_file)

    people_counts = pd.Series()

    while True:
        try:
            people_counts = read_n_people(people_counts, credentials)
            time.sleep(TIME_BETWEEN_SCRAPES)
        except Exception as e:
            print(e)
            print("")
            time.sleep(TIME_BETWEEN_RETRIES)


if __name__ == '__main__':
    main()
