import sys
import os
sys.path.append(os.path.join(os.path.dirname("ReadFile"),'.'))
sys.path.append(os.path.join(os.path.dirname("Function"),'.'))
sys.path.append(os.path.join(os.path.dirname("dadang"),'.'))
sys.path.append(os.path.join(os.path.dirname("batngo"),'.'))
sys.path.append(os.path.join(os.path.dirname("tinhmoi"),'.'))
sys.path.append(os.path.join(os.path.dirname("recall"),'.'))
sys.path.append(os.path.join(os.path.dirname("contentbase"),'.'))
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import cross_validate
import numpy as np
import math
import ReadFile
import Function
import dadang
import tinhmoi
import batngo
import recall
import contentbase
MAX_IID = 1683
MAX_UID = 944


 
# -*- coding: utf-8 -*-
if __name__ == '__main__':
    K = 30                           #rank cua ma tran s
    topN=10
    topC=50
    user=1                          #gio y cho user 1
    loaiDadang=0;
    alpha=0.5                       #can bang da dang voi rel
    standardMetric=0.8              #
    kUser=5                         #k_nearest_neighbors 
#   đường dẫn    
    baseFile = 'D:/danthanh/DoAnTotNghiep/datasets/ml-100k/ua.base'
    itemFile = 'D:/danthanh/DoAnTotNghiep/datasets/ml-100k/u.item'
    userFile='D:/danthanh/DoAnTotNghiep/datasets/ml-100k/u.user'
#   
#    #khoi tao listitem, va ma tran danh gia
    listItem=ReadFile.getItem(itemFile);
    listUser=ReadFile.getUser(userFile);
    urm=ReadFile.UserRatingMatrix("D:/danthanh/DoAnTotNghiep/datasets/ml-100k/u1.base",MAX_UID,MAX_IID)
    urmTest=ReadFile.UserRatingMatrix("D:/danthanh/DoAnTotNghiep/datasets/ml-100k/u1.test",MAX_UID,MAX_IID)
    uTest=ReadFile.GetListUSerTest("D:/danthanh/DoAnTotNghiep/datasets/ml-100k/u1.test")
    gMS=ReadFile.getMoviesSeen("D:/danthanh/DoAnTotNghiep/datasets/ml-100k/u1.base")
    GroupByCategory,GroupByMovies=ReadFile.getMovies_Genres(itemFile)


############################### MF   #####################################
    #    Hệ thống cũ MF
    U, S, Vt = Function.computeSVD(urm, K)  
    A=U*S*Vt
    listRecommedOld = Function.MF(U, S, Vt, uTest, gMS,topN,MAX_UID,MAX_IID)
#    fullRecommedMF=listRecommedOld
#    print (fullRecommedMF)
    userRecommedMF=listRecommedOld[user];
    print ('Danh sach goi y cu bang MF:')
    print('################################################');
    print (userRecommedMF)
    
     #Re call
    relItem=recall.relItem(urmTest,user)
    recall=recall.Recall(userRecommedMF,relItem)
    print ("\nRecall: ",recall)
   
    
    #DA DANG
    print("\nDa dang")
    dadangprev=dadang.Diversity(urm,None,userRecommedMF,loaiDadang)
    print ("Do da dang truoc khi tang",dadangprev)
    listRel=dadang.vectorRel(urm,userRecommedMF,user)
    listRecommedNewDiversity=dadang.IncreasingDiversity(urm,None,user,userRecommedMF,listRel,topN,alpha,loaiDadang);
    dd=dadang.Diversity(urm,None,listRecommedNewDiversity,loaiDadang)
    print ("Danh sach goi y khi tang da dang:",listRecommedNewDiversity)
    print("Do da dang sau khi tang",dd)
    
    #TINH MOI
    print("\nTinh moi")
    novelty=tinhmoi.Novelty(userRecommedMF,urm)
    print("Tinh moi truoc khi tang",novelty)
    listRecommedNewNovelty=tinhmoi.IncreasingNoveltyNhanh(urm,listItem,listUser,topN);
    novelty=tinhmoi.Novelty(listRecommedNewNovelty,urm)
    print ("Danh sach goi y khi tang tinh moi:",listRecommedNewNovelty)
    print("Tinh moi sau khi tang",novelty)
    
    #TINH BAT NGO
    print("\nTinh bat ngo");
    Reu=batngo.Eu(urm[user],listItem,GroupByMovies,standardMetric);
    Runexp=batngo.RUnexp(userRecommedMF,Reu)
    Ruseful=batngo.RUsefull(urm,userRecommedMF,MAX_UID,MAX_IID)
    SRDPT=batngo.Serendipity(userRecommedMF,Runexp,Ruseful)
    print ("Do bat ngoi truoc khi tang la: ",SRDPT)

    print("#######################################");
#########################################################################
#########################################################################
#########################################################################
#####################       user-base UB   ############################
    #goi y he thong cu bang user-base UB
    userRecommedKNN_UB=Function.recommendKNN_UB(urm,user,kUser,topN)
    print('################################################');
    print ('Danh sach gio y cu bang KNN-UB:')
    print(userRecommedKNN_UB)

    #DA DANG
    print("\nDa dang")
    dadangprev=dadang.Diversity(urm,None,userRecommedKNN_UB,loaiDadang)
    print ("Do da dang truoc khi tang",dadangprev)
    listRel=dadang.vectorRel(urm,userRecommedKNN_UB,user)
    listRecommedNewDiversity=dadang.IncreasingDiversity(urm,None,user,userRecommedKNN_UB,listRel,topN,alpha,loaiDadang);
    dd=dadang.Diversity(urm,None,listRecommedNewDiversity,loaiDadang)
    print ("Danh sach goi y khi tang da dang: ",listRecommedNewDiversity)
    print("Do da dang sau khi tang",dd)
    
    #TINH MOI
    print("\nTinh moi")
    novelty=tinhmoi.Novelty(userRecommedKNN_UB,urm)
    print("Tinh moi truoc khi tang",novelty)
    listRecommedNewNovelty=tinhmoi.IncreasingNoveltyNhanh(urm,listItem,listUser,topN);
    novelty=tinhmoi.Novelty(listRecommedNewNovelty,urm)
    print ("Danh sach goi y khi tang tinh moi:",listRecommedNewNovelty)
    print("tinh moi sau khi tang",novelty)
    
    #TINH BAT NGOI
    print("\nTinh bat ngo");
    Reu=batngo.Eu(urm[user],listItem,GroupByMovies,standardMetric);
    Runexp=batngo.RUnexp(userRecommedKNN_UB,Reu)
    Ruseful=batngo.RUsefull(urm,userRecommedKNN_UB,MAX_UID,MAX_IID)
    SRDPT=batngo.Serendipity(userRecommedKNN_UB,Runexp,Ruseful)
    print ("Do bat ngoi truoc khi tang la: ",SRDPT)

    print("#######################################");
#####################       Content-base   ############################
#goi y he thong cu bang Content-base
    userRecommed_ContentBase=contentbase.recommend_ContentBase(user,topN, baseFile, itemFile, userFile)
    print('################################################');
    print ('Danh sach gio y cu bang Content-based:')
    print(userRecommed_ContentBase)

    #DA DANG
    print("\nDa dang")
    dadangprev=dadang.Diversity(urm,None,userRecommed_ContentBase,loaiDadang)
    print ("Do da dang truoc khi tang",dadangprev)
    listRel=dadang.vectorRel(urm,userRecommed_ContentBase,user)
    listRecommedNewDiversity=dadang.IncreasingDiversity(urm,None,user,userRecommed_ContentBase,listRel,topN,alpha,loaiDadang);
    dd=dadang.Diversity(urm,None,listRecommedNewDiversity,loaiDadang)
    print ("Danh sach goi y khi tang da dang: ",listRecommedNewDiversity)
    print("Do da dang sau khi tang",dd)
    
    #TINH MOI
    print("\nTinh moi")
    novelty=tinhmoi.Novelty(userRecommed_ContentBase,urm)
    print("Tinh moi truoc khi tang",novelty)
    listRecommedNewNovelty=tinhmoi.IncreasingNoveltyNhanh(urm,listItem,listUser,topN);
    novelty=tinhmoi.Novelty(listRecommedNewNovelty,urm)
    print ("Danh sach goi y khi tang tinh moi:",listRecommedNewNovelty)
    print("tinh moi sau khi tang",novelty)
    
    #TINH BAT NGOI
    print("\nTinh bat ngo");
    Reu=batngo.Eu(urm[user],listItem,GroupByMovies,standardMetric);
    Runexp=batngo.RUnexp(userRecommed_ContentBase,Reu)
    Ruseful=batngo.RUsefull(urm,userRecommed_ContentBase,MAX_UID,MAX_IID)
    SRDPT=batngo.Serendipity(userRecommed_ContentBase,Runexp,Ruseful)
    print ("Do bat ngoi truoc khi tang la: ",SRDPT)
#       Ket thuc #/////////////////////////////
#############################################################
    