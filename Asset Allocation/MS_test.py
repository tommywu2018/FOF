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
