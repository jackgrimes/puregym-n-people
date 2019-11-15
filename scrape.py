import datetime
import json
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

from configs import CSV_PATH, CREDENTIALS_PATH

with open(CREDENTIALS_PATH, "r") as read_file:
	credentials = json.load(read_file)


LOGIN_URL = 'https://www.puregym.com/login/'
LOGIN_API_URL = 'https://www.puregym.com/api/members/login'
MEMBERS_URL = 'https://www.puregym.com/members/'


def read_n_people(people_counts):
	with requests.Session() as session:
		s = session.get(LOGIN_URL)
		cookies = s.cookies
		soup = BeautifulSoup(s.text, 'html.parser')
		tag = soup.find("input", {'name': '__RequestVerificationToken'})
		token = tag['value']

		payload = {'email' : credentials['email'], #replace with email
				 'pin' : credentials['pin'] #replace with pin
				 }

		headers = {'__RequestVerificationToken' : token
				  }

		post = session.post(LOGIN_API_URL, headers = headers, data = payload)

		response = session.get(MEMBERS_URL)

	soup = BeautifulSoup(response.text, 'html.parser')
	#Find the member count on the page
	count = soup.find('span', 'heading heading--level3 secondary-color margin-none')

	members = count.text.split()

	if (members[0] == 'Fewer'):
		#Fewer than 20 people
		heads = 20

	else:
		heads = int(members[0])

	#scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
	#creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_NAME, scope) #replace with generated json name
	#client = gspread.authorize(creds)

	#sheet = client.open(SHEET_NAME).sheet1 #replace with Google sheet name

	now = datetime.datetime.now()
	date = now.date() #strftime('%Y-%m-%d')
	current_time = now.strftime('%H:%M:%S')
	weekday = date.isoweekday()
	hour = now.hour
	minute = now.minute
	second = now.second
	#sheet.append_row([str(date), weekday, str(time), hour, minute, second, heads])

	print("The time is " + current_time)
	print("There are " + str(heads) + " people in the gym")
	print("")

	this_count = pd.Series(heads, index=[now])
	people_counts = pd.concat([people_counts, this_count])

	people_counts.to_csv(CSV_PATH, header=False)

	print(people_counts)

	#plt.plot(people_counts)
	#plt.show()

	return people_counts

def main(people_counts):
	while True:
		try:
			people_counts = read_n_people(people_counts)
			# time.sleep(270)
			time.sleep(270)
		except Exception as e:
			print(e)
			print("")
			time.sleep(1)

people_counts = pd.Series()

if __name__ == '__main__':
	main(people_counts)