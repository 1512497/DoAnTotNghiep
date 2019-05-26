# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.join(os.path.dirname("ReadFile"),'.'))

import math as mt
import numpy as np

def Serendipity(R,Runexp,Rusefull):
    return len(set.intersection(*[set(Runexp), set(Rusefull)]))/ len(R)

def RUnexp (R,Eu):
    runexp=list()
    for i in R:
        if i not in Eu:
            runexp.append(i);
    return runexp;

#Bao gom cac item da duoc danh gia va cac item tuong tu voi 
#nhung cai da danh gia(content)
def Eu(userVector,items,GroupByMovie,standardMetric):
    resdsItem=list()
    ratedItem=list()
    for i in range(1,len(userVector)):
        if(userVector[i]!=0):
            ratedItem.append(i)
            resdsItem.append(i)
    #khoi tao ma tran
    urm = np.zeros(shape=(len(items)+1,len(items)+1), dtype=np.float32)    
    for i in ratedItem:
        for j in items:
            if j not in resdsItem:
                urm[i,j]=float(jaccard_similarity(GroupByMovie[i],GroupByMovie[j]))
                if(urm[i,j]>=standardMetric):
                    resdsItem.append(j)
    return resdsItem
        
#tuong dong dua tren noi dung
def jaccard_similarity(x,y):

    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return float(intersection_cardinality/float(union_cardinality))

def RUsefull(matrix,R,max_uid,max_iid):  
    result=list()
    ave=np.arange(max_iid)
    ave=ave.reshape(max_iid)
    for i in range(1, max_iid):    
        tong=0            
        k=0
        for j in range(1, max_uid):
            if(matrix[j][i]!=0):
                tong=tong+matrix[j][i]
                k=k+1
        if(k!=0):        
            ave[i]=float(tong/k)
    for i in R:
        if(ave[i]>3.0):
            result.append(i)
    return result  
    


