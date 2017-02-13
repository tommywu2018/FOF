# coding=utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pylab import *
import datetime as dt
from WindPy import *
import xlrd
import xlwt
from xlutils.copy import copy
w.start()

temp_data = w.wsd("000300.SH", "pct_chg", "2016-01-02", "2017-01-02")

# 获取日度数据
def Wsd_Data_Install(code, fields, startdate, enddate):
    temp_data = w.wsd(code, fields, startdate, enddate)
    if temp_data.ErrorCode == 0:
        data = pd.DataFrame(np.array(temp_data.Data).T, index=temp_data.Times, columns=temp_data.Fields)
        return data
    else:
        return "ErrodCode=%s" % temp_data.ErrorCode

# 获取日内数据
def Wsi_Data_Install(code, startdate, enddate):
    temp_data = w.wsi(code, "close", startdate, enddate, "BarSize=5")
    if temp_data.ErrorCode == 0:
        data = pd.DataFrame(np.array(temp_data).T, index=temp_data.Times, columns=temp_data.Fields)
    return data

# 计算日内波动率
def Intraday_Volatility(code, startdate, enddate):
    date_set = pd.date_range(startdate, enddate, freq="D")
    data = Wsi_Data_Install(code, startdate, enddate)
    intraday_std_list = list()
    date_list = list()
    for each in range(len(date_set) - 1):
        data_temp = data.loc[date_set[each]:date_set[each+1]]
        if data_temp.empty:
            pass
        else:
            intraday_std = data_temp.pct_change().std()
            intraday_std_list = intraday_std_list.append(intraday_std)
            date_list = date_list.append(each)
    intraday_std_frame = pd.DataFrame(np.array(intraday_std_list), index=date_list, columns=["intraday_std"])
    return intraday_std_frame

test = pd.DataFrame(np.random.randn(100))
test.std()
# 计算资产组合的当日净值
def Protfolio_Net_Value(code_list, weight_list, previous_nv, today_date):
    pct_chg_list = list()
    for each_code in code_list:
        temp_data = w.wsd(each_code, "pct_chg", today_date, today_date)
        if type(temp_data) == str:
            print temp_data
            break
        else:
            pct_chg_list.append(temp_data.Data[0][0])
    if len(pct_chg_list) == len(code_list):
        nv_pct_chg = np.array(pct_chg_list) * np.array(weight_list)
        nv_today = previous_nv * (1 + nv_pct_chg/100)
        return nv_today
    else:
        return "Error"

'''
close:收盘价
amt:交易量
pct_chg:涨跌幅
swing:振幅
free_turn:换手率（以自由流通股本计）
'''
day_shift = 120
week_shift = 52
month_shift = 36

today_date = dt.date.today().isoformat()
print today_date

daily_backtest_start_date = str(w.tdaysoffset(-day_shift, today_date).Data[0][0])[:10]
