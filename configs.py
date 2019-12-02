PATHS = {
    "Windows": {
        "DATA_PATH": r"C:\dev\data\puregym_n_people",
    },
    "Linux": {
        "DATA_PATH": r"/home/pi/Desktop/puregym/",
    },
}

LOGIN_URL = "https://www.puregym.com/login/"
LOGIN_API_URL = "https://www.puregym.com/api/members/login"
MEMBERS_URL = "https://www.puregym.com/members/"

# In seconds
TIME_BETWEEN_SCRAPES = 270
TIME_BETWEEN_RETRIES = 1


DAYS_OF_WEEK = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
