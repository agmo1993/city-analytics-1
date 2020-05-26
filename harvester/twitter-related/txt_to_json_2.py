import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from afinn import Afinn
from textblob import Word
import re
import nltk

nltk.download('stopwords')
nltk.download('punkt')

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

json_file_path = "harvested.json"
txt_file_path = 'harvested2.txt'

json_file = open(json_file_path, "w")
data = {}
data["docs"] = []
file = open(txt_file_path,"r")


while True:
    try:
        newTweet = file.readline()

        if newTweet:
            loaded_tweet = json.loads(newTweet)
            sentence = loaded_tweet['text']
            sentiment = sentiment_analysis(sentence)
            loaded_tweet['sentiment'] = sentiment
            data["docs"].append(loaded_tweet)
        else:
            break

    except Exception as e:
        print(str(e))
        break

json.dump(data, json_file)
json_file.close()