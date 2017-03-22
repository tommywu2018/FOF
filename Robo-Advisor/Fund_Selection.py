# coding=utf-8

import pandas as pd
import numpy as np
import math

index_fund_map = {"000300.SH" : ["163415.OF", "090013.OF", "000308.OF", "519736.OF", "000577.OF"],
"000905.SH" : ["180031.OF", "000547.OF", "000524.OF", "040035.OF", "000471.OF"],
"SPX.GI" : ["513500.OF", "519981.OF", "096001.OF", "513100.OF"],
"HSI.HI" : ["159920.OF", "513660.OF"],
"H11001.CSI" : ["511220.OF", "001021.OF", "003358.OF", "511010.OF", "161821.OF", "159926.OF", "001512.OF", "000022.OF"],
"AU9999.SGE" : ["518880.OF", "159937.OF", "159934.OF", "320013.OF", "518800.OF"],
"H11025.CSI" : ["003022.OF", "000434.OF"]}

asset_weight = pd.Series([0.1, 0.1, 0.1, 0.1, 0.4, 0.1, 0.1], index=["000300.SH", "000905.SH", "SPX.GI", "HSI.HI", "H11001.CSI", "AU9999.SGE", "H11025.CSI"])

def Fund_Weight(asset_weight, fund_list):
    fund_count = int(math.ceil(asset_weight/0.05))
    if fund_count <= len(fund_list):
        return fund_list[:fund_count], [asset_weight/fund_count]*fund_count
    else:
        return fund_list, [asset_weight/len(fund_list)]*len(fund_list)

fund_list = []
weight_list = []
for each_asset in asset_weight.index:
    temp_fund_list, temp_weight_list = Fund_Weight(asset_weight[each_asset], index_fund_map[each_asset])
    fund_list = fund_list + temp_fund_list
    weight_list = weight_list + temp_weight_list

fund_weight = pd.Series(weight_list, index=fund_list)
