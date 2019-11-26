import datetime
import platform
import time


def get_paths(PATHS):
    if platform.system() == "Windows":
        PATHS = PATHS["Windows"]
    else:
        PATHS = PATHS["Linux"]
    CSV_PATH = PATHS["CSV_PATH"]
    CREDENTIALS_PATH = PATHS["CREDENTIALS_PATH"]
    GRAPH_PATH = PATHS["GRAPH_PATH"]
    BY_DAY_GRAPH_PATH = PATHS["BY_DAY_GRAPH_PATH"]
    return CSV_PATH, CREDENTIALS_PATH, GRAPH_PATH, BY_DAY_GRAPH_PATH


def print_updates(start_time, errors_this_run):
    print("Errors in this run: " + str(errors_this_run))
    print(
        "Running for "
        + str(datetime.timedelta(seconds=(time.time() - start_time)))
        + "\n"
    )
