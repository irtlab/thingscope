DIR=$1


for d in $(find $DIR -maxdepth 1 -type d)
do
  #Do something, the directory is accessible with $d:
  echo $d

  if [ "$d" = "$DIR" ]; then
    continue
  fi
  NAME=`basename $d`

  MAC=`cat $d/_iotdevice-mac.txt`
  echo Processing $NAME $MAC $d

  python update_device_name.py --device_mac=$MAC --name=$NAME

  #./run_pcaps_files_dir.sh $d $MAC $NAME

done
