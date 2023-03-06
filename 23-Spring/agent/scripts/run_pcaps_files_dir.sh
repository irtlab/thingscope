DIR=$1
MAC=$2
TITLE=$3

for FILE in $DIR/*pcap; do
    echo $FILE; 
    python device_security_scanner.py --devmacaddr="${MAC}" --pcap=$FILE --title=$TITLE --db_name=iotalto
done
