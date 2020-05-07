import json

json_file_path = "harvested.json"
txt_file_path = 'harvested.txt'

json_file = open(json_file_path, "w")
json_file.write('{"new_edits": false,\n')
json_file.write('"docs":[\n')

with open(txt_file_path, "r") as file:
    
    while True:
        try:
            newTweet = file.readline()
            
            if newTweet:
                json.loads(newTweet)
                json_file.write(newTweet[:-1] + ',\n')

            else:
                break
  
        except:
            json_file.write('{"content" : "corrupted"},\n')
            
json_file.write('{"dummy" : "tweet"}]}')
json_file.close()