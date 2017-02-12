import twitterhandler
import databasehandler
from userio import say, ok, warn, error

accounts = databasehandler.configuration["monitored_accounts"]

# returns deleted tweets
def full_pass(account):
    if not databasehandler.is_account(account):
        error("Cannot scan account that doesn't exist!", detail="Offending account is " + str(account))
    else:
        # pull all the tweet ids from the database
        archived_ids = databasehandler.get_tweets(account)

        # pull all the tweets from Twitter
        available_tweets = twitterhandler.get_all_tweets(account)
        available_ids = [tweet["id"] for tweet in available_tweets]

        deleted_candidates = [idz for idz in archived_ids if int(idz) not in available_ids]

        ok("Found " + str(len(deleted_candidates)) + " deletion candidates...")

        deleted = []
        for candidate in deleted_candidates:
            if not twitterhandler.does_status_exist(candidate):
                ok("Tweet " + str(candidate) + " has been deleted!")
                deleted.append(candidate)
        ok("Found " + str(len(deleted)) + " deleted tweets!")

        # also write the new tweets to the database
        pushed = 0
        for tweet in available_tweets:
            if databasehandler.write_tweet(account, tweet["id"], tweet, overwrite=False):
                pushed += 1

        # and mark the deleted tweets as deleted
        for tweet_id in deleted:
            tweet = databasehandler.get_tweet(account, tweet_id)
            tweet["deleted"] = True
            databasehandler.write_tweet(account, tweet_id, tweet)

        ok("Also pushed " + str(pushed) + " new tweets to the database.")

        return deleted

# updates an account with the latest 200 tweets
def update_account(account):
    pushed = 0
    for tweet in twitterhandler.get_latest_tweets(account):
        tweet["deleted"] = False
        if databasehandler.write_tweet(account, tweet["id_str"], tweet, overwrite=False):
            pushed += 1
    ok("Pushed latest tweets for " + str("account") + " into the database.", detail="Pushed " + str(pushed) + " new tweets.")
