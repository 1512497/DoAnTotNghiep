# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.join(os.path.dirname("ReadFile"),'.'))
import math as mt
import numpy as np

from scipy.sparse import csr_matrix
from scipy.sparse import csc_matrix
from sparsesvd import sparsesvd
import pandas as pd



###########################################################
#                                                         #
#               MF                                        #
#                                                         #
###########################################################

def computeSVD(urm, K):
    urm=csc_matrix(urm, dtype=np.float32)
    U, s, Vt = sparsesvd(urm, K)
    dim = (len(s), len(s))
    S = np.zeros(dim, dtype=np.float32)
    for i in range(0, len(s)):
        S[i,i] = mt.sqrt(s[i])

    U = csr_matrix(np.transpose(U), dtype=np.float32)
    S = csr_matrix(S, dtype=np.float32)
    Vt = csr_matrix(Vt, dtype=np.float32)

    return U, S, Vt	

def MF(U, S, Vt, dsTest, moviesSeen,topN,MAX_UID, MAX_PID):
	rightTerm = S*Vt

	estimatedRatings = np.zeros(shape=(MAX_UID, MAX_PID), dtype=np.float16)
	for userTest in dsTest:
		prod = U[userTest, :]*rightTerm

		#we convert the vector to dense format in order to get the indices of 
      #the movies with the best estimated ratings 
		estimatedRatings[userTest, :] = prod.todense()
		recom = (-estimatedRatings[userTest, :]).argsort()
		for item in recom:
			if item not in moviesSeen[userTest]:
				dsTest[userTest].append(item)
				if len(dsTest[userTest]) == topN:
					break

	return dsTest




def PM(userVector,GroupByCategory,GroupByMovies,topCategory):
    SeenCategory=dict()
    
    for i in range(1,len(userVector)):
        if(userVector[i]!=0):
            if(i in GroupByMovies):
                for category in GroupByMovies[i]:
                    try:
                        SeenCategory[category].append(i)
                    except:
                        SeenCategory[category]=list()
                        SeenCategory[category].append(i)
    
    l=dict()
    for j in SeenCategory.keys():
        l[j]=int(len(SeenCategory[j]))

    lsort= sorted(l,key=l.get,reverse=True)[:topCategory]    
    listMovies=list()
    for i in lsort:
        for j in GroupByCategory[i]:
            if j not in listMovies:
                listMovies.append(j)    
    
    return listMovies[:100];


        

#################################################################
#
#               Knn
#
######################################################

#danh sach cac item ma user da danh gia
def List_Rating(urm, user):
    result=list()
    (rows,columns)=np.shape(urm)
    for i in range(1, columns):
        if(urm[user][i]!=0):
            result.append(i)
    return result
        

def pearson_correlation(urm, user1, user2):
    (rows,columns)=np.shape(urm)
    data_user1=List_Rating(urm,user1)
    data_user2=List_Rating(urm,user2)
    
    rating_avg_user1=sum(data_user1) / len(data_user1) 
    rating_avg_user2=sum(data_user2) / len(data_user2) 
    common=set.intersection(*[set(data_user1), set(data_user2)])
    tongTu=0
    
    tongUser1=0
    tongUser2=0
    for i in common:        
        tongTu=tongTu+(urm[user1][i]-rating_avg_user1)*(urm[user2][i]-rating_avg_user2)
        tongUser1=tongUser1+mt.pow(urm[user1][i]-rating_avg_user1,2)
        tongUser2=tongUser2+mt.pow(urm[user2][i]-rating_avg_user2,2)
    sqrt_User1=float(mt.sqrt(tongUser1))
    sqrt_User2=float(mt.sqrt(tongUser2))
    tongMau=sqrt_User1*sqrt_User2
    if(tongMau==0):
        return 0
    return float(tongTu/tongMau)

#lay k user_neighbor lien quan voi user
def k_nearest_neighbors(urm,user,k):
    neighbors=list()
    result=list()
    (users,items)=np.shape(urm)
    for user_id in range(users):
        if(user_id==user or user_id==0):
            continue
        upc=pearson_correlation(urm,user,user_id)
        neighbors.append([user_id,upc])####cau truc tra ve
    sorted_neighbors = sorted(neighbors, key=lambda neighbor: neighbor[1], reverse=True) 

    for i in range(k):
        if i >= len(sorted_neighbors):
            break
        result.append(sorted_neighbors[i])
    return result

def check_neighbors_validattion(urm, item, k_nearest_neighbors):
    result = []
    for neighbor in k_nearest_neighbors:
        neighbor_user_id = neighbor[0]
        #ds item user danh gia
        list_user_rating =List_Rating(urm,neighbor_user_id);
        if item in list_user_rating:
            result.append(neighbor)
    return result

#du doan chi so item phu hop voi user
def predict(urm, user, item, k_nearest_neighbors):
    valid_neighbors = check_neighbors_validattion(urm,item, k_nearest_neighbors)
    if not len(valid_neighbors):
        return 0.0
    top_result = 0.0
    bottom_result = 0.0
    for neighbor in valid_neighbors:
        neighbor_user_id = neighbor[0]
        neighbor_similarity = neighbor[1]   # Wi1
        rating = urm[neighbor_user_id][item] # rating i,item
        top_result += neighbor_similarity * rating
        bottom_result += neighbor_similarity
    result = top_result/bottom_result
    return result


def recommendKNN_UB(urm,user,k,N):
    user_neighbors=k_nearest_neighbors(urm,user,k) #user-độ liên quan

    result=list()
    #lay danh sach item chung
    dsitem=list()
    for user_item in user_neighbors:
        list_user_rating =List_Rating(urm,user_item[0]);
        dsitem=set.union(*[set(dsitem), set(list_user_rating)])
    
    listupc=list()
    for item in dsitem:
        upc=predict(urm,user,item,user_neighbors)
        listupc.append([item,upc])
    sorted_neighbors = sorted(listupc, key=lambda res: res[1], reverse=True) 
    for i in range(N):
        if i >= len(sorted_neighbors):
            break
        result.append(sorted_neighbors[i][0])
    return result

#############################################################
#
#
#
##############################################################
