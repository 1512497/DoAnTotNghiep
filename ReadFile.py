# -*- coding: utf-8 -*-
import numpy as np
from scipy.sparse import csc_matrix



def UserRatingMatrix(filename,MAX_UID,MAX_IID):
    urm = np.zeros(shape=(MAX_UID,MAX_IID), dtype=np.float32)
    f = open(filename, "r")
    
    for x in f:
        t= x.split('\t')
        urm[int(t[0]),int(t[1])]=int(t[2])
        
    return urm
        #print(x)

def GetListUSerTest(filename):
    uTest = dict()
    f = open(filename, "r")
    
    for x in f:
        t= x.split('\t')        
        uTest[int(t[0])]=list()
    return uTest


def getItem(filename):
    items = dict()
    f = open(filename, "r")
    
    for x in f:
        t= x.split('|')  
        items[int(t[0])]=int(t[0])
    return items

def getUser(filename):
    users = dict()
    f = open(filename, "r")
    
    for x in f:
        t= x.split('|')  
        users[int(t[0])]=int(t[0])
    return users

def getMoviesSeen(filename):
    moviesSeen = dict()
    f = open(filename, "r")
    
    for x in f:
        t= x.split('\t')
        try:
            moviesSeen[int(t[0])].append(int(t[1]))
        except:
            moviesSeen[int(t[0])] = list()
            moviesSeen[int(t[0])].append(int(t[1]))        
    return moviesSeen


def getGenres(filename):
    genres=dict()
    f=open(filename,"r")
    for x in f:
        t=x.split('|')
        if(len(t)==2):
            genres[int(t[1])]=t[0]
    return genres


def getMovies_Genres(itemsFile):
    GroupByCategory=dict() 
    GroupByMovies=dict()
    f=open(itemsFile,"r")
    for x in f:
        t=x.split('|')        
        for k in range(5,len(t)):
            if(int(t[k])==1):
                try:
                    GroupByCategory[k-5].append(int(t[0]))
                except:
                    GroupByCategory[k-5] = list()
                    GroupByCategory[k-5].append(int(t[0]))

                try:
                    GroupByMovies[int(t[0])].append(k-5)
                except:
                    GroupByMovies[int(t[0])] = list()
                    GroupByMovies[int(t[0])].append(k-5)
    return GroupByCategory,GroupByMovies


#GroupByMovies[0]=[2,4,4,5,6,2,1]
#GroupByMovies[1]=[2,4,4,5,6,2,1,32,2,]
#GroupByMovies[2]=[2,4,5,6,4,4,5,6,2,1]
#GroupByMovies[3]=[2,4,5,6,4,4,5,6,1]
#GroupByMovies[4]=[2,4,41]
#
#GroupByCategory[1]=[100,200,4002,23,445,234]
#GroupByCategory[2]=[100,200,4002,23,445,234]



#urm=UserRatingMatrix("D:/4/DOAN TN/ml-100k/u1.base")
#uTest=GetListUSerTest("D:/4/DOAN TN/ml-100k/u1.test")
#gMS=getMoviesSeen("D:/4/DOAN TN/ml-100k/u1.base")
#print(urm)
#print(uTest)
#print(gMS)