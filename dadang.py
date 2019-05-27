# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.join(os.path.dirname("ReadFile"),'.'))

import math



#COSINE
def Similar_CalDis_Vargas(urm,i,j):
    I=urm[:,i]
    #.todense();
    J=urm[:,j]
    #.todense();
    iTb= I.mean()
    jTb= J.mean()
    uLen=len(I)
    tu=0
    mauUI=0
    mauUJ=0
    for x in range(1,uLen):
        tu= tu + float((I[x]-iTb)*(J[x]-jTb))
        mauUI = mauUI+float((I[x]-iTb)*(I[x]-iTb))
        mauUJ= mauUJ+float((J[x]-jTb)*(J[x]-jTb))
    if(mauUI==0):
        return 0
    if(mauUJ==0):
        return 0
    mau= 2 * math.sqrt(mauUI)*math.sqrt(mauUJ)

    return float(1/2)-float(tu/mau)


#Jaccard         [4,5,10,18], [4,10,2,3,5]
def Similar_Dist_Jaccard(listCatory,i,j):
    itemI=listCatory[i]
    itemJ=listCatory[j]
    intersection = len(list(set(itemI).intersection(itemJ)))
    union = (len(itemI) + len(itemJ)) - intersection
    return float(intersection / union)

def CalDist(urm,listCatory,i,j,loai):
    if(loai==0):
        return Similar_CalDis_Vargas(urm,i,j)
    if(loai==1):
        return Similar_Dist_Jaccard(listCatory,i,j)
    i
    return Similar_CalDis_Vargas(urm,i,j)


def Diversity(urm,listCatory,listR,loai):
    s=float(0)
    l=len(listR)
    for i in listR:
        for j in listR:
            if (i!=j):
                s=s+ float(CalDist(urm,listCatory,i,j,loai))
    return s/(l*(l-1))

def objectiveFunction(urm,listCatory,user,R,listI,listRel,alpha,loai):
    lenR =len(R);
    maxObj=0;
    iMax=1
    dem=0
    for i in listI:
        if i in R:
            continue;
        di=0
        dem=dem+1
        if (lenR!=0):
            s=float(0)
            for j in R:
                s=s+float(CalDist(urm,listCatory,i,j,loai))
            di=s/lenR
        obj=alpha*listRel[i] + (1-alpha)*di
        if(obj>maxObj):
            maxObj=obj
            iMax=i
        #if(dem>100):  #gio han vong for, cho chay nhieu qua thi lau
            #return iMax
    return iMax

#danh sach do phu hop cua tung item
def vectorRel(urm,listI,u):
    listRel =dict()
    for i in listI:
        I=urm[:,i]
        #.todense();
        if(I.argmax()==0):
            listRel[i]=0
        else:
            listRel[i]=float(urm[u,i])/ float(I.argmax())#tinh chi so phu hop
    return listRel;

def IncreasingDiversity(urm,listCatory,user,listI,listRel,topN,alpha,loai):
    R=[]
    while len(R)<topN:
        i=objectiveFunction(urm,listCatory,user,R,listI,listRel,alpha,loai)
        R.append(i);
        #listI.pop(i);
    return R

