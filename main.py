import praw
import io
import os
import re
import configparser
from datetime import timedelta
from time import time
config = configparser.ConfigParser()
config.read('auth.ini') #All my usernames and passwords for the api

reddit = praw.Reddit(client_id=config.get('auth', 'reddit_client_id'),
                     client_secret=config.get('auth', 'reddit_client_secret'),
                     password=config.get('auth', 'reddit_password'),
                     user_agent="Flair your posts bot made by u/J_C___",
                     username=config.get('auth', 'reddit_username'))
bot_message = "\r\r^(I am a script. If I did something wrong, ) [^(let me know)](/message/compose/?to=J_C___&subject=all_seeing_eye_bot)"
print("Posting as: ", reddit.user.me())
SUBREDDIT = config.get('auth', 'reddit_subreddit')
LIMIT = int(config.get('auth', 'reddit_limit'))

#If the meep_replys text file dosn't exist, create it and initilize the enpty list.
if not os.path.isfile("posts_replied.txt"):
    posts_replied = []
#If the file does exist import the contents into a list
else:
    with open("posts_replied.txt", "r") as f:
       posts_replied = f.read()
       posts_replied = posts_replied.split("\n")
       posts_replied = list(filter(None, posts_replied))

def reply_bot(debug=False):
    subreddit = reddit.subreddit(SUBREDDIT)
    new_posts = subreddit.new(limit=LIMIT)
    for submission in new_posts:
		if (submission.link_flair_text is None) and (submission.created_utc - datetime.utcnow() == timedelta(minutes=1):
			submission.reply("Hey there! Don't forget to flair your posts c: don't want to anger the mods ;)" + bot_message)


def update_files(posts_replied):
    with open("posts_replied.txt", "w") as f:
        for x in posts_replied:
            f.write(x + "\n")
try:
    while True:
        reply_bot()
except KeyboardInterrupt:
    update_files(posts_replied)
    print('Interrupted')
