import os
import sys
import tweepy
import numpy as np
import pandas as pd
from tweepy import OAuthHandler
from tweepy import Cursor
import matplotlib.pyplot as plt

"""
Twitter Authentification Credentials
Please update with your own credentials
"""
cons_key = os.environ.get("CONSUMER_KEY")
cons_secret = os.environ.get("CONSUMER_SECRET")
acc_token = ''
acc_secret = ''
# (1). Athentication Function
def get_twitter_auth():
    """
    @return:
        - the authentification to Twitter
    """
    try:
        consumer_key = cons_key
        consumer_secret = cons_secret
        access_token = acc_token
        access_secret = acc_secret
        
    except KeyError:
        sys.stderr.write("Twitter Environment Variable not Set\n")
        sys.exit(1)
        
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    
    return auth
# (2). Client function to access the authentication API
def get_twitter_client():
    """
    @return:
        - the client to access the authentification API
    """
    auth = get_twitter_auth()
    client = tweepy.API(auth, wait_on_rate_limit=True)
    return client
# (3). Function creating final dataframe
def get_tweets_from_user(twitter_user_name, page_limit=16, count_tweet=200):
    """
    @params:
        - twitter_user_name: the twitter username of a user (company, etc.)
        - page_limit: the total number of pages (max=16)
        - count_tweet: maximum number to be retrieved from a page
        
    @return
        - all the tweets from the user twitter_user_name
    """
    client = get_twitter_client()
    
    all_tweets = []
    
    for page in Cursor(client.user_timeline, 
                        screen_name=twitter_user_name, 
                        count=count_tweet).pages(page_limit):
        for tweet in page:
            parsed_tweet = {}
            parsed_tweet['date'] = tweet.created_at
            parsed_tweet['author'] = tweet.user.name
            parsed_tweet['source'] = tweet.source            

    
            all_tweets.append(parsed_tweet)
    
    # Create dataframe 
    df = pd.DataFrame(all_tweets)
    
    
    return df

def get_frequency_from_df(dataframe, column_name):
    """
    @params:
        - dataframe: the pandas dataframe object returned by get_tweets_from_user()
        - column_name: the item from the API (author, date, OR source)
        
    @return
        - A series containing unique counts for different values in the DF Column
    """
    count = dataframe[column_name].value_counts()
    return count


def main():
    user = sys.argv[1]
    account = get_tweets_from_user(user)
    freq = get_frequency_from_df(account, 'source')
    print(freq)
   
    labels, sizes = [ freq.keys(), freq.values ]
 
    plt.pie(sizes, labels=labels, autopct='%1.1i%%')
    plt.title("@" + str(user) + "\nTweets Looked At: " + str(account.shape[0] + 1))
    plt.show()

    
main()

