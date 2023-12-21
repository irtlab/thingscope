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
    sns.heatmap(c, label =X_indices)
    plt.legend(labels=X_indices,loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title('Pairwise Correlation')
    plt.tight_layout()
    plt.show()
    importances=[]
    for i in range(len(x_train.T)):
        corr=np.corrcoef(x_train.T[i],y_train.T)[0,1]
        importances.append(corr)
    
    plt.figure(figsize=(15,13))
    im=dict(zip(X_indices,importances))
    im = dict(sorted(im .items(), key=lambda x: x[1]))
    r=list(im.keys())
    r.reverse()
    print(r)
    plt.barh(range(len(X_indices)),list(im.values()), color='g', align='center',label=r)
    plt.yticks(range(len(X_indices)), list(im.keys()))
    plt.xlabel('Relative Importance')
    plt.title('Features correlation with target',fontdict={'fontsize':8})
    plt.legend(loc='center left',prop = {'size':8},bbox_to_anchor=(1, 0.5))
    plt.show()
    importances=np.array(importances)
    important_index=np.where([importances>0])[1]
    for i in important_index:
        for j in important_index:
            if i!=j:
                correlations = np.corrcoef(x_train.T[i],x_train.T[j])[0,1]
                if correlations>0.4:
                    np.delete(important_index, np.where(important_index==j))
    feature_name=[X_indices[important_index[i]] for i in range(len(important_index))]
    x_train=train_data[feature_name]
    mi = mutual_info_classif(x_train,y_train)
    mi = pd.Series(mi,index=list(x_train.columns))
    mi.index = x_train.columns
    idx=mi[mi>0.4]
    feature_name=idx.index
    plt.Figure(figsize=(30, 10))
    mi=mi.sort_values(ascending=False)
    plt.bar(mi.index,mi.values,label=mi.index,color='y')
    plt.xticks(rotation=90)
    print(list(x_train.columns))
    plt.legend(loc='center left',prop = {'size':8},bbox_to_anchor=(1, 0.25))
    plt.xlabel('features')
    plt.ylabel('reduction in entropy')
    plt.title('information gain')
    plt.tight_layout()
    plt.show()
    return feature_name

def embedded_method(train_data,y_train,X_indices):
    x_train=train_data[X_indices].values
    clf = ExtraTreesClassifier(n_estimators=100)
    clf = clf.fit(x_train, y_train)
    score=clf.feature_importances_
    plt.Figure(figsize=(30,10))
    plt.xlabel('feature')
    plt.ylabel('reduction in impurity')
    sort_indice=dict(zip(X_indices,score))
    sort_indice = dict(sorted(sort_indice.items(), key=lambda x: x[1], reverse=True))
    plt.bar(list(sort_indice.keys()),list(sort_indice.values()),label=list(sort_indice.keys()))
    plt.xticks(rotation=90)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title('tree-based method scores')
    plt.tight_layout()
    plt.show()
    model = SelectFromModel(clf,threshold=0.04, prefit=True)
    X_new = model.fit_transform(x_train)
    feature_name=model.get_feature_names_out(X_indices)
    feature_name=list(feature_name)
    print(feature_name)

    return feature_name

def information_gain(train_data,y_train,X_indices):
    x_train=train_data[X_indices].values
    mi = mutual_info_classif(x_train,y_train)
    mi = pd.Series(mi)
    mi.index =X_indices
    plt.Figure(figsize=(30, 10))
    mi=mi.sort_values(ascending=False)
    plt.bar(mi.index,mi.values,label=mi.index,color='purple')
    plt.xlabel('features')
    plt.ylabel('reduction in entropy')
    plt.xticks(rotation=90)
    plt.legend(loc='center left',prop = {'size':8},bbox_to_anchor=(1, 0.25))
    plt.title('categorical features information gain')
    plt.tight_layout()
    plt.show()
