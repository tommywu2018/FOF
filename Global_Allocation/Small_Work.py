# coding=utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_excel("F:\GitHub\FOF\Global_Allocation\SP500.xlsx")
data.to_excel("F:\GitHub\FOF\Global_Allocation\SP500.xlsx")

sp_data = pd.read_excel("F:\GitHub\FOF\Global_Allocation\SP500.xlsx")
gold_data = pd.read_excel("F:\GitHub\FOF\Global_Allocation\London_gold.xlsx")
bond_data = pd.read_excel("F:\GitHub\FOF\Global_Allocation\Barclays_US_bond.xlsx")

len(sp_data)
len(gold_data)
len(bond_data)
data = pd.merge(sp_data, gold_data, left_index=True, right_index=True)
data = pd.merge(data, bond_data, left_index=True, right_index=True)

data.plot()
plt.show()

data.resample("W").to_excel("F:\GitHub\FOF\Global_Allocation\SBG_US_W.xlsx")
