import pandas as pd
import numpy as np
import pyper as pr

data = pd.read_excel("/Users/WangBin-Mac/FOF/Global Allocation/SBG_US_M.xlsx")
data_W = data.pct_change().dropna()*100

return_list = list(data_W['SP500'])
return_frame = pd.DataFrame(np.array([return_list, [1]*len(return_list)]).T, columns=['return', 'One'])
r = pr.R(use_pandas=True)
r("library(MSwM)")

for each in range(20):
    r.assign("rframe", return_frame)
    r('''
    lm_return <- lm(formula=return~0+One, data=rframe)
    lm_mswm <- msmFit(lm_return, k=2, p=0, sw=c(T,T))
    rstd <- lm_mswm@std
    rCoef <- lm_mswm@Coef
    rtransMat <- lm_mswm@transMat
    rprob_smo <- lm_mswm@Fit@smoProb[-1,]
    #print(lm_mswm@Fit@logLikel)
    raic_mswn <- AIC(lm_mswm)
    raic_lm <- AIC(lm_return)
    ''')
    std = np.round(r.get("rCoef")[' One '], 4)
    if std[0]>std[1]:
        print [std[1], std[0]]
    else:
        print std

'''
round([1.123123,1.214125],4)
test = np.array([[1.1213124,2.12441241,3.125164],[1.1213124,2.12441241,3.125164]])
test = [1.1213124,2.12441241,3.125164]
a = np.round(test,4)[2]
a
test[0]
np.where(test, round(test, 4), 0)
'''


def Performance(return_series, rf_ret):
    end_value = (return_series + 1).prod()
    annual_return = (return_series + 1).prod() ** (1/(len(return_series)/12.0)) - 1
    annual_variance = (return_series.var() * 12.0) ** 0.5
    sharpe_ratio = (annual_return - rf_ret)/annual_variance
    max_drawdown = max(((return_series + 1).cumprod().cummax()-(return_series + 1).cumprod())/(return_series + 1).cumprod().cummax())
    return [end_value, annual_return, annual_variance, sharpe_ratio, max_drawdown]

def Comparance(file_path):
    data = pd.read_csv(file_path)
    ms_per = Performance(data["ms_return"], 0.04)
    bm_per = Performance(data["bm_return"], 0.04)
    ms_turnover = data[["SP500", "London_gold", "Barclays_US_bond"]].diff().dropna().abs().sum(axis=1).mean()*12
    bm_turnover = data[["s_bm", "g_bm", "b_bm"]].diff().dropna().abs().sum(axis=1).mean()*12
    ms_per.append(ms_turnover)
    bm_per.append(bm_turnover)
    return pd.DataFrame(np.array([ms_per, bm_per]).T, columns=[file_path[-8:-4] + "_ms", file_path[-8:-4] + "_bm"], index=['end_value', 'annual_return', 'annual_variance', 'sharpe_ratio', 'max_drawdown', 'turnover'])

def Comparance(file_path):
    data = pd.read_csv(file_path)
    ms_per = Performance(data["ms_return"], 0.04)
    bm_per = Performance(data["bm_return"], 0.04)
    ms_turnover = data[["SP500", "Barclays_US_bond"]].diff().dropna().abs().sum(axis=1).mean()*12
    bm_turnover = data[["s_bm", "b_bm"]].diff().dropna().abs().sum(axis=1).mean()*12
    ms_per.append(ms_turnover)
    bm_per.append(bm_turnover)
    return pd.DataFrame(np.array([ms_per, bm_per]).T, columns=[file_path[-8:-4] + "_ms", file_path[-8:-4] + "_bm"], index=['end_value', 'annual_return', 'annual_variance', 'sharpe_ratio', 'max_drawdown', 'turnover'])

Comparance("F:\GitHub\FOF\MU_e.csv").to_clipboard()
