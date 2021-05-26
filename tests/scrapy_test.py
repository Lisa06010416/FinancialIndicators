from financial_indicators import KDDataProcess, read_all_data, StockData


processor = KDDataProcess()
# scrapy data
# processor.scrapy_day_data("2019","TAIEX_data/day")
# read all data
all_data = read_all_data("TAIEX_data/day")
# week_data
week_data = processor.process_week_data(all_data)
StockData("TAIEX_data").save_data_by_year(week_data, "week")
# month data
month_data = processor.process_month_data(all_data)
StockData("TAIEX_data").save_data_by_year(month_data, "month")