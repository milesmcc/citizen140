import json
import os
from userio import say, error, ok, warn
import sys

# initialization
if not os.path.isfile("configuration.json"):
    warn("No configuration file found. First launch?")
    say("Generating configuration file...")

    default_configuration = {
        "authentication": {
            "consumer_key": "consumerKeyHere",
            "consumer_secret": "consumerSecretHere",
            "access_token": "accessTokenHere",
            "access_token_secret": "accessTokenSecretHere"
        },
        "monitored_accounts": [
            25073877,
            822215679726100480
        ],
        "intervals": {
            "fullpass": 600,
            "account": 1200,
            "pass": 5
        },
        "notifications": {
            "email": "email@example.com"
        }
    }
    
    with open("configuration.json", "w") as configuration_file:
        json.dump(default_configuration, configuration_file, indent=4, sort_keys=True)
        ok("Configuration file created!", detail="The file is located at " + os.path.abspath("configuration.json"))
        configuration_file.close()
        ok("Please configure the file, then re-run citizen140.")
        sys.exit()  # exit the system to allow user to configure

if not os.path.exists("database"):  # make the database, for first run
    os.mkdir("database")
    ok("Created database folder!")

configuration = {}

with open("configuration.json", "r") as configuration_file:
    configuration = json.load(configuration_file)
    configuration["monitored_accounts"] = [str(account) for account in configuration["monitored_accounts"]]
    ok("Loaded configuration from file!")

def get_authentication():
    return configuration["authentication"]


def is_account(id):
    return os.path.isfile("database/" + str(id) + "/account.json")


def write_account(id, data):
    if not is_account(id):
        if not os.path.isdir("database/" + str(id)):
            os.mkdir("database/" + str(id))
    with open("database/" + str(id) + "/account.json", "w") as account_file:
        json.dump(data, account_file)


def get_account(id):
    if is_account(id):
        with open("database/" + str(id) + "/account.json", "r") as account_file:
            json_data = json.load(account_file)
            account_file.close()
            return json_data


def get_tweet(account, tweet):
    if is_account(account):
        if os.path.exists("database/" + str(account) + "/tweets/" + str(tweet) + ".json"):
            with open("database/" + str(account) + "/tweets/" +str(tweet) + ".json", "r") as tweet_file:
                return json.load(tweet_file)

# THIS MUST NOT BE CALLED ON AN ACCOUNT WHICH HAS NOT BEEN INITIALIZED
def write_tweet(account, tweet, data, overwrite=True):
    if (not overwrite) and os.path.exists("database/"+str(account)+"/tweets/" + str(tweet) + ".json"):  # if tweet already written and overwrite = false, do not write to file
        return False
    if not is_account(account):
        error("Cannot write tweet to an account that does not exist!", detail="Tweet = " + str(tweet) + ", account = " + str(account) + ".")
        return
    if not os.path.isdir("database/" + str(account) + "/tweets"):
        os.mkdir("database/" + str(account) + "/tweets")
    with open("database/" + str(account) + "/tweets/" + str(tweet) + ".json", "w") as tweet_file:
        json.dump(data, tweet_file)
        return True

def get_tweets(account):
    if is_account(account) and os.path.isdir("database/" + str(account) + "/tweets"):
        files = os.listdir("database/" + str(account) + "/tweets")
        tweet_ids = []
        for filename in files:
            try:
                tweet_ids.append(str(int(filename[:-5])))
            except ValueError as e:
                continue  # is not a .json tweet file
        return tweet_ids
