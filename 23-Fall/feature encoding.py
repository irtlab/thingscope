import pandas as pd
import os
from data import get_file
from operator import itemgetter
from collections import defaultdict
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest, f_classif, chi2
from sklearn.feature_selection import mutual_info_regression, mutual_info_classif
from sklearn.decomposition import PCA
from scipy import stats
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from feature_selection import feature_selection, embedded_method,information_gain
import vaex as vx
import vaex.ml
from vaex.ml.sklearn import Predictor
from sklearn.metrics import classification_report
from vaex.ml.xgboost import XGBoostModel
from sklearn.preprocessing import LabelEncoder
import category_encoders as ce
def one_hot(df,feature_name):
    df=pd.concat([df,pd.get_dummies(df[feature_name],drop_first=True)],axis=1)
    return df
def label_encode(df,feature_name):
    le=LabelEncoder()
    df[feature_name]=le.fit_transform(df[feature_name])
    return df
def fequency_encode(df,feature_name):
    frequency=df[feature_name].value_counts(normalize=True).to_dict()
    df[feature_name] = df[feature_name].map(frequency)
    return df

def target_encode(df,feature_name):
    X=df[feature_name]
    y=df['label']
    y = y.astype(str)  # convert to string to onehot encode
    enc = ce.OneHotEncoder().fit(y)
    y_onehot = enc.transform(y)
    class_names = y_onehot.columns  # names of onehot encoded columns
    for class_ in class_names:
        enc = ce.TargetEncoder()
        enc.fit(X, y_onehot[class_])  # convert all categorical
        temp = enc.transform(X)  # columns for class_
        temp.columns = [str(x) + '_' + str(class_) for x in temp.columns]
        df = pd.concat([df, temp], axis=1)  # add to original dataset

    return df
def split_text(df,feature_name,delimiter):
    for f in feature_name:
        columns = []
        lens = len(df[f].str.split(delimiter, expand=True).columns)
        print(lens)
        for i in range(lens):
            columns.append(str(f)+str(i))
            print(columns)
        df[columns] = df[f].str.split(delimiter, expand=True)
    print(df[columns])
    return df

