import databasehandler
import scanner
import twitterhandler
import notificationhandler
import time
import sys
from userio import say, error, ok, warn

# download all the tweets
def operate():
    ok("Beginning operation...")
    for account in databasehandler.configuration["monitored_accounts"]:
        say("Writing the account data for " + str(account))
        databasehandler.write_account(account, twitterhandler.get_account_data(account))
        say("Writing the other data for " + str(account))
        scanner.update_account(account)
        # this operation is done at the beginning of operation because
        # it sets up the database on the first run, and it also grabs
        # any tweets quickly, before the first full pass is run on each account

    iteration = 0
    while iteration < sys.maxint:
        if iteration % databasehandler.configuration["intervals"]["fullpass"] == 0:
            for account in databasehandler.configuration["monitored_accounts"]:
                ok("Running full pass for " + str(account))
                deleted = scanner.full_pass(account)
                if len(deleted) > 0:
                    deleted_tweets = [databasehandler.get_tweet(account, tweet) for tweet in deleted]
                    notificationhandler.notify_deletions(account, deleted)
        if iteration % databasehandler.configuration["intervals"]["account"] == 0:
            for account in databasehandler.configuration["monitored_accounts"]:
                ok("Running account update...")
                databasehandler.write_account(account, twitterhandler.get_account_data(account))

        for account in databasehandler.configuration["monitored_accounts"]:
            ok("Running partial update pass for " + str(account))
            deleted = scanner.update_account(account)

        iteration += 1
        time.sleep(databasehandler.configuration["intervals"]["pass"])
    operate()  # in 292471208677 years...

operate()
