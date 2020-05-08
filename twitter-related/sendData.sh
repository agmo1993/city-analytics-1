#!/bin/sh

while true
do
python txt_to_json.py

curl -XPOST "http://${user}:${pass}@${masternode}:5984/twitter/_bulk_docs " --header "Content-Type: application/json"   --data @harvested.json

rm harvested.json
rm harvested.txt

sleep 60
done