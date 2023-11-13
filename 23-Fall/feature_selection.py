import pandas as pd
import os
from data import get_file
from operator import itemgetter
from collections import defaultdict
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest, f_classif,chi2
from sklearn.feature_selection import mutual_info_regression, mutual_info_classif
from sklearn.decomposition import PCA
from scipy import stats
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import chi2
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
def feature_selection(train_data,y_train,X_indices):
    x_train=np.array(train_data[X_indices].values)
    correlation=np.corrcoef(x_train.T)
    c=pd.DataFrame(correlation,index=X_indices,columns=X_indices)
    sns.heatmap(c)
    plt.title('Pairwise Correlation')
    plt.show()
    importances=[]
    for i in range(len(x_train.T)):
        corr=np.corrcoef(x_train.T[i],y_train.T)[0,1]
        importances.append(corr)
    
    plt.figure(figsize=(15,13))
    plt.title('Features correlation with target')
    plt.barh(range(len(X_indices)), importances, color='g', align='center')
    plt.yticks(range(len(X_indices)), [i for i in X_indices])
    plt.xlabel('Relative Importance')
    plt.show()
    importances=np.array(importances)
    important_index=np.where([importances>0.1])[1]
    for i in important_index:
        for j in important_index:
            if i!=j:
                correlations = np.corrcoef(x_train.T[i],x_train.T[j])[0,1]
                if correlations>0.6:
                    np.delete(important_index, np.where(important_index==j))
    feature_name=[X_indices[important_index[i]] for i in range(len(important_index))]
    x_train=train_data[feature_name]
    mi = mutual_info_classif(x_train,y_train)
    mi = pd.Series(mi)
    mi.index = x_train.columns
    idx=mi[mi>0.5]
    feature_name=idx.index
    mi.sort_values(ascending=False)
    mi.sort_values(ascending=False).plot.bar(figsize=(10, 5))
    plt.show()
    return feature_name

def embedded_method(train_data,y_train,X_indices):
    x_train=train_data[X_indices].values
    clf = ExtraTreesClassifier(n_estimators=50)
    clf = clf.fit(x_train, y_train)
    score=clf.feature_importances_
    model = SelectFromModel(clf, prefit=True)
    X_new = model.transform(x_train)
    feature_name=model.get_feature_names_out(input_features=X_indices)
    print(feature_name)
    plt.Figure(figsize=(20,5))
    plt.bar(np.array(X_indices),score)
    plt.xticks(rotation=-90)
    plt.show()
    return feature_name

def information_gain(train_data,y_train,X_indices):
    x_train=train_data.values
    mi = mutual_info_classif(x_train,y_train)
    mi = pd.Series(mi)
    mi.index =X_indices
    mi.sort_values(ascending=False)
    mi.sort_values(ascending=False).plot.bar(figsize=(10, 5))
    plt.show()