from t2py import T2Utils
import pandas as pd
import os
import pickle
def get_file(file_path):
    roots=[]
    pcap_file=[]
    files=[]
    for root, dirs, file in os.walk(file_path,topdown=False):
        files.append(file)
        filename=[f for f in file if (f.split('.')[-1])=='pcap']
        pcap_file.append(filename)
        roots.append(root)
    pcap_file.remove([])
    roots.pop(-1)
    #save filename
    dictionary = dict(zip(dirs, pcap_file))
    dict_2 = dict(sorted(dictionary.items(), key=lambda i: i[0]))
    f_save = open('filename.pkl', 'wb')
    pickle.dump(dict_2, f_save)
    f_save.close()
    return roots, dirs, pcap_file


def convert_pcap(roots,dirs,pcap_file):
    for root,path,files in zip(roots,dirs,pcap_file):
        for file in files:
            pcap_path=os.path.join(root,file)
            output ='/home/yfy/flows/'+str(path)+'/'
            T2Utils.run_tranalyzer(
                pcap= str(pcap_path),
                output_prefix= output ,
                plugins=['protoStats', 'basicFlow', 'macRecorder', 'portClassifier','basicStats',
                 'tcpFlags','tcpStates','icmpDecode','connStat','txtSink'],
                 packet_mode=False
            )
            file_name = os.path.basename(file).split('.')[0]
            txt_path = os.path.join(output,str(file_name)+"_flows.txt")
            csv_path='/home/yfy/flow_csv/'+path+"/"+ file_name + ".csv"
            # Convert flow text to csv file
            os.makedirs('/home/yfy/flow_csv/'+path+'/', exist_ok=True)
            read_file = pd.read_csv(txt_path, index_col=None, header=0, delimiter='\t')
            read_file.to_csv(csv_path,index=None)
