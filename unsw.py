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
from model import *
from sklearn.model_selection import train_test_split
from feature_selection import feature_selection, embedded_method,information_gain
import vaex as vx
import vaex.ml
from vaex.ml.sklearn import Predictor
from sklearn.metrics import classification_report
from vaex.ml.xgboost import XGBoostModel
from sklearn.preprocessing import LabelEncoder
from feature_encoding import label_encode
from operator import itemgetter
vx.multithreading.thread_count_default = 8
# unsw data
filenames = []
f = open('UNSW_label.pkl', 'rb')
labels = pickle.load(f)
f.close()
root, dir, filename = get_file("D:/graduate/COMS6901/code/UNSW/Processed_data")
root = str(root[0])


# def flatten_extend(matrix):
#     flat_list = []
#     for row in matrix:
#         flat_list.append(row)
#     return flat_list


# with open('y_train.npy', 'wb') as f:
#     np.save(f,y_train)
# with open('y_test.npy', 'wb') as f:
#     np.save(f,y_test)
for f in filename[0]:
    filenames.append(os.path.join(root, f))
df = []
data = filenames
hex_features = ['flowStat', 'tcpFStat', 'ipToS', 'ipFlags', 'ethType',
                 'tcpStatesAFlags', 'icmpStat', 'icmpTmGtw', 'macStat','tcpAnomaly',
                'tcpFlags',  'tcpMPF', 'tcpMPTBF', 'tcpMPDSSF', 'tcpOptions']
string_features = ['%dir']
catergorial_feature=['map_IpCountry', "map_IpOrg"]+hex_features+string_features
not_used_features = ['timeFirst', 'timeLast', 'srcPort', 'dstIP',
                       'dstMac', 'srcIP', 'srcMac', 'srcMac_dstMac_numP','ipOptCpCl_Num',
                     'icmpBFTypH_TypL_Code', 'ip6OptHH_D', 'ip6OptCntHH_D']
feature_name = ['dstPort', 'minPktSz', 'avePktSize', 'bytAsm', 'ipMinTTL', 'ipMaxTTL',
                'tcpInitWinSz', 'tcpMinWinSz', 'tcpRTTAckTripMin']

new_feature = ['Number_of_endpoints',
               'Num_of_ntp_endpoints_countries',
               'Num_of_endpoints_countries',
               'map_IpOrg',
               'Number_of_ntp_endpoints',
               'map_IpCountry'
                ]
for f in data:
    d = pd.read_csv(f, low_memory=False)
    d['protocolClassN'] = d.apply(
        lambda row: row['dstPortClassN'] if row['dstPortClass'] != 'unknown' else row['l4Proto'], axis=1)
    d['map_IpCountry'] =d.apply(lambda row: row['dstIPCC'] if row['%dir'] == 'A' else row['srcIPCC'], axis=1)
    d['map_IpOrg'] = d.apply(lambda row: row['dstIPOrg'] if row['%dir'] == 'A' else row['srcIPOrg'], axis=1)
    d=d[d['label']!=7]
    d=d[d['label']!=22]
    d = d.drop(not_used_features, axis=1)
    d= label_encode(d,catergorial_feature)
    df.append(d)
data = pd.concat(df)
print(data['dstPort'])
train_data, test_data= train_test_split(
    df, test_size=0.2, random_state=0)
train_data=pd.concat(train_data)
test_data=pd.concat(test_data)
print(train_data['dstPort'])

data=data[data.T[data.dtypes!=object].index]
data=pd.DataFrame.dropna(data,axis=1,how='any')
information_gain(data,data['label'],catergorial_feature)
data=data.loc[:,(data!= 0).any(axis=0)]
data.drop(data.columns[data.std()<0.01], axis=1, inplace=True)
x_indices =list(data.columns)
x_indices.remove('label')
x_indices.remove('dstPortClassN')
# x_indices.remove('flowInd')
# x_indices.remove('%dir')
# x_indices= [i for i in x_indices if i not in new_feature ]
# print(x_indices)
# feature selection

# feature_name=feature_selection(data,data['label'],x_indices)
# feature_name=embedded_method(data,data['label'],feature_name)
# # feature_name=embedded_method(data,y,feature_name)
feature_name = ['avePktSize',
                'maxPktSz',
                'minPktSz',
                'maxIAT',
                'connNumBCnt',
                'tcpRTTAckTripMin',
                'dstPort',
                'ipMinTTL',
                'ipMaxTTL',
                'stdPktSize'
                ]

x_train = train_data[feature_name+new_feature+['label']]
x_test = test_data[feature_name+new_feature+['label']]
print(feature_name)
f = open('UNSW_label_map.pkl', 'rb')
device = pickle.load(f)
f.close()
classes=list(device.values())[:22]
classes.remove(7)
print(classes)
device=list(device.keys())[:24]
device.remove('Samsung Galaxy Tab')
device.remove('Nest Dropcam')
device[7]='unknown'
device.remove('unknown')
print(device)
class_weights = class_weight.compute_class_weight(class_weight='balanced',classes=classes,y= data['label'])
norm_class_weights= data['label'].value_counts(normalize=True).to_dict()
n=list(norm_class_weights.keys())
print(norm_class_weights)
dict_weights=dict(zip(classes,class_weights))
num_dict=dict(zip(classes,device))
sorted_device=list(itemgetter(*n)(num_dict))
print(sorted_device)
plt.Figure(figsize=( 100,50),dpi=150)
plt.pie(list(norm_class_weights.values()),radius=1,textprops={'size': 7}, autopct='%1.1f%%', pctdistance=0.6,labels=sorted_device)
plt.legend(loc='center left',prop = {'size':5}, bbox_to_anchor=(1.10, 0.5))
plt.title('UNSW dataset distribution')
plt.tight_layout()
plt.show()
# # machine learning
# # random forest
#

features = feature_name
features = feature_name+new_feature
target='label'
x_train,x_test=xgboost(x_train,x_test,features,target,dict_weights)

print(classification_report(x_test['label'].values, x_test['xgboost_prediction'].values,labels=classes,target_names=device))
