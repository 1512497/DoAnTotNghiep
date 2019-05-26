# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.join(os.path.dirname("ReadFile"),'.'))

import math as mt
import numpy as np

#do pho bien cua 1 item
def Popularity(i,matrix):
    (rows,colunms)=np.shape(matrix)
    u=0
    for j in range(1, rows):
        if(matrix[j][i]!=0):                
            u=u+1
    p=float(u/rows)                    
    return p

def Novelty(R,matrix):
    tong=0
    for i in R:
        tong=float(tong-mt.log(Popularity(i,matrix),2))
    (rows,columns)=np.shape(matrix)    
    nov_max=-mt.log(float(1/rows),2)
    return float(1/(nov_max*len(R)))* float(tong/len(R))

#danh sach cac user danh gia item
def List_Rating_Item(urm, item):
    result=list()
    (rows,columns)=np.shape(urm)
    for u in range(1, rows):
        if(urm[u][item]!=0):
            result.append(u)
    return result
        
def objectiveFunctionNovelty(urm,listItem,U,R):    
    maxObj=0;
    iMax=1
    for i in listItem:
        if i in R:
            continue;
        rating_item=List_Rating_Item(urm,i);
        if(len(rating_item)==0):
            obj=0
        else:
            obj=-mt.log(len(rating_item)/U,2)
        if(obj>maxObj):
            maxObj=obj
            iMax=i
        #if(dem>100):  #gio han vong for, cho chay nhieu qua thi lau
            #return iMax
    return iMax


def IncreasingNovelty(urm,listItem,listUser,topN):
    R=[]
    U= len(listUser)
    while len(R)<topN:
        i=objectiveFunctionNovelty(urm,listItem,U,R)
        R.append(i);
        #listItem.pop(i);
    return R


#xu ly lai ham IncreasingNovelty
# bang cach1 tinh listObject cua tung item truoc
# roi sap xep lai, chon ra top N phan cao cao nhat
def IncreasingNoveltyNhanh(urm,listItem,listUser,topN):
    R=[]
    U= len(listUser)
    listObj=list()
    for i in listItem:
        rating_item=List_Rating_Item(urm,i);
        if(len(rating_item)==0):
            obj=0
        else:
            obj=-mt.log(len(rating_item)/U,2)
        listObj.append([i,float(obj)])

    listObj= sorted(listObj,key= lambda obj:obj[1],reverse=True)[:topN]
    for i in listObj:
        if len(R)>=topN:
            break;
        R.append(i[0])
    return R