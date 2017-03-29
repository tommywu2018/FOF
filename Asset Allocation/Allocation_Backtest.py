# -*- coding: utf-8 -*-
"""
@author: Wang Bin
"""

portfolio_name = u"wenjian"

from Allocation_Method import Risk_Parity_Weight, Min_Variance_Weight, Combined_Return_Distribution, Max_Sharpe_Weight, Max_Utility_Weight, Inverse_Minimize
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

History_Data = pd.read_excel("/Users/WangBin-Mac/FOF/Asset Allocation/History_Data.xlsx")
Predict_Data = pd.read_excel("/Users/WangBin-Mac/FOF/Asset Allocation/Predict_Data.xlsx")
asset_list = ["bond", "stock_large", "stock_small",
              "stock_HongKong", "stock_US", "gold"]
bnds = [(0.0, None), (0.0, None), (0.0, None),
        (0.0, None), (0.0, None), (0.0, None)]
#bnds = [(0.1, 0.6), (0.05, 0.2), (0.05, 0.2), (0.05, 0.2), (0.05, 0.2), (0.0, 0.3)]

year_delta = 5
tau = 1.0
if portfolio_name == "wenjian":
    lam = 2.3 #进取-1.9 平衡-2.0 稳健-2.3
    money_weight = 0.75
elif portfolio_name == "pingheng":
    lam = 1.9
    money_weight = 0.85
elif portfolio_name == "jinqu":
    lam = 1.7
    money_weight = 0.95
else:
    raise Exception("Wrong portfolio_name!")

pct_list = []
weight_list = []
date_list = []
for each_date in Predict_Data.index[60:-1]:
    last_date = History_Data.index[list(Predict_Data.index).index(each_date)-1]  # 当前月份日期
    next_date = each_date  # 下一月份日期
    if last_date.month <= 11:
        start_year = last_date.year - year_delta
        start_month = last_date.month + 1
    else:
        start_year = last_date.year - year_delta + 1
        start_month = 1

    # 基础设定
    history_data = History_Data[asset_list][
        str(start_year) + '-' + str(start_month): last_date]
    predict_data = Predict_Data[asset_list][
        str(start_year) + '-' + str(start_month): last_date]
    cov_mat = history_data[asset_list].cov() * 12.0
    # print cov_mat
    omega = np.matrix(cov_mat.values)
    mkt_wgt = Risk_Parity_Weight(cov_mat)
    #print mkt_wgt

    P = np.diag([1] * len(mkt_wgt))

    conf_list = list()
    for each in asset_list:
        conf_temp = ((history_data[each][str(start_year) + '-' + str(start_month):] -
                      predict_data[each][str(start_year) + '-' + str(start_month):])**2).mean() * 12.0
        conf_list.append(conf_temp)
    conf_mat = np.matrix(np.diag(conf_list))

    Q = np.matrix(Predict_Data[asset_list].loc[next_date])

    com_ret, com_cov_mat = Combined_Return_Distribution(
        2, cov_mat, tau, mkt_wgt, P, Q, conf_mat)

    #print com_ret

    weight_bl = Max_Utility_Weight(com_ret, com_cov_mat, lam, bnds)

    print sum(weight_bl*History_Data[asset_list].loc[next_date])*money_weight + money_weight*History_Data["money"].loc[next_date]
    pct_list.append(sum(weight_bl*History_Data[asset_list].loc[next_date])*money_weight + money_weight*History_Data["money"].loc[next_date])
    weight_list.append(list(weight_bl))
    date_list.append(next_date)

pd.Series(np.array(pct_list), index=date_list).to_csv("/Users/WangBin-Mac/FOF/Asset Allocation/backtest_wenjian.csv")
pd.DataFrame(np.array(weight_list), index=date_list, columns=asset_list).to_excel("/Users/WangBin-Mac/FOF/Asset Allocation/backtest_wj_weight.xlsx")

print (np.array(pct_list)+1).cumprod()[-1]

def Performance(return_series, rf_ret):
    end_value = (return_series + 1).prod()
    annual_return = (return_series + 1).prod() ** (1/(len(return_series)/12.0)) - 1
    annual_variance = (return_series.var() * 12.0) ** 0.5
    sharpe_ratio = (annual_return - rf_ret)/annual_variance
    max_drawdown = max(((return_series + 1).cumprod().cummax()-(return_series + 1).cumprod())/(return_series + 1).cumprod().cummax())
    (return_series + 1).cumprod().plot()
    return [end_value, annual_return, annual_variance, sharpe_ratio, max_drawdown]


return_series = pd.read_csv("/Users/WangBin-Mac/FOF/Asset Allocation/backtest_wenjian.csv", header=None)[1]
print Performance(return_series, 0.025)

'''
file_name_list = ['wenjian', 'pingheng', 'jinqu', 'wenjian_f', 'pingheng_f', 'jinqu_f']
result_list = list()
for each_file in file_name_list:
    return_series = pd.read_csv("/Users/WangBin-Mac/FOF/Asset Allocation/backtest_"+each_file+".csv", header=None)[1]
    return_series = [1] + list(return_series.values)
    return_series = pd.Series(return_series).pct_change().dropna()
    temp_result = Performance(return_series, 0.025)
    result_list.append(temp_result)

pd.DataFrame(np.array(result_list).T, index=['end_value', 'annual_return', 'annual_variance', 'sharpe_ratio', 'max_drawdown'], columns=['wenjian', 'pingheng', 'jinqu', 'wenjian_f', 'pingheng_f', 'jinqu_f']).to_excel("/Users/WangBin-Mac/FOF/Asset Allocation/backtest_results.xlsx")
'''
