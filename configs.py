PATHS = {
    "Windows": {
        "CSV_PATH": r"C:\dev\data\puregym_n_people",
        "GRAPH_PATH": r"C:\dev\data\puregym_n_people\gym_people_counts_graph.png",
        "CREDENTIALS_PATH": r"C:\dev\data\puregym_n_people\puregym_credentials.json",
        "BY_DAY_GRAPH_PATH": r"C:\dev\data\puregym_n_people\gym_people_counts_graph_by_day.png",
        "BY_DAY_AVERAGE_GRAPH_PATH": r"C:\dev\data\puregym_n_people\gym_people_counts_graph_by_day_average.png",
    },
    "Linux": {
        "CSV_PATH": r"/home/pi/Desktop/puregym",
        "GRAPH_PATH": r"/home/pi/Desktop/puregym/gym_people_counts_graph.png",
        "CREDENTIALS_PATH": r"/home/pi/Desktop/puregym/puregym_credentials.json",
        "BY_DAY_GRAPH_PATH": r"/home/pi/Desktop/puregym/gym_people_counts_graph_by_day.png",
        "BY_DAY_AVERAGE_GRAPH_PATH": r"/home/pi/Desktop/puregym/gym_people_counts_graph_by_day_average.png",
    },
}

LOGIN_URL = "https://www.puregym.com/login/"
LOGIN_API_URL = "https://www.puregym.com/api/members/login"
MEMBERS_URL = "https://www.puregym.com/members/"

# In seconds
TIME_BETWEEN_SCRAPES = 270
TIME_BETWEEN_RETRIES = 1
