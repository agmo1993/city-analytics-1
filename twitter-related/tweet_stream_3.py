
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
 
ACCESS_TOKEN = '1251843024440528896-Ap9IxW0TbyLbN9XcQjc00Pc6ox9T0z'
ACCESS_TOKEN_SECRET = 'pMyWWJ6AsuAaP9Yi2Mjwql3NGWKvZc8nOoPKbl4op4l8S'
CONSUMER_KEY = 'bpOrX6SJQ73qOFXxy65AZ3uRA'
CONSUMER_SECRET = 'BWHs9pRCZb5KPNAo2Mahd0AEvEa9FgWP15g0cc5yEjDOBiKGQz'

class Listener(StreamListener):

    def on_data(self, data):
        try:
            with open("harvested_tweets.json", 'a') as file:
                file.write(data)

        except Exception as e:
            with open("error_log.txt", 'a') as file2:
                file2.write(str(e) + '\n')

        return True
          
    def on_error(self, status):
        print(status)

 
if __name__ == '__main__':

    while True:
        try:
            listener = Listener()
            auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

            stream = Stream(auth, listener)
            stream.filter(locations = [113.338953078, -43.6345972634, 153.569469029, -10.6681857235])
        except Exception as e:
            with open("error_log.txt", 'a') as file2:
                file2.write(str(e) + '\n')
