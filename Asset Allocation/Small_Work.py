# coding=utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

<<<<<<< HEAD
data = pd.read_excel("/Users/WangBin-Mac/FOF/Asset Allocation/History_Data.xlsx")


return_series = data["bond"]
drawdown = ((return_series + 1).cumprod().cummax()-(return_series + 1).cumprod())/(return_series + 1).cumprod().cummax()
drawdown = drawdown[drawdown>0]
drawdown.hist(bins=50)
print drawdown.quantile(0.5)
plt.show()
drawdown.plot()
=======
data = pd.read_excel("History_Data.xlsx")
return_series = data["bond"]
drawdown = ((return_series + 1).cumprod().cummax()-(return_series + 1).cumprod())/(return_series + 1).cumprod().cummax()
drawdown = drawdown[drawdown>0]
drawdown.hist(bins=30)
plt.show()

return_series = data["gold"]
de_series = return_series[return_series<0]
de_list = []
cum_de = 0.0
for each in return_series:
    if each < 0:
        cum_de = (1.0+cum_de)*(1.0+each)-1
    else:
        de_list.append(cum_de)
        cum_de = 0.0

de_series = pd.Series(de_list)
(-de_series[de_series<0]).hist(bins=30)
(-de_series[de_series<0]).quantile(0.5)
plt.show()

return_series = data["stock_large"]
return_series.quantile(0.10)
return_series = data["stock_small"]
return_series.quantile(0.10)
return_series = data["stock_US"]
return_series.quantile(0.10)
return_series = data["stock_HongKong"]
return_series.quantile(0.10)
return_series = data["bond"]
return_series.quantile(0.10)
return_series = data["gold"]
return_series.quantile(0.10)

data = pd.read_excel(u"/Users/WangBin-Mac/Documents/研究生文件/FOF投顾/201706报告/收益分解/nv_index.xlsx")

return_series = data[u"稳健组合"].pct_change().dropna()
Performance(return_series, 0.04)

return_series = data[u"平衡组合"].pct_change().dropna()
Performance(return_series, 0.04)

return_series = data[u"进取组合"].pct_change().dropna()
Performance(return_series, 0.04)

def Performance(return_series, rf_ret):
    end_value = (return_series + 1).prod()
    annual_return = (return_series + 1).prod() ** (1/(len(return_series)/240.0)) - 1
    annual_variance = (return_series.var() * 240.0) ** 0.5
    sharpe_ratio = (annual_return - rf_ret)/annual_variance
    max_drawdown = max(((return_series + 1).cumprod().cummax()-(return_series + 1).cumprod())/(return_series + 1).cumprod().cummax())
    (return_series + 1).cumprod().plot()
    return [end_value, annual_return, annual_variance, sharpe_ratio, max_drawdown]

from WindPy import *
w.start()
index_code_list = ["000300.SH", "000905.SH", "SPX.GI", "HSI.HI", "H11001.CSI", "AU9999.SGE", "H11025.CSI"]
temp_data = w.wsd(index_code_list, "close", "2017-02-01", "2017-03-30")
data = pd.DataFrame(np.array(temp_data.Data).T, index=temp_data.Times, columns=temp_data.Codes)
data.to_excel("D:\\FOF\\index.xlsx")
>>>>>>> origin/master
