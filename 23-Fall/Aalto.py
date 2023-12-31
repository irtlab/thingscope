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
from sklearn.utils import class_weight
from sklearn import preprocessing
from model import *
f = open('Aalto_filename.pkl', 'rb')
filename = pickle.load(f)
f.close()
label=list(filename.keys())
labels=LabelEncoder().fit_transform(label)
print(labels)
root, dir, filename = get_file("D:/graduate/COMS6901/code/Aalto/flow_csv")
root.pop(-1)
print(filename)
df=[]
train=[]
test=[]
hex_features = ['flowStat', 'tcpFStat', 'ipToS', 'ipFlags', 'ethType',
                 'tcpStatesAFlags', 'icmpStat', 'icmpTmGtw', 'macStat','tcpAnomaly',
                'tcpFlags',  'tcpMPF', 'tcpMPTBF', 'tcpMPDSSF', 'tcpOptions']
string_features = ['%dir']
catergorial_feature=['map_IpCountry', "map_IpOrg"]+hex_features+string_features
not_used_features = ['timeFirst', 'timeLast','dstPort', 'srcPort', 'dstIP',
                      'dstMac', 'srcIP', 'srcMac', 'srcMac_dstMac_numP','ipOptCpCl_Num',
                     'icmpBFTypH_TypL_Code', 'ip6OptHH_D', 'ip6OptCntHH_D']

# catergorial_feature=["%dir","flowStat","hdrDesc","ethType","macStat","dstPortClass","srcIPCC",
#                     "srcIPOrg","dstIPCC","dstIPOrg", "ipOptCpCl_Num",
#                     "ip6OptCntHH_D", "ip6OptHH_D","ipToS",
#                     "icmpBFTypH_TypL_Code","icmpTmGtw"]
country_df = pd.read_csv('IPCC_to_number.csv', dtype={'Number': int})
org_df = pd.read_csv('IPOrg_to_number.csv', dtype={'Number': int})
# Convert DataFrame back to dictionary
country_list = country_df.set_index(['Country'])['Number'].to_dict()
org_list = org_df.set_index(['Org'])['Number'].to_dict()
df = []
for r,f,l in zip(root,filename,labels):
    data = []
    for p in f:
        path=os.path.join(r,p)
        d = pd.read_csv(path, low_memory=False)
        d = pd.DataFrame.dropna(d, axis=1, how='any')
        d = d.assign(label=l)
        d['protocolClassN'] = d.apply(lambda row: row['dstPortClassN'] if row['dstPortClass'] != 'unknown' else row['l4Proto'], axis=1)
        d['map_IpCountry'] = d.apply(lambda row: row['dstIPCC'] if row['%dir'] == 'A' else row['srcIPCC'], axis=1)
        d['map_IpOrg'] = d.apply(lambda row: row['dstIPOrg'] if row['%dir'] == 'A' else row['srcIPOrg'], axis=1)
        # d= label_encode(d,catergorial_feature)
        d=d.drop(not_used_features, axis=1)
        d = label_encode(d, catergorial_feature)
        data.append(d)
        df.append(d)
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
    train_data = pd.concat(train_data)
    test_data = pd.concat(test_data)
    train.append(train_data)
    test.append(test_data)
data=pd.concat(df)
train_data=pd.concat(train)
test_data=pd.concat(test)
information_gain(data,data['label'],catergorial_feature)
d=data
d=d[d.T[d.dtypes!=object].index]
d=pd.DataFrame.dropna(d,axis=1,how='any')
# d=d.loc[:,(d!= 0).any(axis=0)]
d.drop(d.columns[d.std()<0.01], axis=1, inplace=True)
x_indices=list(d.columns.values)
x_indices.remove('label')
x_indices.remove('flowInd')
x_indices.remove('%dir')
# x_indices.remove('dstPortClass')
x_indices.remove('dstPortClassN')
x_indices.remove('protocolClassN')
print('x',len(x_indices))
# information_gain(data,data['label'], catergorial_feature)

feature_name=feature_selection(data,data['label'],x_indices)
feature_name=embedded_method(data,data['label'],feature_name)
class_weights = class_weight.compute_class_weight(class_weight='balanced',classes=range(31),y= data['label'])
dict_weights=dict(zip(range(31),class_weights))

norm_class_weights= data['label'].value_counts(normalize=True).to_dict()
print(norm_class_weights)
n=list(norm_class_weights.keys())
num_dict=dict(zip(range(31),label))
sorted_device=list(itemgetter(*n)(num_dict))
device=sorted_device
print(sorted_device)
plt.Figure(figsize=( 100,50),dpi=150)
plt.pie(list(norm_class_weights.values()),labels=device,radius=1,textprops={'size': 7}, autopct='%1.1f%%', pctdistance=0.6)

plt.axis('equal')
plt.title('Aalto dataset distribution')
plt.tight_layout()
plt.show()

x_train = train_data[x_indices+['label']]
x_test = test_data[x_indices+['label']]
smote = SMOTE(random_state=0)

features = feature_name
target = 'label'
x_train,x_test=adaboost(x_train,x_test,features,target,dict_weights)

print(classification_report(x_test['label'].values, x_test['pred'].values, target_names=label))
