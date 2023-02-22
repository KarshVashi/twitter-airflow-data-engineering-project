import tweepy
import pandas as pd
import json
from datetime import datetime
import s3fs

def run_twitter_etl():
    api_key = "FB57q2lyzShM4XxRTQ9v3dpV4"
    api_secrets = "bkLV14CEJnV0vyB38E9NhnTY2Cj8obnHUqupWT1z6wmDcUW5bW"
    access_token = "987600519442001920-lVclhsJMPu9gVOHUbCOpg6L325uKUzO"
    access_secret = "oa6jrctsSli0O0XOqeeHRIOgqhu98Y2luNWfgngfKIc7w"

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(api_key, api_secrets)
    auth.set_access_token(access_token, access_secret)

    # Creating the api object
    api = tweepy.API(auth)

    tweets = api.user_timeline(screen_name='@elonmusk',count=100, include_rts=False, tweet_mode='extended')
    print(tweets)

    tweet_list = []
    for tweet in tweets:
        text = tweet._json['full_text']

        t = {'user': tweet.user.screen_name,
             'text': text,
             'favorite_count': tweet.favorite_count,
             'retweet_count': tweet.retweet_count,
             'created_at': tweet.created_at}

        tweet_list.append(t)

    df = pd.DataFrame(tweet_list)
    df.to_csv("s3://karsh-twitter-s3bucket/elontwitteractivity.csv")

