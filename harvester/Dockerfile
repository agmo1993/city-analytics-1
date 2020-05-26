FROM python:3

WORKDIR /usr/src/app

COPY twitter-related /usr/src/app

RUN pip3 install tweepy && \
    pip3 install nltk && \
    pip3 install afinn && \
    cd twitter-related && \
    nohup python3 tweet_stream_3.py & 

CMD nohup ./sendData.sh &