# -*- coding: utf-8 -*-
import numpy as np

def Recall(listRecommd,relItem):
    nDung = len(set.intersection(*[set(listRecommd), set(relItem)]))
    nrelItem=len(relItem)
    print (nDung,nrelItem)
    return float(nDung/nrelItem)

def relItem(urm,user):
    (rows,columns)=np.shape(urm)
    listRelItem = list()
    for i in range(1,columns):
        if(urm[user][i]>=3.5):
            listRelItem.append(i)
    return listRelItem