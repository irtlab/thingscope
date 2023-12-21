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
from sklearn.ensemble import AdaBoostClassifier
from feature_encoding import label_encode,target_encode
from vaex.ml.catboost import CatBoostModel
from imblearn.over_sampling import SMOTE, ADASYN,SMOTENC
from imblearn.combine import SMOTETomek,SMOTEENN
from sklearn import metrics
from sklearn.ensemble import BaggingClassifier
from imblearn.ensemble import BalancedBaggingClassifier
from imblearn.ensemble import BalancedRandomForestClassifier
from imblearn.pipeline import Pipeline
import vaex.ml.tensorflow
import keras as K
from keras.models import Sequential
from keras.layers import *
from sklearn.preprocessing import LabelBinarizer
from sklearn.ensemble import AdaBoostClassifier
from sklearn.utils import class_weight
from sklearn import preprocessing
from sklearn import tree
from imbens.ensemble import *
from sklearn.ensemble import HistGradientBoostingClassifier
import vaex.ml
import vaex.ml.lightgbm
import lightgbm as lgb
import xgboost as xgb
def random_forest(x_train,x_test,features,target):
    x_train = vx.from_pandas(df=x_train, copy_index=True)
    x_test = vx.from_pandas(df=x_test, copy_index=True)
    clf = RandomForestClassifier(max_depth=20, random_state=0, class_weight='balanced')
    vaex_model = Predictor(features=features, target=target, model=clf, prediction_name='pred')
    vaex_model.fit(df=x_train)
    x_test = vaex_model.transform(x_test)
    return x_train,x_test
def cnn(x_train,x_test,features,dict_weights):
    x_train = vx.from_pandas(df=x_train, copy_index=True)
    x_test = vx.from_pandas(df=x_test, copy_index=True)
    print(x_train)
    x_train = x_train.ml.minmax_scaler(features=features)
    state_prep = x_train.state_get()
    x_test.state_set(state_prep)
    features = x_train.get_column_names(regex='^minmax_')
    print(x_train[ features])
    lb = LabelBinarizer()
    lb.fit(range(31))
    X_train=x_train[ features].values
    X_test=x_test[features].values
    y_train = lb.transform(x_train['label'].values)
    y_test = lb.transform(x_test['label'].values)
    model = Sequential()
    model.add(Input(shape=(len(features),)))
    model.add(Reshape((9,9,1)))
    model.add(Conv2D(32, kernel_size=(2,2),padding='same',strides=1, activation='relu', input_shape=(9, 9, 1)))
    model.add(MaxPool2D(pool_size=(1,1), strides=1))
    model.add(Conv2D(32, kernel_size=(2,2),padding='same',strides=1, activation='relu'))
    model.add(MaxPool2D(pool_size=(1,1), strides=1))
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dense(31, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    history=model.fit(x=X_train,y=y_train,validation_data= [X_test,y_test], epochs=150,batch_size=1024,
                      steps_per_epoch=X_train.shape[0]//1024,
                      validation_steps=X_test.shape[0]//1024,class_weight=dict_weights)
    model.summary()
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.tight_layout()
    plt.show()

    keras_model = vaex.ml.tensorflow.KerasModel(features=features, prediction_name='pred', model=model)
    x_train = keras_model.transform(x_train)
    state = x_train.state_get()
    x_test.state_set(state)
    pred=np.vstack(x_test['pred'].values)
    x_test['pred']=np.argmax(pred,axis=1)
    return x_train,x_test


def resampling(x_train,x_test,features,target,method,clf):
    x_train = vx.from_pandas(df=x_train, copy_index=True)
    x_test = vx.from_pandas(df=x_test, copy_index=True)
    pipeline = Pipeline([('sampler',method),('classification', clf)])
    vaex_model = Predictor(features=features, target=target, model=pipeline, prediction_name='pred')
    vaex_model.fit(df=x_train)
    x_test = vaex_model.transform(x_test)
    return x_train,x_test

def ensemble(x_train,x_test,features,target,clf):
    x_train = vx.from_pandas(df=x_train, copy_index=True)
    x_test = vx.from_pandas(df=x_test, copy_index=True)
    clf = BaggingClassifier(estimator=clf, n_estimators=31,
                            random_state=0)
    vaex_model = Predictor(features=features, target=target, model=clf, prediction_name='pred')
    vaex_model.fit(df=x_train)
    x_test = vaex_model.transform(x_test)
    return x_train, x_test

def xgboost(x_train,x_test,features,target,dict_weights):
    x_train = vx.from_pandas(df=x_train, copy_index=True)
    x_test = vx.from_pandas(df=x_test, copy_index=True)
    params = {'learning_rate': 0.1,
              'max_depth': 50,
              'num_class': 31,
              'objective': 'multi:softmax',
              'subsample': 1,
              'random_state': 42,
              'n_jobs': -1,
              'class_weight': dict_weights
              }
    booster = XGBoostModel(features=features, target=target, num_boost_round=500, params=params)
    booster.fit(df=x_train, evals=[(x_train, 'train'), (x_test, 'test')],verbose_eval=True, early_stopping_rounds=5)

    x_test = booster.transform(x_train)
    return x_train,x_test

def catboost(x_train,x_test,features,target,dict_weights):
    x_train = vx.from_pandas(df=x_train, copy_index=True)
    x_test = vx.from_pandas(df=x_test, copy_index=True)
    params = {
        'leaf_estimation_method': 'Gradient',
        'learning_rate': 1e-4,
        'max_depth': 20,
        'bootstrap_type': 'Bernoulli',
        'subsample': 0.8,
        'sampling_frequency': 'PerTree',
        'colsample_bylevel': 0.8,
        'reg_lambda': 1,
        'objective': 'MultiClass',
        'eval_metric': 'MultiClass',
        'random_state': 42,
        'verbose': 0,
        'class_weight': dict_weights}

    booster = CatBoostModel(features=features, target=target, num_boost_round=100,
                            params=params, prediction_type='Class', batch_size=11_000_000)
    booster.fit(df=x_train, progress='widget')

    x_test = booster.transform(x_test)
    return x_train,x_test

def lightgbm(x_train,x_test,features,target,dict_weights):
    X_train=x_train[features]
    X_test = x_test[features]
    y_train=x_train[target]
    y_test=x_test[target]
    lgb_train = lgb.Dataset(X_train, y_train)
    lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)
    params = {
        'boosting': 'gbdt',
        'max_depth': 30,
        'learning_rate': 0.01,
        'application': 'multiclass',
        'num_class': 31,
        'subsample': 1,
        'colsample_bytree': 0.8,
        'num_leaves':30,
        'verbose':1
    }
    gbm = lgb.train(params,
                    lgb_train,
                    num_boost_round=500,
                    valid_sets=lgb_eval)
    y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
    x_test['pred']=np.argmax(y_pred,axis=1)
    return x_train,x_test

def adaboost(x_train,x_test,features,target,dict_weights):
    x_train = vx.from_pandas(df=x_train, copy_index=True)
    x_test = vx.from_pandas(df=x_test, copy_index=True)
    clf = tree.DecisionTreeClassifier(max_depth=50,class_weight=dict_weights)
    clf = AdaBoostClassifier(estimator= clf,n_estimators=100, random_state=0,learning_rate=1)

    vaex_model = Predictor(features=features, target=target, model=clf, prediction_name='pred')
    vaex_model.fit(df=x_train)
    x_test = vaex_model.transform(x_test)
    return x_train, x_test

def overBoostClassifier(x_train,x_test,features,target,dict_weights):
    x_train = vx.from_pandas(df=x_train, copy_index=True)
    x_test = vx.from_pandas(df=x_test, copy_index=True)
    # clf= tree.DecisionTreeClassifier(max_depth=50,class_weight=dict_weights)
    clf = HistGradientBoostingClassifier(max_iter=500, max_depth=20, class_weight=dict_weights,learning_rate=1e-2, random_state = 0)
    # clf =SMOTEBoostClassifier(estimator=clf,n_estimators=20,learning_rate=1e-2,random_state=0)
    vaex_model = Predictor(features=features, target=target, model=clf, prediction_name='pred')
    vaex_model.fit(df=x_train)
    x_test = vaex_model.transform(x_test)
    return x_train,x_test