
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
from afinn import Afinn 
from textblob import Word
import json
import re
import nltk

nltk.download('stopwords')
nltk.download('punkt')

comm = MPI.COMM_WORLD

rank, size = comm.Get_rank(), comm.Get_size()

comm.Barrier()

def sentiment_analysis(text):
    afinn = Afinn()
    stop_words = set(stopwords.words('english')) 
    tokenized = word_tokenize(text.lower())
    sw_removed = [word for word in tokenized if not word in stop_words] 
    corrected = list()
    for word in sw_removed:
        corrected.append(Word(word).spellcheck()[0][0])
    sentiment = 0
    for word in corrected:
        sentiment += afinn.score(word)
    return sentiment

filehandle = open("db.json", 'r')
txt_file_path = 'processedMPI.json'
json_file_path = open(txt_file_path.format(count), "w")
json_file_path.write("{ docs:[\n")

count = 0
while count < 100:
    count += 1
    if rank == 0:
        line = filehandle.readline()
        if "text" in line:
            comm.send(line, dest=1)
        if not line: #if no line is left to read, a break command is sent to processes 2 and 4
            comm.send("break", dest=1) #check for tweets
            break

    elif rank == 1:
        line = comm.recv(source=0)
        if line == "break":
            comm.send("break",dest=2)
            break
        line = line.strip("\n")
        line = line.rstrip()
        line = line.rstrip(",")
        line_dict = json.loads(line)
        comm.send(line_dict, dest=2)

    elif rank == 2:
        line_dict = comm.recv(source=1)
        if line_dict == "break":
            comm.send("break",dest=3)
            break
        sentence = line_dict['doc']['text']
        line_dict['sentiment'] = sentiment_analysis(sentence)
        comm.send(line_dict, dest=3)
        
    elif rank == 3:
        line_dict = comm.recv(source=2)
        if line_dict == "break":
            break
        json_file_path.write(str(line_dict) + ",\n")

json_file_path.write("]}")
json_file_path.close()
