import tweepy
import databasehandler as db
import json
from userio import say, ok, warn, error

say("Establishing connection to Twitter...")
auth = tweepy.OAuthHandler(db.get_authentication()["consumer_key"], db.get_authentication()["consumer_secret"])
auth.set_access_token(db.get_authentication()["access_token"], db.get_authentication()["access_token_secret"])
api = tweepy.API(auth)
ok("Connection established!")

#Twitter only allows access to a users most recent 3240 tweets with this method
def get_all_tweets(id):
    tweets = []
    new_tweets = api.user_timeline(user_id=id, count=200)
    tweets.extend(new_tweets)
    oldest = tweets[-1].id - 1
    while len(new_tweets) > 0:
    	say("getting tweets before " + str(oldest))
    	new_tweets = api.user_timeline(user_id=id, count=200, max_id=oldest)
    	tweets.extend(new_tweets)
    	oldest = tweets[-1].id - 1
    	say("..." + str(len(tweets)) + " tweets downloaded so far")
    return [tweet._json for tweet in tweets]  # this makes me sad, but is there a better way? submit a PR.


def get_account_data(account):
    return api.get_user(account)._json


def get_latest_tweets(id):
    tweets = api.user_timeline(user_id=id, count=200)
    return [tweet._json for tweet in tweets]  # this makes me sad, but is there a better way? submit a PR.

def does_status_exist(id):
    try:
        api.get_status(id)
        return True
    except tweepy.TweepError as err:
        if err[0][0]["code"] == 144:
            return False
        else:
            raise err
