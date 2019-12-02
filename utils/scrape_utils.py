import datetime
import platform
import time


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
