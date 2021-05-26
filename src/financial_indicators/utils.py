import re
import os
import time

import pandas as pd


def check_string(re_exp, str):
    res = re.search(re_exp, str)
    if res:
        return True
    else:
        return False


def convert_to_float(str):
    str = str.replace(",", "")
    str = str.replace('"', "")
    return float(str)


def read_all_data(dir_path):
    from os import listdir
    from os.path import isfile, join
    files = [os.path.join(dir_path,f) for f in listdir(dir_path) if isfile(join(dir_path, f))]
    files.sort()
    print(files)
    all_data = pd.DataFrame()
    for f in files:
        data = pd.read_csv(f, index_col=0)
        all_data = pd.concat([all_data,data])
    return all_data.reset_index()


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split("-")


def get_pre_month(year,month):
    if int(month)-1 == 0:
        year = str(int(year)-1)
        month = "12"
    else:
        month = str(int(month) - 1)
    return year, month


def get_pre_year(year):
    return str(int(year) - 1)


