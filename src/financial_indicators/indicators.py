import pandas as pd
from talib import abstract
import os

from .utils import get_time, get_pre_month, get_pre_year
from .scrapy import crawl_TAIEX


class KDDataProcess():
    @staticmethod
    def scrapy_day_data(start_y, save_path):
        end_year, end_month, _ = get_time()
        for y in range(int(start_y), int(end_year)+1):
            for m in range(1,13):
                if y==end_year and m>end_month:
                    break
                crawl_TAIEX(str(y),str(m)).to_csv(os.path.join(save_path,"{}_{}.csv".format(y,m)))

    @staticmethod
    def process_week_data(stock_pd):
        week_stock_data = []
        stock_pd['date'] = stock_pd['date'].apply(pd.to_datetime)
        stock_pd['week'] = stock_pd['date'].diff().dt.days.ne(1).cumsum()
        stock_pd['date'] = stock_pd['date'].apply(lambda x: "{}-{}-{}".format(x.year, x.month, x.day))
        for g, d in stock_pd.groupby("week"):
            start_date = d.iloc[0]['date']
            close_date = d.iloc[-1]['date']
            open = d.iloc[0]['open']
            close = d.iloc[-1]['close']
            high = d["high"].max()
            low = d["low"].min()
            week_stock_data.append([start_date, close_date, open, high, low, close])
        return pd.DataFrame(week_stock_data, columns=["start_date", "close_date", "open", "high", "low", "close"])

    @staticmethod
    def process_month_data(stock_pd):
        def get_year_month(x):
            x = str(x)
            return x.split("-")[0]+"_"+x.split("-")[1]
        month_stock_data = []
        stock_pd["year_month"] = stock_pd["date"].apply(get_year_month)
        stock_pd['date'] =stock_pd['date'].apply(lambda x: "{}-{}-{}".format(x.year, x.month, x.day))
        for g, d in stock_pd.groupby("year_month"):
            month_stock_data.append([
                                        d.iloc[0]['date'],
                                        d.iloc[-1]['date'],
                                        d.iloc[0]['open'],
                                        d["high"].max(),
                                        d["low"].min(),
                                        d.iloc[-1]['close'],
                                    ])
        return pd.DataFrame(month_stock_data, columns=["start_date", "close_date", "open", "high", "low", "close"])


class StockData:
    def __init__(self, data_path):
        self.data_path = data_path

    def get_data_path(self, time_region, year, month=None):
        if time_region == "day":
            data_path = os.path.join(self.data_path, time_region + "/" + year + "_" + month + ".csv")
        else:
            data_path = os.path.join(self.data_path, time_region + "/" + year + ".csv")
        return data_path

    def get_pre_date(self, time_region,year, month):
        if time_region == "day":
            year, month = get_pre_month(year, month)
        else:
            year = get_pre_year(year)
        month = month if len(month) == 2 else "0" + month
        return year, month

    def get_data(self, time_region, only_this_period=False):
        y, m, d = get_time()
        data_path = self.get_data_path(time_region, y, m)
        data = pd.read_csv(data_path, index_col=0)
        while not only_this_period and len(data) < 30:
            y, m = self.get_pre_date(time_region, y, m)
            pre_data_path = self.get_data_path(time_region, y, m)
            pre_data = pd.read_csv(pre_data_path, index_col=0)
            data = pd.concat([pre_data, data])
        return data

    def save_data_by_year(self, stock_pd, time_region):
        def get_year(x):
            x = str(x)
            return x.split("-")[0]
        stock_pd["year"] = stock_pd["start_date"].apply(get_year)
        for g,d in stock_pd.groupby("year"):
            year = d.iloc[0]["year"]
            del d['year']
            d.reset_index(drop=True).to_csv(self.get_data_path(time_region,year))


class KD(StockData):
    def __init__(self, data_path):
        super().__init__(data_path)

    def get_kd(self, time_region):
        data = self.get_data(time_region)
        data = data[["open", "high", "low", "close"]]
        return abstract.STOCH(data, fastk_period=9, slowk_period=5,slowd_period=5,slowk_matype=1,slowd_matype=1)

    def update_data_daily(self):
        y, m, d = get_time()
        # 爬本月最新的資料
        stock_pd = crawl_TAIEX(y,m)
        # 存起來
        stock_pd.to_csv(self.get_data_path("day",y,m))

        # month_data
        latest_month_data = KDDataProcess.process_month_data(stock_pd).iloc[-1]
        try:
            old_month_data = self.get_data('month',only_this_period=True)
        except:
            old_month_data = pd.DataFrame()
            print("A new year .. creat a new month data csv.")

        if not old_month_data.empty and latest_month_data["start_date"] == old_month_data.iloc[-1]["start_date"]:
            old_month_data.iloc[-1] = latest_month_data
        else:
            old_month_data = old_month_data.append(latest_month_data)
        old_month_data.reset_index(drop=True).to_csv(self.get_data_path("month", y))

        # week data
        stock_pd = self.get_data('day')
        latest_week_data = KDDataProcess.process_week_data(stock_pd).iloc[-1]
        try:
            old_week_data = self.get_data('week',only_this_period=True)
        except:
            old_week_data = pd.DataFrame()
            print("A new year .. creat a new week data csv.")
        if not old_week_data.empty and latest_week_data["start_date"] == old_week_data.iloc[-1]["start_date"]:
            old_week_data.iloc[-1] = latest_week_data
        else:
            old_week_data = old_week_data.append(latest_week_data)
        old_week_data.reset_index(drop=True).to_csv(self.get_data_path("week", y))