import tweepy
from tweepy import OAuthHandler
 
consumer_key = 'YOUR-CONSUMER-KEY'
consumer_secret = 'YOUR-CONSUMER-SECRET'
access_token = 'YOUR-ACCESS-TOKEN'
access_secret = 'YOUR-ACCESS-SECRET'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

# first 10 tweets from app authors timeline
# Cursor interface to iterate through different types of objects
for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    print(status.text)
    #print(status._json)

# To have a list of all the followers.
for friend in tweepy.Cursor(api.friends).items():
    print(friend._json)

