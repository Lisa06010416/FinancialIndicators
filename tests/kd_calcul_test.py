from financial_indicators import KD

kd = KD("TAIEX_data")
# calculate kd
day_kd = kd.get_kd("day")
print(day_kd)
week_kd = kd.get_kd("week")
print(week_kd)
month_kd = kd.get_kd("month")
print(month_kd)
