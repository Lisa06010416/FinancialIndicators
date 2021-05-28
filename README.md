# Financial Indicators
Download stock data from and calculate some financial indicators(only KD value know) simply.


## STEP 0 install package
````
pip install .
````

## STEP1 get stock data
#### creat empty data dir

- TAIEX_data
  * day
  * month
  * week

#### doenload and process data
````
from financial_indicators import KDDataProcess, read_all_data, StockData


processor = KDDataProcess()
# scrapy data
processor.scrapy_day_data("2019","TAIEX_data/day")
# read all data
all_data = read_all_data("TAIEX_data/day")
# week_data
week_data = processor.process_week_data(all_data)
StockData("TAIEX_data").save_data_by_year(week_data, "week")
# month data
month_data = processor.process_month_data(all_data)
StockData("TAIEX_data").save_data_by_year(month_data, "month")
````

## STEP2 calculate KD value
we can calculate day, week, month KD
```
from financial_indicators import KD

# calculate kd
day_kd = KD("TAIEX_data").get_kd("day")
print(day_kd)
week_kd = KD("TAIEX_data").get_kd("week")
print(week_kd)
month_kd = KD("TAIEX_data").get_kd("month")
print(month_kd)
```

