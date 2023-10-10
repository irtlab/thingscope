### Import Tranalyzer and convert pcap to flow.csv

import imp
from ml_classification import predict
from t2py import T2Utils
import pandas as pd
import os
import ml_classification


cwd = os.getcwd()

## Final feature vector obtained after implementing the feature selection methods ##
features = [
'connDip',
'connSip',
'minPktSz',
'duration',
'pktAsm',
'tcpRTTAckTripMax'
]

## Convert PCAP file to flow file using Tranalyzer and call ml_classification ##
def convert_pcap(pcap_path):
    pcap_path2 = cwd +"/"+  pcap_path
    T2Utils.run_tranalyzer(
        pcap= pcap_path2,
        output_prefix= cwd ,
        plugins=['protoStats', 'basicFlow', 'macRecorder', 'portClassifier','basicStats',
         'tcpFlags','tcpStates','icmpDecode','connStat','txtSink'],
         packet_mode=True
    )
    file_name = os.path.splitext(pcap_path)[0]
    path = cwd +"/"+ file_name + "_flows.txt"
    # Convert flow text to csv file
    read_file = pd.read_csv(path, index_col=None, header=0, delimiter='\t')
    read_file.to_csv(file_name+".csv",index=None)
    flow_file = cwd +"/"+ file_name + ".csv"
    flow_file2 = pd.read_csv(flow_file)
    flow_file3 = flow_file2[features]
    # Call predict function to predict the device name based on the flows 
    ml_classification.predict(flow_file3)