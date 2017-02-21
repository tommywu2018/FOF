# coding=utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pylab import *
import datetime as dt
from WindPy import *
import xlrd
from xlwt import Workbook, easyxf
from xlutils.copy import copy
w.start()

def Portfolio_Net_Value(code_list, weight_list, previous_nv, today_date):
    pct_chg_list = list()
    yesterday_date = str(w.tdaysoffset(-1, today_date).Data[0][0])[:10]
    for each_code in code_list:
        temp_data = w.wsd(each_code, "NAV_adj", yesterday_date, today_date)
        if temp_data.ErrorCode != 0:
            print temp_data.ErrorCode
            raise Exception("error in data install!")
        else:
            pct_chg = (temp_data.Data[0][1] - temp_data.Data[0][0])/temp_data.Data[0][0]
            pct_chg_list.append(pct_chg)
    if len(pct_chg_list) == len(code_list):
        pct_chg_list = pct_chg_list + [0.0] * (len(weight_list) - len(code_list))
        nv_pct_chg = sum(np.array(pct_chg_list) * np.array(weight_list))
        nv_today = previous_nv * (1 + nv_pct_chg)
        return nv_today
    else:
        raise Exception("missing data!")

code_list_wenjian = ["180031.OF", "513500.OF", "513100.OF", "159920.OF", "513660.OF",
"159926.OF", "003358.OF", "001512.OF", "511010.OF", "161821.OF", "000022.OF",
"518880.OF", "159934.OF", "003022.OF", "000434.OF"]

weight_list_wenjian = [4.47, 3.78, 3.78, 4.33, 4.33, 5.00, 5.00, 5.00, 6.25, 5.00, 5.00,
3.72, 3.72, 10.00, 10.00]

code_list_pingheng = ["180031.OF", "040035.OF", "513500.OF", "513100.OF", "159920.OF", "513660.OF",
"511220.OF", "003358.OF", "159926.OF", "511010.OF",
"518880.OF", "159934.OF", "003022.OF", "000434.OF"]

weight_list_pingheng = [3.78, 3.78, 4.79, 4.79, 7.27, 7.27, 1.00, 5.75, 5.75, 5.75, 5.90, 5.90, 8.00, 8.00]

code_list_jinqu = ["180031.OF", "040035.OF", "000471.OF", "513500.OF", "096001.OF", "513100.OF", "159920.OF", "513660.OF",
"511220.OF", "003358.OF", "511010.OF",
"518880.OF", "159934.OF", "159937.OF", "518800.OF", "003022.OF", "000434.OF"]

weight_list_jinqu = [3.70, 3.70, 3.70, 3.95, 3.95, 3.95, 10.64, 10.64, 1.00, 5.51, 5.51, 4.20, 4.20, 4.20, 4.20, 6.50, 6.50]


code_list = code_list_jinqu
weight_list = weight_list_jinqu
len(code_list) == len(weight_list)
weight_list = np.array(weight_list)/100
tdays_list = w.tdays("2017-02-01", "2017-02-19")

nv_series = pd.Series(index=tdays_list.Times)

for each_date in nv_series.index:
    nv_series[each_date] = Portfolio_Net_Value(code_list, weight_list, 1, each_date)
print "OK!"

(nv_series.prod() ** (21/11)) ** 12
(1.0125123 ** (21/11)) ** 12
