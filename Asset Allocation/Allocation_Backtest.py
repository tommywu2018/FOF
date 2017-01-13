# -*- coding: utf-8 -*-
"""
@author: Wang Bin
"""

from Allocation_Method import Risk_Parity_Weight, Min_Variance_Weight, Combined_Return_Distribution, Max_Sharpe_Weight, Max_Utility_Weight, Inverse_Minimize
import pandas as pd
import numpy as np

def Performance(file_path, rf_ret):
    data = pd.read_excel(file_path)
    return_series = data['return']
    weight_mean = data[['H11001.CSI', '000300.SH', 'AU9999.SGE']].mean()
    end_value = (return_series + 1).prod()
    annual_return = (return_series + 1).prod() ** (1/(len(data)/12.0)) - 1
    annual_variance = (return_series.var() * 12.0) ** 0.5
    sharpe_ratio = (annual_return - rf_ret)/annual_variance
    max_drawdown = max(((return_series + 1).cumprod().cummax()-(return_series + 1).cumprod())/(return_series + 1).cumprod().cummax())
    (return_series + 1).cumprod().plot()
    return [end_value, annual_return, annual_variance, sharpe_ratio, max_drawdown] + list(weight_mean.values)

risk_level_list = ['high', 'middle', 'low']
#确定使用的数据文件
file_name_list = ['Index_Return_funds_future']

results_list = list()
for file_name in file_name_list:
    for risk_level in risk_level_list:

        if risk_level == 'high':
            lam = 1.0
        elif risk_level == 'middle':
            lam = 1.15
        elif risk_level == 'low':
            lam = 1.5
        else:
            pass

        ret_data = pd.read_excel(file_name + '.xlsx')
        return_data = pd.read_excel('Index_Return_funds.xlsx')

        year_delta = 5

        tau = 1.0
        wl_bl = list()
        for each in ret_data.index[60:]:
            year = each.year - year_delta
            month = each.month
            history_data = ret_data[str(year)+'-'+str(month): each][:-1]
            year_o = each.year - 2
            cov_mat = history_data[['H11001.CSI', '000300.SH', 'AU9999.SGE']].cov() * 12.0
            omega = np.matrix(cov_mat.values)
            mkt_wgt = Risk_Parity_Weight(cov_mat)
            P = np.diag([1] * len(mkt_wgt))
            conf_mat = np.matrix(np.diag([((history_data['H11001.CSI'][str(year_o)+'-'+str(month):]-history_data['Bond_pre'][str(year_o)+'-'+str(month):])**2).mean() * 12.0,
                                          ((history_data['000300.SH'][str(year_o)+'-'+str(month):]-history_data['Stock_pre'][str(year_o)+'-'+str(month):])**2).mean() * 12.0,
                                          ((history_data['AU9999.SGE'][str(year_o)+'-'+str(month):]-history_data['Gold_pre'][str(year_o)+'-'+str(month):])**2).mean() * 12.0]))
            Q = np.matrix(ret_data[['Bond_pre', 'Stock_pre', 'Gold_pre']].loc[each])
            com_ret, com_cov_mat = Combined_Return_Distribution(3, cov_mat, tau, mkt_wgt, P, Q, conf_mat)
            weight_bl = Max_Utility_Weight(com_ret, com_cov_mat, lam)
            wl_bl.append(list(weight_bl) + [(np.matrix(return_data[['H11001.CSI', '000300.SH', 'AU9999.SGE']].loc[each]) * np.matrix(weight_bl).T)[0,0]])

        wl_bl = pd.DataFrame(np.array(wl_bl), index=ret_data.index[60:], columns=list(ret_data[['H11001.CSI', '000300.SH', 'AU9999.SGE']].columns)+['return'])
        wl_bl.to_excel(file_name + '_funds_' + risk_level + '.xlsx')

        print Performance(file_name + '_funds_' + risk_level + '.xlsx', 0.025)
        results_list.append(Performance(file_name + '_funds_' + risk_level + '.xlsx', 0.025))

pd.DataFrame(np.array(results_list)).to_excel('results_funds_pre.xlsx')

'''
results_list = list()
results_list.append(Performance('Index_Return_high_adjusted.xlsx', 0.025))
results_list.append(Performance('Index_Return_middle_adjusted.xlsx', 0.025))
results_list.append(Performance('Index_Return_low_adjusted.xlsx', 0.025))
pd.DataFrame(np.array(results_list)).to_excel('results_adjusted.xlsx')
'''
