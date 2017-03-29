# coding=utf-8

import pandas as pd
import numpy as np
import pyper as pr
from Allocation_Method import Risk_Parity_Weight

#Simulation
def Ms_Simulation(length, p=0.9, q=0.7, mean_p=0.05, mean_q=-0.1, std_p=0.1, std_q=0.15):
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
    ''')
    std = r.get("rstd")
    Coef = np.array(r.get("rCoef")[' One '])
    transMat = r.get("rtransMat").T
    prob_smo = r.get("rprob_smo")
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
            temp_std = np.array([np.std(list(return_frame['each']))]*2)
            temp_Coef = np.array([np.mean(list(return_frame['each']))]*2)
            temp_transMat = np.array([[1,0],[0,1]]).reshape(2,2)
            temp_prob_smo = np.array([[1]*len(return_frame['each']),[0]*len(return_frame['each'])]).T
        temp_Ms_list.append([temp_std, temp_Coef, temp_transMat, temp_prob_smo])
    Ms_frame = pd.DataFrame(temp_Ms_list, index=temp_columns, columns=['std','Coef','transMat','prob_smo']).T

    temp_cov_list = []
    for each_i in temp_columns:
        for each_j in temp_columns[temp_columns.index(each_i):]:
            temp_cov_mat = Cross_Cov(return_frame[each_i], return_frame[each_j], Ms_frame[each_i]['Coef'], Ms_frame[each_j]['Coef'], Ms_frame[each_i]['prob_smo'], Ms_frame[each_j]['prob_smo'])
            temp_cov_list.append(temp_cov_mat)

    Tree = Tree_Gen(len(temp_columns))
    rp_wgt_list = []
    for each_leaf in Tree:
        cov_mat_list = []
        for i in range(len(temp_columns)):
            for j in range(len(temp_columns)):
                if i == j:
                    cov_mat_list.append(Ms_frame[temp_columns[i]]['std'][int(each_leaf[i])])
                else:
                    if i>j :
                        cov_mat_list.append(temp_cov_list[i+j][int(each_leaf[i]),int(each_leaf[j])])
                    else:
                        cov_mat_list.append(temp_cov_list[i+j][int(each_leaf[j]),int(each_leaf[i])])
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
test_list_1 = Ms_Simulation(350)
test_list_2 = Ms_Simulation(350)
ms_list = []
bm_list = []
for i in range(100):
    tl_cut_1 = test_list_1[:250+i]
    tl_cut_2 = test_list_2[:250+i]
    test_frame = pd.DataFrame(np.array([tl_cut_1,tl_cut_2]).T, columns=['A','B'])
    wgt = Ms_RP(test_frame, {'A':True, 'B':True})
    '''
    wgt = pd.Series([0.6, 0.4], index=['A','B'])
    '''
    ms_return = wgt['A']*test_list_1[250+i] + wgt['B']*test_list_2[250+i]
    bm_return = (test_list_1[250+i] + test_list_2[250+i])/2
    print ms_return
    print bm_return
    ms_list.append(ms_return)
    bm_list.append(bm_return)

print (pd.Series(ms_list)+1).prod()
print (pd.Series(bm_list)+1).prod()
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
test = [1,2,3,4]
test[3]