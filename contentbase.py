# -*- coding: utf-8 -*-
# Trích xuất dữ liệu
# xây dựng item profiles (feature vector cho mỗi item)
    # Load toàn bộ thông tin phim vào biến item
    #Xây dựng feature vector cho mỗi item (bộ phim')
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd 
import numpy as np
from sklearn.linear_model import Ridge
from sklearn import linear_model
import numpy;
def getFeatureVector(itemsFile):
     i_cols = ['movie id', 'movie title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
               'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
               'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
     items = pd.read_csv(itemsFile, sep='|', names=i_cols, encoding='latin-1')
     X0 = items.as_matrix()
     X_train_counts = X0[:, -19:]
     transformer = TfidfTransformer(smooth_idf=True, norm ='l2')
     tfidf = transformer.fit_transform(X_train_counts.tolist()).toarray()
     return tfidf

def getUser(userFiles):
    u_cols =  ['user_id', 'age', 'sex', 'occupation', 'zip_code']
    users = pd.read_csv(userFiles, sep='|', names=u_cols,encoding='latin-1')
    n_users = users.shape[0]
    return n_users

def getUser_Item(nameFile):
    r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
    ratings_base = pd.read_csv(nameFile, sep='\t', names=r_cols, encoding='latin-1')
    rate_train = ratings_base.as_matrix()
    return rate_train

def get_items_rated_by_user(rate_matrix, user_id):
    y = rate_matrix[:,0] # all users
    # item indices rated by user_id
    # we need to +1 to user_id since in the rate_matrix, id starts from 1 
    # while index in python starts from 0
    ids = np.where(y == user_id +1)[0] 
    item_ids = rate_matrix[ids, 1] - 1 # index starts from 0 
    scores = rate_matrix[ids, 2]
    return (item_ids, scores)
    
def getWandBias(tfidf,n_users,rate_train):
    d = tfidf.shape[1] # data dimension
    W = np.zeros((d, n_users))
    b = np.zeros((1, n_users))
    for n in range(n_users):    
        ids, scores = get_items_rated_by_user(rate_train, n)
        clf = Ridge(alpha=0.01, fit_intercept  = True)
        Xhat = tfidf[ids, :]
        
        clf.fit(Xhat, scores) 
        W[:, n] = clf.coef_
        b[0, n] = clf.intercept_
    Yhat = tfidf.dot(W) + b
    return Yhat
    # predicted scores

def recommend_ContentBase(user,topN, baseFile, itemFile, userFile):  
    #
    n_users=getUser(userFile)
    rate_train=getUser_Item(baseFile)
    tfidf=getFeatureVector(itemFile)
    Yhat =getWandBias(tfidf,n_users,rate_train)

    listObj= numpy.argsort(Yhat[user])[:topN]
    #listObj= sorted(Yhat[user],reverse=True)[:topN]
    print('Predicted ratings:', listObj)
    return listObj