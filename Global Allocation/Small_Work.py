# coding=utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.multivariate.pca import PCA


Barclays_US_bond = pd.read_excel("/Users/WangBin-Mac/FOF/Global Allocation/Barclays_US_bond.xlsx")
BloomBerg_commodity = pd.read_excel("/Users/WangBin-Mac/FOF/Global Allocation/BloomBerg_commodity.xlsx")
FTSE_global_REITs = pd.read_excel("/Users/WangBin-Mac/FOF/Global Allocation/FTSE_global_REITs.xlsx")
London_gold = pd.read_excel("/Users/WangBin-Mac/FOF/Global Allocation/London_gold.xlsx")
MSCI_US_REITs = pd.read_excel("/Users/WangBin-Mac/FOF/Global Allocation/MSCI_US_REITs.xlsx")
MSCI_emerging = pd.read_excel("/Users/WangBin-Mac/FOF/Global Allocation/MSCI_emerging.xlsx")
MSCI_global = pd.read_excel("/Users/WangBin-Mac/FOF/Global Allocation/MSCI_global.xlsx")
SP500 = pd.read_excel("/Users/WangBin-Mac/FOF/Global Allocation/SP500.xlsx")
Barclays_US_HY = pd.read_excel("/Users/WangBin-Mac/FOF/Global Allocation/Barclays_US_HY.xlsx")
#Barclays_US_HY.resample("M").last().to_excel("/Users/WangBin-Mac/FOF/Global Allocation/Barclays_US_HY.xlsx")
Barclays_US_CB = pd.read_excel("/Users/WangBin-Mac/FOF/Global Allocation/Barclays_US_CB.xlsx")
#Barclays_US_CB.resample("M").last().to_excel("/Users/WangBin-Mac/FOF/Global Allocation/Barclays_US_CB.xlsx")
Barclays_US_Treasury = pd.read_excel("/Users/WangBin-Mac/FOF/Global Allocation/Barclays_US_Treasury.xlsx")
#Barclays_US_Treasury.resample("M").last().to_excel("/Users/WangBin-Mac/FOF/Global Allocation/Barclays_US_Treasury.xlsx")

data = pd.merge(Barclays_US_CB, BloomBerg_commodity, how='outer', left_index=True, right_index=True)
data = pd.merge(data, FTSE_global_REITs, how='outer', left_index=True, right_index=True)
data = pd.merge(data, London_gold, how='outer', left_index=True, right_index=True)
data = pd.merge(data, MSCI_US_REITs, how='outer', left_index=True, right_index=True)
data = pd.merge(data, MSCI_emerging, how='outer', left_index=True, right_index=True)
data = pd.merge(data, MSCI_global, how='outer', left_index=True, right_index=True)
data = pd.merge(data, SP500, how='outer', left_index=True, right_index=True)
data = pd.merge(data, Barclays_US_HY, how='outer', left_index=True, right_index=True)
data = pd.merge(data, Barclays_US_Treasury, how='outer', left_index=True, right_index=True)
data_M[['SP500', 'MSCI_global']].corr().iloc[1,0]


data.resample("M").last().pct_change().to_excel("/Users/WangBin-Mac/FOF/Global Allocation/All_Assets_M.xlsx")
def Rolling_Correlation(df, lags):
    corr_list = list()
    for i in range(lags-1, len(df)):
        temp_df = df[df.index[i+1-lags]:df.index[i]]
        corr_list.append(temp_df.corr().iloc[0,1])
    return pd.DataFrame(corr_list, index=df.index[lags-1:], columns=[df.columns[0]+'*'+df.columns[1]])

data_M = pd.read_excel("/Users/WangBin-Mac/FOF/Global Allocation/All_Assets_M.xlsx")
correl_frame = pd.DataFrame()
for each_i in data_M.columns:
    for each_j in data_M.columns[list(data_M.columns).index(each_i)+1:]:
        temp_data = data_M[[each_i, each_j]].dropna()
        temp_corr = Rolling_Correlation(temp_data, 20)
        correl_frame = pd.merge(correl_frame, temp_corr, how='outer', left_index=True, right_index=True)

correl_mean = correl_frame.mean(axis=1)
correl_mean.plot()
plt.show()

correl_mean = pd.DataFrame(correl_mean, columns=['corr_mean'])
correl_frame = pd.merge(correl_frame, correl_mean, how='outer', left_index=True, right_index=True)

correl_frame.corr()['corr_mean']


each = correl_frame.columns[1]
for each in correl_frame.columns[:-2]:
    temp_data = correl_frame[[each, 'corr_mean']].dropna()
    X = temp_data['corr_mean']
    X = sm.add_constant(X)
    y = temp_data[each]
    model = sm.OLS(y, X)
    results = model.fit()
    if (results.params[1] < 0) or (results.pvalues[1] >= 0.05):
        print each
