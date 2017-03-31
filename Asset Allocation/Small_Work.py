# coding=utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_excel("/Users/WangBin-Mac/FOF/Asset Allocation/History_Data.xlsx")


return_series = data["bond"]
drawdown = ((return_series + 1).cumprod().cummax()-(return_series + 1).cumprod())/(return_series + 1).cumprod().cummax()
drawdown = drawdown[drawdown>0]
drawdown.hist(bins=50)
print drawdown.quantile(0.5)
plt.show()
drawdown.plot()
