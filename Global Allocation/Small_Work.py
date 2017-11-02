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

data = pd.merge(Barclays_US_bond, Barclays_US_Treasury, how='outer', left_index=True, right_index=True)
data = pd.merge(data, Barclays_US_CB, how='outer', left_index=True, right_index=True)
data = pd.merge(data, Barclays_US_HY, how='outer', left_index=True, right_index=True)
data = pd.merge(data, SP500, how='outer', left_index=True, right_index=True)
data = pd.merge(data, MSCI_US_REITs, how='outer', left_index=True, right_index=True)
data = pd.merge(data, MSCI_global, how='outer', left_index=True, right_index=True)
data = pd.merge(data, MSCI_emerging, how='outer', left_index=True, right_index=True)
data = pd.merge(data, FTSE_global_REITs, how='outer', left_index=True, right_index=True)
data = pd.merge(data, BloomBerg_commodity, how='outer', left_index=True, right_index=True)
data = pd.merge(data, London_gold, how='outer', left_index=True, right_index=True)
#data_M[['SP500', 'MSCI_global']].corr().iloc[1,0]


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
        temp_corr = Rolling_Correlation(temp_data, 24)
        correl_frame = pd.merge(correl_frame, temp_corr, how='outer', left_index=True, right_index=True)

correl_frame.to_excel("/Users/WangBin-Mac/FOF/Global Allocation/All_Assets_correlframe.xlsx")
correl_frame.mean()[correl_frame.mean() > 0.8]
correl_frame.plot.violin()
plt.show()
plt.boxplot(correl_frame["Barclays_US_bond*Barclays_US_HY"])



plt.figure(figsize=(33,22))
for i in range(0,11):
    for j in range(i,11):
        if i == j:
            pass
        else:
            num = (j-1)*10+i+1
            plt.subplot(10,10,num)
            plt.ylim(-1,1)
            if i != 0:
                plt.yticks([])
            else:
                pass
            if j != 10:
                plt.xticks([])
            else:
                pass
            temp_name = data_M.columns[i] + "*" + data_M.columns[j]
            plt.violinplot(np.array(correl_frame[temp_name].dropna()), showmeans=True, vert=True)
plt.show()

fig = plt.figure(figsize=(33,22))
for i in range(0,11):
    for j in range(0,11):
        if i == j:
            if i == 0:
                ax1 = plt.subplot(11,11,1)
                plt.ylim(-1,1) #设置纵坐标范围
                plt.xlim(0.75,1.25) #设置横坐标范围
                plt.xticks([]) #不显示横坐标
                ax1.spines["bottom"].set_color("none") #隐藏下边线
                ax1.spines["right"].set_color("none") #隐藏右边线
                plt.plot([-1,-2,-3],[-1,-2,-3]) #在坐标范围外画一个虚图
            if j == 10:
                ax2 = plt.subplot(11,11,121)
                plt.ylim(-1,1)
                plt.xlim(0.75,1.25)
                plt.yticks([])
                ax2.spines["top"].set_color("none")
                ax2.spines["left"].set_color("none")
                plt.plot([-1,-2,-3],[-1,-2,-3])
        else:
            num = j*11+i+1
            plt.subplot(11,11,num)
            plt.ylim(-1,1)
            plt.xlim(0.75,1.25)
            if i != 0:
                plt.yticks([])
            else:
                pass
            if j != 10:
                plt.xticks([])
            else:
                pass
            if i < j:
                temp_name = data_M.columns[i] + "*" + data_M.columns[j]
            else:
                temp_name = data_M.columns[j] + "*" + data_M.columns[i]
            plt.violinplot(np.array(correl_frame[temp_name].dropna()), showmeans=True, vert=True)
            plt.hlines(0, 0, 2, colors='r', linestyles='dashed')
#plt.show()
fig.savefig("/Users/WangBin-Mac/FOF/Global Allocation/All_Assets_correl.png")



correl_mean_frame = pd.DataFrame(index=data_M.columns, columns=data_M.columns)
for each in correl_frame.mean().index:
    name_list = each.split("*")
    correl_mean_frame[name_list[0]][name_list[1]] = correl_frame.mean()[each]

correl_min_frame = pd.DataFrame(index=data_M.columns, columns=data_M.columns)
for each in correl_frame.min().index:
    name_list = each.split("*")
    correl_min_frame[name_list[0]][name_list[1]] = correl_frame.min()[each]

correl_max_frame = pd.DataFrame(index=data_M.columns, columns=data_M.columns)
for each in correl_frame.max().index:
    name_list = each.split("*")
    correl_max_frame[name_list[0]][name_list[1]] = correl_frame.max()[each]

"ab*cd".split("*")
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
