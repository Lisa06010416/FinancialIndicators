import os
import requests

from financial_indicators import KD
from financial_indicators import ckeck


kd = KD("TAIEX_data")
kd.update_data_daily()


def daily_alert():
    day_kd = kd.get_kd("day")
    week_kd = kd.get_kd("week")
    month_kd = kd.get_kd("month")
    message = ckeck(day_kd,week_kd,month_kd)
    if message:
        url = os.environ["secrets.README_AUTHORIZATION"]
        requests.post(url,
                     params={'message': message},
                     headers={'Authorization': 'Bearer ' + os.environ["secrets.README_AUTHORIZATION"]})

daily_alert()
