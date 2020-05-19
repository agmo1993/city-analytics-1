from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
from afinn import Afinn 
from textblob import Word
import json
import re
import nltk

afinn = Afinn()
stop_words = set(stopwords.words('english'))

def sentiment_analysis(text):
    tokenized = word_tokenize(text.lower())
    sw_removed = [word for word in tokenized if not word in stop_words] 
    corrected = list()
    corrected = [ Word(w).spellcheck()[0][0] for w in sw_removed ]
    sentiment = 0
    for word in corrected:
        sentiment += afinn.score(word)
    return sentiment


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

file_out = open('processed-' + rank + '.json', "w")
file_out.write("{ docs:[\n")

with open('db.json', 'r') as file_in:

    while True:
        
        try:
            newTweet = file_in.readline()
            distributor += 1
            
            if newTweet:

                if distributor % size == rank:
                    
                    tweetString = newTweet[:-2]
                    tweetJson = json.loads(tweetString)

                    tweetJson['sentiment'] = sentiment_analysis(tweetJson['doc']['text'])
                    
                    file_out.write(str(tweetJson) + ",\n")

                else:
                    continue
    
            else:
                file_out.write("]}")
                file_out.close()
                break
        
        except:
            print('error')
