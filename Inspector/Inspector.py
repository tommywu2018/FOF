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
        data = pd.DataFrame(np.array(temp_data.Data).T, index=temp_data.Times, columns=temp_data.Fields)
    return data

# 计算日内波动率
def Intraday_Volatility(code, startdate, enddate):
    enddate = dt.datetime.strptime(enddate, "%Y-%m-%d") + timedelta(1)
    enddate = enddate.strftime("%Y-%m-%d")
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
            intraday_std_list.append(intraday_std)
            date_list.append(date_set[each])
    intraday_std_frame = pd.DataFrame(np.array(intraday_std_list), index=date_list, columns=["intraday_std"])
    return intraday_std_frame

test = pd.DataFrame(np.random.randn(100))
test.std()
# 计算资产组合的当日净值
# code_list只包含公募类产品，weight_list包含所有产品（含私募类产品），私募类产品的权重应在weight_list的最后
def Portfolio_Net_Value(code_list, weight_list, previous_nv, today_date):
    pct_chg_list = list()
    yesterday_date = str(w.tdaysoffset(-1, today_date).Data[0][0])[:10]
    for each_code in code_list:
        temp_data = w.wsd(each_code, "NAV_adj", yesterday_date, today_date)
        if temp_data.ErrorCode != 0:
            print temp_data.ErrorCode
            break
        else:
            pct_chg = (temp_data.Data[0][1] - temp_data.Data[0][0])/temp_data.Data[0][0]
            pct_chg_list.append(temp_data.Data[0][0])
    if len(pct_chg_list) == len(code_list):
        pct_chg_list = pct_chg_list + [0.0] * (len(weight_list) - len(code_list))
        nv_pct_chg = np.array(pct_chg_list) * np.array(weight_list)
        nv_today = previous_nv * (1 + nv_pct_chg)
        return nv_today
    else:
        return "Error"

def Index_Performance(code, startdate, enddate):
    wsd_data = Wsd_Data_Install(code, ["pct_chg", "swing", "amt", "free_turn"], startdate, enddate)
    today_data = list(wsd_data.iloc[-1])
    upper_quantile = list(wsd_data.iloc[:-1].quantile(0.9))
    lower_quantile = list(wsd_data.iloc[:-1].quantile(0.1))
    intraday_std_data = Intraday_Volatility(code, startdate, enddate)
    today_data.append(intraday_std_data.iloc[-1,0])
    upper_quantile.append(intraday_std_data.iloc[0:-1,0].quantile(0.9))
    lower_quantile.append(intraday_std_data.iloc[0:-1,0].quantile(0.1))
    data = pd.DataFrame(np.array([today_data, upper_quantile, lower_quantile]), index=[u"今日值", u"上10%分位数", u"下10%分位数"], columns=[u"涨跌幅", u"振幅", u"成交额", u"换手率", u"日内波动率"])
    return data

def Subfund_Performance(code, startdate, enddate):
    startdate = str(w.tdaysoffset(-1, startdate).Data[0][0])[:10]
    wsd_data = Wsd_Data_Install(code, "NAV_adj", startdate, enddate).pct_change()
    today_data = wsd_data.iloc[-1,0]
    upper_quantile = wsd_data.iloc[:-1,0].quantile(0.9)
    lower_quantile = wsd_data.iloc[:-1,0].quantile(0.1)
    data = pd.DataFrame(np.array([today_data, upper_quantile, lower_quantile]), index=[u"今日值", u"上10%分位数", u"下10%分位数"], columns=[u"净值涨跌幅"])
    return data


Index_Performance("000300.SH", "2016-11-11", "2017-02-10")
code = "000300.SH"
startdate = "2016-11-11"
enddate = "2017-02-10"
wsd_data = w.wsd(code, ["pct_chg", "swing", "amt", "free_turn"], startdate, enddate)
print wsd_data
wsd_data.iloc[:-1,0].quantile(0.1)
'''
close:收盘价
amt:交易量
pct_chg:涨跌幅
swing:振幅
free_turn:换手率（以自由流通股本计）
NAV_adj:
NAV_acc:

'''
day_shift = 120
week_shift = 52
month_shift = 36

today_date = dt.date.today().isoformat()
#print today_date

daily_backtest_start_date = str(w.tdaysoffset(-day_shift, today_date).Data[0][0])[:10]
#print daily_backtest_start_date

pd.Series(np.random.randn(8)).quantile(0.5)
