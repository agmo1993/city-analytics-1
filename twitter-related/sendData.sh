#!/bin/sh

python tweet_stream.py

while true
do
python txt_to_json.py

curl -XPOST "http://${user}:${pass}@${masternode}:5984/twitter/_bulk_docs " --header "Content-Type: application/json"   --data @ha$
rm harvested.json
rm harvested_tweets.txt

sleep 60
done