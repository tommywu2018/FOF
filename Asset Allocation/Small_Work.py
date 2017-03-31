# coding=utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
