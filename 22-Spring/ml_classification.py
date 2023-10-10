from unittest import result
import joblib
from collections import Counter
import json
from sklearn import metrics
from sklearn.preprocessing import StandardScaler


def predict(flow_file):
    # load std scaler used to normlized the data before training the model 
    loaded_std_scaler = joblib.load("./std_scaler.bin")
    X_test = loaded_std_scaler.transform(flow_file)
    # load trained RF model
    loaded_rf = joblib.load("./random_forest.joblib")
    y_pred = loaded_rf.predict(X_test)
    result = Counter(y_pred).most_common()
    res = [list(ele) for ele in result]
    print("***** Device Classification Random Forest: ",print_result(res),"*****") 
    # load trained KNN model
    loaded_knn = joblib.load("./KNeighborsClassifier.joblib")
    y2_pred = loaded_knn.predict(X_test)
    result2 = Counter(y2_pred).most_common()
    res2 = [list(ele) for ele in result2]
    print("***** Device Classification KNN: ",print_result(res2),"*****")


## Print device type/name ## 
def print_result(res):
    f = open('device_label.json')
    data = json.load(f)
    dataList =  data['lables']
    # loop through json file to find the device name
    for i in res:
        for index in range(len(data['lables'])):
            if (i[0] == index):
                for key in dataList[index]:
                    i[0]= dataList[index][key]
        if (i[0] == 20):
            i[0]= "amazon Echo"
    return res

    
