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
elif hostname == "":
    path = "F:/GitHub/FOF/Global Allocation/"

data_M = pd.read_excel(path+"All_Assets_M.xlsx")
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
