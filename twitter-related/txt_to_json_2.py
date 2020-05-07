import json

json_file_path = "harvested.json"
txt_file_path = 'harvested.txt'

json_file = open(json_file_path, "w")
data = {}

data["docs"] = []
file = open(txt_file_path, "r")
    
while True:
    try:
        newTweet = file.readline()
        
        if newTweet:
            loaded_tweet = json.loads(newTweet)
            data["docs"].append(loaded_tweet)

        else:
            break

    except:
        break
            
json.dump(data, json_file_path)
json_file.close()