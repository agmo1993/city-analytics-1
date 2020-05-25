#!/bin/bash
# set n to 1
n=1
now=$(date +'%d%m%Y%H%M%S')

# continue until $n equals 5
while [ $n -le $1 ]
do
	echo "Welcome scaling cluster $n"
    sed -i -e 's/addition_instance=[0-9].*/addition_instance='"${now}"'/g' ./inventory/hosts.ini
    ./launch-nectar-servers.sh
    ./install-environments.sh
	n=$(( n+1 ))	 # increments $n
done