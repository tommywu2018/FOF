# coding=utf-8

import numpy as np
import pandas as pd
from WindPy import *
w.start()

file_dir = u"Z:\\Mac 上的 WangBin-Mac\\"
start_date = "2014-08-16"
end_date = "2017-08-22"

index_list = ["H11025.CSI", "038.CS", "066.CS", "000300.SH", "000905.SH", "HSI.HI", "SPX.GI", "AU9999.SGE", "885064.WI"]
index_name = ["money_fund", "bond_rate", "bond_credit", "stock_A_large", "stock_A_small", "stock_HongKong", "stock_US", "gold", "hedge_fund"]

ETF_list = []
fund_list = []

index_data = w.wsd(index_list, "close", start_date, end_date, "Days=Alldays")
print index_data.ErrorCode
index_data = pd.DataFrame(np.array(index_data.Data).T, index=index_data.Times, columns=index_name)
index_data.index = index_data.index.strftime('%Y-%m-%d')
index_data.to_csv(file_dir+"index.csv")

etf_data = w.wsd(index_list, "close", start_date, end_date, "Days=Alldays")
print etf_data.ErrorCode
etf_data = pd.DataFrame(np.array(etf_data.Data).T, index=etf_data.Times, columns=ETF_list)
etf_data.index = etf_data.index.strftime('%Y-%m-%d')

fund_data = w.wsd(fund_list, "NAV_adj", start_date, end_date, "Days=Alldays")
print fund_data.ErrorCode
fund_data = pd.DataFrame(np.array(fund_data.Data).T, index=fund_data.Times, columns=fund_list)
fund_data.index = fund_data.index.strftime("%Y-%m-%d")

sub_product_data = pd.merge(etf_data, fund_data, left_index=True, right_index=True)

money_product_position = pd.read_excel(file_dir+"money_product_position.xlsx")
bond_product_position = pd.read_excel(file_dir+"bond_product_position.xlsx")
domestic_stock_product_position = pd.read_excel(file_dir+"domestic_stock_product_position.xlsx")
foreign_stock_position = pd.read_excel(file_dir+"foreign_stock_product_position.xlsx")
alternative_product_position = pd.read_excel(file_dir+"alternative_product_position.xlsx")

product_data = pd.DataFrame()
product_data['money_product'] = (money_product_position * sub_product_data[money_product_position.columns]).sum(axis=1)
product_data['bond_product'] = (bond_product_position * sub_product_data[bond_product_position.columns]).sum(axis=1)
product_data['domestic_stock_product'] = (domestic_stock_product_position * sub_product_data[domestic_stock_product_position.columns]).sum(axis=1)
product_data['foreign_stock_product'] = (foreign_stock_product_position * sub_product_data[foreign_stock_product_position.columns]).sum(axis=1)
product_data['alternative_product'] = (alternative_product_position * sub_product_data[alternative_product_position.columns]).sum(axis=1)


tdata = np.array(range(9)).reshape(3,3)
test1 = pd.DataFrame(tdata, index=[1,2,3], columns=['a','b','c'])
test2 = pd.DataFrame(tdata, index=[1,2,3], columns=['a','b','c'])
(test1*test2).sum(axis=1)

test3 = pd.DataFrame()
test3['a'] = (test1*test2).sum(axis=1)
