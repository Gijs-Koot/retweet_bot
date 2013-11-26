import tweepy
from pprint import pprint 
from tweepy.streaming import StreamListener, Stream

import simplejson as json
with open('config.json') as f:
	config = json.load(f)

def get_main_identity_auth():

	consumer_key = config["main"]["consumer_key"]
	consumer_secret = config["main"]["consumer_secret"]

	access_token = config["application"]["access_token"]
	access_secret = config["application"]["access_secret"]

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)

	return auth

def get_client_auths():

	return [get_main_identity_auth()]

def get_client_names():

	return ['tw_explorer']

def is_retweetable_tweet(status):

	if 'user' in status and not status['user']['screen_name'] in get_client_names(): return True
	return False	

def condition(status):
	
	if is_retweetable_tweet(status) and	config["condition"] in status["text"]: return True
	return False

def retweet_by_all(status):

	for auth in get_client_auths():
		
		api = tweepy.API(auth)
		api.retweet(status["id"])
		print 'i will retweet', status["id"], status["text"]

class StdOutListener(StreamListener):
    
    # listens to stream and will start retweet_by_all if condition
    def on_data(self, data):
        
        status = json.loads(data)
        if condition(status):
	        retweet_by_all(status)
	
    def on_error(self, status):
        print status

if __name__ == "__main__":

	# starts main loop
	auth = get_main_identity_auth()
	api = tweepy.API(auth)
	stream = Stream(auth, StdOutListener(StreamListener))
	stream.filter(config["listen"])