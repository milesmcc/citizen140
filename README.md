# citizen140
Archive those tweets, and get a notification whenever one is deleted.

140 characters certainly has a lot to hide. If it's public, then why not archive it!

## Installation
1. Set up a new app on your Twitter account, and get all the necessary credentials ready (consumer key/secret, access token/secret). If you don't know what those are, then citizen140 is probably not for you.
2. Clone C140 into a directory of your choice.
3. Move into the directory that will serve as the root data directory for citizen140. This is where data will be stored, and it's best practice to keep this separated from C140's source. Source protection.
4. Run main.py
5. The program will close and tell you to edit the configuration file it just created. It'll tell you where to look.
6. Edit the configuration file, adding the Twitter authentication credentials as needed.
7. Add the twitter IDs of the users you want to monitor in the config file.
8. Adjust the intervals as necessary. C140 operates under the idea of 'iterations': the program runs a loop, and every X loops (iterations), certain actions are conducted. Each iteration runs a 'quick' update, called a pass, in which new tweets are written to the database. The 'pass' field defines the amount of seconds between each pass. 'Account' defines how many passes between each account data update (account metadata, such as followers, following, bio, etc), and 'fullpass' defines how many passes between each scan, in which the latest 3400 (maximum permitted by Twitter API) tweets are loaded from Twitter, and deleted tweets are detected.
9. Set something up in *notificationhandler.py*. Got something good? Submit a PR. An official notification system (via the email defined in configuration.json) will be implemented soon.
10. Run main.py again
11. Let C140 do its work!
