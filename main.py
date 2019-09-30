import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

LOGIN_URL = 'https://www.puregym.com/login/'
LOGIN_API_URL = 'https://www.puregym.com/api/members/login'
MEMBERS_URL = 'https://www.puregym.com/members/'

def main():
	with requests.Session() as session:
		s = session.get(LOGIN_URL)
		cookies = s.cookies
		soup = BeautifulSoup(s.text, 'html.parser')
		tag = soup.find("input", {'name': '__RequestVerificationToken'})
		token = tag['value']

		payload = {'email' : EMAIL, #replace with email
				 'pin' : PIN #replace with pin
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

	scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_NAME, scope) #replace with generated json name
	client = gspread.authorize(creds)

	sheet = client.open(SHEET_NAME).sheet1 #replace with Google sheet name

	now = datetime.datetime.now()
	date = now.date() #strftime('%Y-%m-%d')
	time = now.strftime('%H:%M:%S')
	weekday = date.isoweekday()
	hour = now.hour
	minute = now.minute
	second = now.second
	sheet.append_row([str(date), weekday, str(time), hour, minute, second, heads])

if __name__ == '__main__':
	main()