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


def Portfolio_Return(codelist, weightlist, startdate, enddate):
    pct_chg_list = list()
    temp_data = w.wsd(codelist, "NAV_adj", startdate, enddate)
    if temp_data.ErrorCode != 0:
        print temp_data.ErrorCode
        raise Exception("error in data install!")
    else:
        for i in range(len(temp_data.Data)):
            pct_chg = (temp_data.Data[i][-1] - temp_data.Data[i][0])/temp_data.Data[i][0]
            pct_chg_list.append(pct_chg)
    if len(pct_chg_list) == len(codelist):
        pct_chg_list = pct_chg_list + [0.0] * (len(weightlist) - len(codelist))
        nv_pct_chg = sum(np.array(pct_chg_list) * np.array(weightlist))
        contri_list = list()
        for j in range(len(codelist)):
            contri = (pct_chg_list[j] * weightlist[j])/nv_pct_chg
            contri_list.append(contri)
        contri_series = pd.Series(contri_list, index=codelist)
        return nv_pct_chg, contri_series
    else:
        raise Exception("missing data!")

def Portfolio_Index_Return(codelist, weightlist, startdate, enddate):
    pct_chg_list = list()
    temp_data = w.wsd(codelist, "close", startdate, enddate)
    if temp_data.ErrorCode != 0:
        print temp_data.ErrorCode
        raise Exception("error in data install!")
    else:
        for i in range(len(temp_data.Data)):
            pct_chg = (temp_data.Data[i][-1] - temp_data.Data[i][0])/temp_data.Data[i][0]
            pct_chg_list.append(pct_chg)
    if len(pct_chg_list) == len(codelist):
        nv_pct_chg = sum(np.array(pct_chg_list) * np.array(weightlist))
        contri_list = list()
        for j in range(len(codelist)):
            contri = (pct_chg_list[j] * weightlist[j])/nv_pct_chg
            contri_list.append(contri)
        contri_series = pd.Series(contri_list, index=codelist)
        return nv_pct_chg, contri_series
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

index_code_list = ["000300.SH", "000905.SH", "SPX.GI", "HSI.HI", "H11001.CSI", "AU9999.SGE", "H11025.CSI"]

index_weight_wenjian = [0.00, 4.47, 7.56, 8.66, 46.88, 7.43, 25.00]
index_weight_pingheng = [0.00, 7.56, 9.58, 14.55, 36.50, 11.81, 20.00]
index_weight_jinqu = [0.00, 11.09, 11.83, 21.27, 24.02, 16.80, 15.00]

start_date = "2017-02-01"
end_date = "2017-02-28"

Portfolio_Index_Return(index_code_list, (np.array(index_weight_jinqu)/100.0), start_date, end_date)

Portfolio_Return(code_list_jinqu, (np.array(weight_list_jinqu)/100.0), start_date, end_date)
