import datetime
import pygsheets
import pandas as pd

gc = pygsheets.authorize(service_file='key.json')

total_time_taken = []


class DataCollection:
    def __init__(self):
        self.hit_list = []
        self.hit_count_list = []
        self.time_start_list = []
        self.time_end_list = []
        self.time_taken_list = []

    def run_once_hit(self, f):
        def wrapper(*args, **kwargs):
            if not wrapper.has_run:
                wrapper.has_run = True
                return f(*args, **kwargs)

        wrapper.has_run = False
        return wrapper

    def run_once_time(self, f):
        def wrapper(*args, **kwargs):
            if not wrapper.has_run:
                wrapper.has_run = True
                return f(*args, **kwargs)

        wrapper.has_run = False
        return wrapper

    def hit_count(self):
        self.hit_list.append("true")
        self.hit_count_list.append(len(self.hit_list))
        time_hit = datetime.datetime.now()
        self.time_start_list.append(time_hit)
        print(len(self.hit_list))

    def time_count(self):
        time_hit = datetime.datetime.now()
        self.time_end_list.append(time_hit)
        print("Not hit")


def calculate_time(time_start, time_end):
    time_taken = time_end - time_start
    global total_time_taken
    total_time_taken.append(time_taken)


def create_data(sheet_index, placement, time_end_list, time_start_list, time_taken_list, hit_count_list):
    print("Creating data frames at column", placement)

    if len(time_end_list) >= 2:
        time_end_list.pop(0)

    for i in range(len(time_end_list)):
        try:
            time_taken = time_end_list[i] - time_start_list[i]
            time_taken_list.append(time_taken.seconds)
        except IndexError:
            time_taken_list.append("Error")
            continue

    total_hit_count = hit_count_list[-1:]  # Get last index from list
    global total_time_taken

    df_hit_count = pd.DataFrame(hit_count_list, columns=['Distance violations'])
    df_time_start = pd.DataFrame(time_start_list, columns=['Time start'])
    df_time_end = pd.DataFrame(time_end_list, columns=['Time end'])
    df_time_taken = pd.DataFrame(time_taken_list, columns=['Time taken (sec)'])
    df_total_hit_count = pd.DataFrame(total_hit_count, columns=['Total violations'])
    df_total_time_taken = pd.DataFrame(total_time_taken, columns=['Total time'])

    spreadsheet = gc.open('Test Data')

    work_sheet = spreadsheet[sheet_index]
    work_sheet.set_dataframe(df_hit_count, (1, 1 + placement))
    work_sheet.set_dataframe(df_time_start, (1, 2 + placement))
    work_sheet.set_dataframe(df_time_end, (1, 3 + placement))
    work_sheet.set_dataframe(df_time_taken, (1, 4 + placement))
    work_sheet.set_dataframe(df_total_hit_count, (1, 5 + placement))
    work_sheet.set_dataframe(df_total_time_taken, (1, 6 + placement))
    print("Added to sheets")
