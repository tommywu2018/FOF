# coding=utf-8

import pandas as pd
import numpy as np
import pyper as pr
#import matplotlib.pyplot as plt

from Allocation_Method import Risk_Parity_Weight

#Simulation
def Ms_Simulation(length, p=0.9, q=0.8, mean_p=0.1, mean_q=-0.1, std_p=0.05, std_q=0.15):
    temp_list = []
    indicator = 1
    for i in range(length):
        if indicator == 1:
            temp_ran = np.random.uniform(0, 1)
            if temp_ran <= p:
                temp_data = np.random.randn() * std_p + mean_p
            else:
                temp_data = np.random.randn() * std_q + mean_q
                indicator = 0
        else:
            temp_ran = np.random.uniform(0, 1)
            if temp_ran <= q:
                temp_data = np.random.randn() * std_q + mean_q
            else:
                temp_data = np.random.randn() * std_p + mean_p
                indicator = 1
        temp_list.append(temp_data)
    return temp_list

def Ms_R(return_list):
    #return_list = list(data_M["AU9999.SGE"])
    return_frame = pd.DataFrame(np.array([return_list, [1]*len(return_list)]).T, columns=['return', 'One'])
    r = pr.R(use_pandas=True)
    r.assign("rframe", return_frame)
    r('''
    library(MSwM)
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
    aic_mswm = r.get("raic_mswm")
    aic_lm = r.get("raic_lm")
    if aic_mswm < aic_lm:
        std = r.get("rstd")
        Coef = np.array(r.get("rCoef")[' One '])
        transMat = r.get("rtransMat").T
        prob_smo = r.get("rprob_smo")
    else:
        std = np.array([np.std(return_list)]*2)
        Coef = np.array([np.mean(return_list)]*2)
        transMat = np.array([[1,0],[0,1]]).reshape(2,2)
        prob_smo = np.array([[0.5]*len(return_list),[0.5]*len(return_list)]).T

    return std, Coef, transMat, prob_smo

def Cross_Cov(return_list_1, return_list_2, Coef_1, Coef_2, prob_smo_1, prob_smo_2):
    temp_list = []
    for i in range(2):
        for j in range(2):
            temp_cov = np.sum(prob_smo_1[:,i]*prob_smo_2[:,j]*(return_list_1 - Coef_1[i])*(return_list_2 - Coef_2[j]))/np.sum(prob_smo_1[:,i]*prob_smo_2[:,j])
            temp_list.append(temp_cov)
    cov_mat = np.array(temp_list).reshape(2,2)
    return cov_mat

def Tree_Gen(length):
    temp_list = []
    for i in range(2**length):
        temp_bin = bin(i)
        temp_bin = temp_bin.replace('0b', '')
        if len(temp_bin) < length:
            temp_bin = '0'*(length-len(temp_bin)) + temp_bin
        temp_list.append(temp_bin)
    return temp_list

# intTree_Gen(4)[1][0]
def Ms_RP(return_frame, switch_map):
    temp_columns = list(return_frame.columns)

    temp_Ms_list = []
    for each in temp_columns:
        if switch_map[each]:
            temp_std, temp_Coef, temp_transMat, temp_prob_smo = Ms_R(list(return_frame[each]))
        else:
            temp_std = np.array([np.std(list(return_frame[each]))]*2)
            temp_Coef = np.array([np.mean(list(return_frame[each]))]*2)
            temp_transMat = np.array([[1,0],[0,1]]).reshape(2,2)
            temp_prob_smo = np.array([[0.5]*len(return_frame[each]),[0.5]*len(return_frame[each])]).T
        temp_Ms_list.append([temp_std, temp_Coef, temp_transMat, temp_prob_smo])
    Ms_frame = pd.DataFrame(temp_Ms_list, index=temp_columns, columns=['std','Coef','transMat','prob_smo']).T

    temp_cov_list = []
    for each_i in temp_columns:
        for each_j in temp_columns[temp_columns.index(each_i)+1:]:
            temp_cov_mat = Cross_Cov(return_frame[each_i], return_frame[each_j], Ms_frame[each_i]['Coef'], Ms_frame[each_j]['Coef'], Ms_frame[each_i]['prob_smo'], Ms_frame[each_j]['prob_smo'])
            temp_cov_list.append(temp_cov_mat)

    Tree = Tree_Gen(len(temp_columns))
    rp_wgt_list = []
    for each_leaf in Tree:
        cov_mat_list = []
        for i in range(len(temp_columns)):
            for j in range(len(temp_columns)):
                if i == j:
                    cov_mat_list.append((Ms_frame[temp_columns[i]]['std'][int(each_leaf[i])])**2)
                else:
                    if i < j :
                        location = len(temp_columns)*(i+1)-sum(range(i+2))-(len(temp_columns)-j)
                        cov_mat_list.append(temp_cov_list[location][int(each_leaf[i]),int(each_leaf[j])])
                    else:
                        location = len(temp_columns)*(j+1)-sum(range(j+2))-(len(temp_columns)-i)
                        cov_mat_list.append(temp_cov_list[location][int(each_leaf[j]),int(each_leaf[i])])
        cov_mat = np.array(cov_mat_list).reshape(len(temp_columns), len(temp_columns))
        cov_mat = pd.DataFrame(cov_mat, columns=temp_columns, index=temp_columns)
        rp_wgt = Risk_Parity_Weight(cov_mat)
        rp_wgt_list.append(rp_wgt)

    prob_list =[]
    for each_leaf in Tree:
        prob_leaf = 1
        for i in range(len(temp_columns)):
            stat = int(each_leaf[i])
            trans_mat = Ms_frame[temp_columns[i]]['transMat']
            temp_prob = Ms_frame[temp_columns[i]]['prob_smo'][-1,0]*trans_mat[0,stat] + Ms_frame[temp_columns[i]]['prob_smo'][-1,1]*trans_mat[0,stat]
            prob_leaf = prob_leaf * temp_prob
        prob_list.append(prob_leaf)
    '''
    filt_prob_list = []
    for each_prob in prob_list:
        if each_prob == max(prob_list):
            filt_prob_list.append(1.0)
        else:
            filt_prob_list.append(0.0)
    prob_list = filt_prob_list
    '''
    prob_wgt_list = []
    for i in range(len(Tree)):
        prob_wgt_list.append(rp_wgt_list[i]*prob_list[i])

    return sum(prob_wgt_list)

'''
ratio_list = []
for ii in range(100):
    test_list_1 = Ms_Simulation(250)
    test_list_2 = Ms_Simulation(250)
    test_frame = pd.DataFrame(np.array([test_list_1,test_list_2]).T, columns=['A','B'])
    wgt = Ms_RP(test_frame, {'A':True, 'B':True})
    ratio = wgt['A']
    print ratio
    ratio_list.append(ratio)

print max(ratio_list)
print min(ratio_list)
print np.mean(ratio_list)
'''


MS_list = []
BM_list = []
for each in range(100):
    test_list_1 = Ms_Simulation(480, 0.94798285, 0.94177644, 0.011348197, 0.0025831495, 0.02178261, 0.05045428)
    test_list_2 = Ms_Simulation(480, 0.90419533, 0.97432935, 0.021510161, 0.0016860435, 0.09058209, 0.03235686)
    test_list_3 = Ms_Simulation(480, 1, 1, 0.00616607, 0.00616607, 0.014926817, 0.014926817)
    ms_list = []
    bm_list = []
    for i in range(360):
        tl_cut_1 = test_list_1[:120+i]
        tl_cut_2 = test_list_2[:120+i]
        tl_cut_3 = test_list_3[:120+i]
        test_frame = pd.DataFrame(np.array([tl_cut_1,tl_cut_2,tl_cut_3]).T, columns=['A','B','C'])

        wgt = Ms_RP(test_frame, {'A':True, 'B':True, 'C':False})

        wgt_rp = Risk_Parity_Weight(test_frame.cov())

        ms_return = wgt['A']*test_list_1[120+i] + wgt['B']*test_list_2[120+i] + wgt['C']*test_list_3[120+i]
        bm_return = wgt_rp['A']*test_list_1[120+i] + wgt_rp['B']*test_list_2[120+i] + wgt_rp['C']*test_list_3[120+i]

        #test_frame = pd.DataFrame(np.array([tl_cut_1,tl_cut_2]).T, columns=['A','B'])

        #wgt = Ms_RP(test_frame, {'A':True, 'B':True})

        #wgt = pd.Series([0.6, 0.4], index=['A','B'])

        #ms_return = wgt['A']*test_list_1[250+i] + wgt['B']*test_list_2[250+i]
        #bm_return = (test_list_1[250+i] + test_list_2[250+i])/2
        #print ms_return
        #print bm_return
        ms_list.append(ms_return)
        bm_list.append(bm_return)

    MS_list.append((pd.Series(ms_list)+1).prod())
    BM_list.append((pd.Series(bm_list)+1).prod())
    print str(each)
    print (pd.Series(ms_list)+1).prod()
    print (pd.Series(bm_list)+1).prod()
    print "-----"

print np.mean(MS_list)
print np.mean(BM_list)

'''
data = pd.read_excel("/Users/WangBin-Mac/FOF/Global Allocation/SBG_US_M.xlsx")
#data_W = (data/100+1).resample("W").prod().dropna()-1
#data_M = (data/100+1).resample("M").prod()-1
data_W = data.pct_change().dropna()

ms_list = []
bm_list = []
for each in range(100,len(data_W)-1):
    #each = 95
    #data_M.index[each]
    data_frame = data_W[data_W.index[each-100]:data_W.index[each]]

    wgt = Ms_RP(data_frame, {'SP500':True, 'London_gold':True, 'Barclays_US_bond':False})
    wgt_bm = Risk_Parity_Weight(data_frame.cov())

    #wgt = pd.Series([0.2, 0.2, 0.6], index=data_frame.columns)
    print wgt
    print data_W.loc[data_W.index[each+1]]
    ms_return = np.sum(wgt*data_W.loc[data_W.index[each+1]])
    bm_return = np.sum(wgt_bm*data_W.loc[data_W.index[each+1]])
    print data_W.index[each+1]
    print ms_return
    print bm_return
    ms_list.append(ms_return)
    bm_list.append(bm_return)

print (pd.Series(ms_list)+1).prod()
print np.std(pd.Series(ms_list))
print (pd.Series(bm_list)+1).prod()
print np.std(pd.Series(bm_list))
'''
'''
data_W['Barclays_US_bond'].mean()
return_list = list(data_W['Barclays_US_bond'])
return_frame = pd.DataFrame(np.array([return_list, [1]*len(return_list)]).T, columns=['return', 'One'])
r = pr.R(use_pandas=True)
r.assign("rframe", return_frame)
r(
library(MSwM)
lm_return <- lm(formula=return~0+One, data=rframe)
lm_mswm <- msmFit(lm_return, k=2, p=0, sw=c(T,T))
rstd <- lm_mswm@std
rCoef <- lm_mswm@Coef
rtransMat <- lm_mswm@transMat
rprob_smo <- lm_mswm@Fit@smoProb[-1,]
#print(lm_mswm@Fit@logLikel)
raic_mswn <- AIC(lm_mswm)
raic_lm <- AIC(lm_return)
)
std = r.get("rstd")
Coef = np.array(r.get("rCoef")[' One '])
transMat = r.get("rtransMat").T
prob_smo = r.get("rprob_smo")
std
Coef
transMat
prob_smo
'''

'''
$std
$model
$Coef
$seCoef
$transMat
$iniProb
$call
$k
$switch
$p
$Fit
    slot"CondMean"
    slot"error"
    slot"Likel"
    slot"margLik"
    slot"filtProb"
    slot"smoProb"
    slot"smoTransMat"
    slot"logLikel"
$class
'''
