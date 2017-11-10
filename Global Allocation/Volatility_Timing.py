# coding=utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import socket
from statsmodels.multivariate.pca import PCA

hostname = socket.gethostname()
if hostname == "DESKTOP-OGC5NH7":
    path = "E:/GitHub/FOF/Global Allocation/"
elif hostname == "localhost":
    path = "/Users/WangBin-Mac/FOF/Global Allocation/"
elif hostname == "CICCB6CR7213VFT":
    path = "F:/GitHub/FOF/Global Allocation/"

data_M = pd.read_excel(path+"All_Assets_M.xlsx")

#粗略测试资产各资产Volatility Timing
for each in data_M.columns:
    temp_series = data_M[each].dropna()
    var_list = list()
    return_list = list()
    for i in range(25,len(temp_series)):
        temp_var = temp_series[i-24:i-1].var()
        var_list.append(temp_var)
    b = np.mean(var_list)
    for i in range(25,len(temp_series)):
        temp_var = temp_series[i-24:i-1].var()
        var_list.append(temp_var)
        multiplier = b/temp_var
        temp_return = multiplier*temp_series[i]
        return_list.append([temp_return, temp_series[i]])
    print each
    print (pd.DataFrame(return_list)+1).product()

#详细测试各资产Volatility Timing
data_D = pd.read_excel(path+"All_Assets_D.xlsx")
for each in ['Barclays_US_bond','SP500','MSCI_US_REITs','MSCI_emerging','BloomBerg_comodity','London_gold']:
    temp_series_d = data_D[each].dropna()
    temp_series_m = data_M[each][temp_series_d.index[0]:].dropna()
    i=1
    var_list = list()
    return_list = list()
    for i in range(1, len(temp_series_m)-1):
        temp_var = temp_series_d[temp_series_m.index[i-1]:temp_series_m.index[i]][1:].var()
        try:
            np.testing.assert_equal(temp_var, np.nan)
        except:
            var_list.append(temp_var)
        else:
            pass
    b = np.mean(var_list)
    for i in range(1, len(temp_series_m)-1):
        temp_var = temp_series_d[temp_series_m.index[i-1]:temp_series_m.index[i]][1:].var()
        try:
            np.testing.assert_equal(temp_var, np.nan)
        except:
            var_list.append(temp_var)
            multiplier = b/temp_var
            temp_return = multiplier*temp_series_m[i+1]
            return_list.append([temp_return, temp_series_m[i+1]])
        else:
            pass

    print each
    print (pd.DataFrame(return_list)+1).product()

var_M = data_M.rolling(24,min_periods=24,axis=0).var().dropna()
var_pca = PCA(var_M)
var_pca.rsquare
var_pca.factors['comp_00']
var_pca = pd.DataFrame(var_pca.factors['comp_00'].values, index=var_M.index, columns=['var_pca'])
var_M = pd.merge(var_M, var_pca, how='outer', left_index=True, right_index=True)
var_M.corr()['var_pca']


results_frame = []
for each in var_M.columns[:-2]:
    temp_data = var_M[[each,'var_pca']].dropna()
    X = temp_data['var_pca']
    X = sm.add_constant(X)
    y = temp_data[each]
    model = sm.OLS(y, X)
    results = model.fit()
    #print type(results.params)
    #print type(results.pvalues)
    #print type(results.rsquared)
    results_list = list(results.params) + list(results.pvalues) + [results.rsquared]
    results_frame.append(results_list)    

panel_data = list()
for each in var_M.columns[:-2]:
    temp_panel = pd.DataFrame(columns=['y','x']+list(var_M.columns[:-2]))
    temp_data = var_M[[each, 'var_pca']].dropna()
    temp_panel['y'] = temp_data[each]
    temp_panel['x'] = temp_data['var_pca']
    for each_i in list(var_M.columns[:-2]):
        if each_i == each:
            temp_panel[each_i] = 1
        else:
            temp_panel[each_i] = 0
    panel_data = panel_data + list(temp_panel.values)

panel_frame = pd.DataFrame(np.array(panel_data),columns=['y','x']+list(var_M.columns[:-2]))
X = panel_frame[['x']+list(var_M.columns[:-2])]
y = panel_frame['y']
model = sm.OLS(y, X)
results = model.fit()
results.params
results.pvalues
results.rsquared


correl_frame = pd.read_excel(path+"Selected_Assets_correlframe.xlsx")
correl_mean = correl_frame.mean(axis=1)
correl_mean = pd.DataFrame(correl_mean, columns=['corr_mean'])
correl_frame = pd.merge(correl_frame, correl_mean, how='outer', left_index=True, right_index=True)
correl_pca = PCA(correl_frame[correl_frame.columns[:-2]].dropna())
correl_pca = pd.DataFrame(correl_pca.factors['comp_00'].values, index=correl_frame.dropna().index, columns=['corr_pca'])
correl_frame = pd.merge(correl_frame, correl_pca, how='outer', left_index=True, right_index=True)

var_pca = pd.DataFrame(var_M['var_pca'].values, index=correl_frame.dropna().index, columns=['var_pca'])
correl_frame = pd.merge(correl_frame, var_pca, how='outer', left_index=True, right_index=True)
