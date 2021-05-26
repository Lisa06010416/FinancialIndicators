import requests
import pandas as pd

from .utils import check_string, convert_to_float



def crawl_TAIEX(year: str, month: str):
    if len(month) == 1:
        month = "0"+month
    assert len(year)==4
    assert len(month) == 2
    data_url = "https://www.twse.com.tw/indicesReport/MI_5MINS_HIST?response=csv&date={y}{m}01".format(y=year, m=month)
    data = requests.get(data_url).text
    stock_data = []
    for line in data.split('\r\n'):
        if check_string("[0-9]+/[0-9]+/[0-9]+", line):
            per_column_data = line.split('","')
            date = per_column_data[0].replace('"', "")
            column_value = [convert_to_float(i) for i in per_column_data[1:]]
            date = date.split("/")
            date[0] = str(int(date[0])+1911)
            column_value = ["/".join(date)] + date + column_value
            stock_data.append(column_value)
    stock_pd = pd.DataFrame(stock_data, columns=["date", "year", "month", "day", "open", "high", "low", "close"])
    stock_pd['date'] = stock_pd['date'].apply(pd.to_datetime)
    stock_pd['week'] = stock_pd['date'].diff().dt.days.ne(1).cumsum()
    return stock_pd