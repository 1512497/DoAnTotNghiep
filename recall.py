# -*- coding: utf-8 -*-
def Recall(listRecommd,relItem):
    nrelItem=len(relItem)
    nDung=0
    for i in listRecommd:
        if(relItem.index(i)!=-1):
            nDung=nDung+1
    return float(nDung/nrelItem)

def relItem(urm,user):
    lrm=urm[:user];
    listRelItem=list()
    for value,index in lrm:
        if(value>=3.5):
            listRelItem.append(index)
    return listRelItem