import pandas as pd
import os
from data import get_file
import numpy as np
from operator import itemgetter
from collections import defaultdict
import pickle
label=[]
labels=[]
filenames=[]
root,dir,filename=get_file("D:/graduate/COMS6901/code/UNSW(1)/UNSW_csv")
root=str(root[0])
class OurDict(dict):
    def __missing__(self, key):
        return None
for f in filename[0]:
    filenames.append(os.path.join(root,f))
df=pd.read_excel('D:/graduate/COMS6901/code/UNSW/UNSW List_Of_Devices.xlsx')
device_list=pd.DataFrame(df.iloc[:,0:2])

device_list=device_list.set_index(['MAC ADDRESS'])['List of Devices'].to_dict()
device_list=OurDict(device_list)
print(device_list)
f_save = open('UNSW_device.pkl', 'wb')
pickle.dump(device_list, f_save)
f_save.close()

index=range(len(device_list))
device=list(device_list.values())
label_map=dict(zip(device,index))
label_map[None]=31
f_save = open('UNSW_label_map.pkl', 'wb')
pickle.dump(label_map, f_save)
f_save.close()
print(label_map)
def Label(df):
    if df['%dir']=='A':
        return df['srcMac']
    if df['%dir']=='B':
        return df['dstMac']
for f in filenames:
    df=pd.read_csv(f,low_memory=False)
    df.loc[:, 'label'] = df.apply(Label,axis=1)
    df.loc[:, 'label'] =df['label'].map(lambda x: label_map[device_list[x]])
    y=df['label'].to_numpy()
    labels.append(y)
print(labels)
f_save = open('UNSW_label.pkl', 'wb')
pickle.dump(labels, f_save)
f_save.close()
print(labels)








