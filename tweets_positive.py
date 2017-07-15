import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
 
class TwitterClient(object):
    """
        Generic Twitter Class for sentiment analysis.
    """
    def __init__(self, key=None, secret=None, token=None, token_secret=None):
        """
            Class constructor or initialization method.
        """
        # keys and tokens from the Twitter Dev Console
        if key and secret and token and token_secret:
            # attempt authentication
            try:
                # create OAuthHandler object
                self.auth = OAuthHandler(key, secret)
                # set access token and secret
                self.auth.set_access_token(token, token_secret)
                # create tweepy API object to fetch tweets
                self.api = tweepy.API(self.auth)
            except Exception, err_msg:
                print("Error: Authentication Failed \n %s" % err_msg)
        else:
            print("Error: Consumer key, secret and access token are required for authentication")
 
    def clean_tweet(self, tweet):
        """
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        """
            Utility function to classify sentiment of passed tweet using textblob's sentiment method
        """
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, keyword, count = 10):
        """
        Main function to fetch tweets and parse them.

        :params
            keyword - the search keyword, you need to search tweets for.
            count - no of tweets to fetch from the search
        """
        # empty list to store parsed tweets
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=keyword, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # saving text and sentiment
                parsed_tweet = {'text': tweet.text, 'sentiment': self.get_tweet_sentiment(tweet.text)}
 
                # saving text of tweet
                # parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                # parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
 
    
if __name__ == "__main__":
    # keys and tokens from the Twitter Dev Console
    consumer_key = raw_input('Enter/Paste the consumer key')
    consumer_secret = raw_input('Enter/Paste the consumer secret')
    access_token = raw_input('Enter/Paste the access token')
    access_token_secret = raw_input('Enter/Paste the access token secret')
    # creating object of TwitterClient Class
    api = TwitterClient(consumer_key, consumer_secret, access_token, access_token_secret)
    # calling function to get tweets
    keyword = raw_input('Enter the keyword - to search the tweets')
    tweets = api.get_tweets(keyword=keyword, count=200)
 
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} % \
        ".format(100*len(tweets - ntweets - ptweets)/len(tweets)))
 
    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
 
    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
 
