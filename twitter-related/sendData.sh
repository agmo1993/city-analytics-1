#!/bin/sh
while true
do
cp harvested.txt harvested2.txt
rm harvested.txt

python3 txt_to_json_4.py

curl -XPOST "http://admin:admin@172.26.129.225:5984/twitter/_bulk_docs " --header "Content-Type: application/json"   --data @harvested.json


sleep 5
rm harvested.json
done