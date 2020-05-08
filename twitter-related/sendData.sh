#!/bin/sh
while true
do
python txt_to_json_4.py

curl -XPOST "http://${user}:${pass}@${masternode}:5984/twitter/_bulk_docs " --header "Content-Type: application/json"   --data @ha$
rm harvested.json
rm harvested_tweets.txt

sleep 60
done