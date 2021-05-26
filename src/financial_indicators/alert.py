import requests
from financial_indicators import KD

kd = KD("TAIEX_data")


def pd_to_int(pd):
    return pd[["slowk","slowd"]].fillna(0.0).astype(int)


def ckeck(day_kd,week_kd,month_kd):
    is_alert = False
    message = "大盤\n"
    info_temp = "{} => K:{}, D:{}\n"

    # 1. 當下的值判斷要不要通知
    # 2. D-K
    month_kd = pd_to_int(month_kd)
    week_kd = pd_to_int(week_kd)
    day_kd = pd_to_int(day_kd)

    # latest value
    m_k, m_d = month_kd.iloc[-1]
    w_k, w_d = week_kd.iloc[-1]
    d_k, d_d = day_kd.iloc[-1]

    # 長期
    if m_k <= 40 or m_k >= 80:
        is_alert = True
    # 中期
    if w_k <= 30 or w_k >= 80:
        is_alert = True

    message = message + info_temp.format("month_kd", m_k, m_d)
    message = message + info_temp.format("week_kd", w_k, w_d)
    message = message + info_temp.format("day_kd", d_k, d_d)
    message = message + "近5次月KD差：\n"
    message = message + str((month_kd[-5:]["slowk"]-month_kd[-5:]["slowd"]).tolist()) + "\n"
    message = message + "近5次週KD差：\n"
    message = message + str((week_kd[-5:]["slowk"] - week_kd[-5:]["slowd"]).tolist()) + "\n"

    if is_alert:
        return message