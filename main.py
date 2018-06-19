import configparser
import logging
import os
import time
from datetime import timedelta, datetime

import coloredlogs
import praw
from pushbullet import Pushbullet

coloredlogs.install()
logging.basicConfig(filename='bot.log', level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
config = configparser.ConfigParser()
config.read('auth.ini')  # All my usernames and passwords for the api
pb = Pushbullet(str(config.get('auth', 'pb_key')))

reddit = praw.Reddit(client_id=config.get('auth', 'reddit_client_id'),
                     client_secret=config.get('auth', 'reddit_client_secret'),
                     password=config.get('auth', 'reddit_password'),
                     user_agent="Flair your posts script made by u/J_C___",
                     username=config.get('auth', 'reddit_username'))
bot_message = "\r\r^(I am a script. If I did something wrong, ) [^(let me know)](/message/compose/?to=J_C___&subject=ALERT+Flair+your+post+bot)"
logging.info("Posting as: " + str(reddit.user.me()))
SUBREDDIT = config.get('auth', 'reddit_subreddit')
LIMIT = int(config.get('auth', 'reddit_limit'))

# If the posts_replied text file dosn't exist, create it and initialize the empty list.
if not os.path.isfile("posts_replied.txt"):
    posts_replied = []
# If the file does exist import the contents into a list
else:
    with open("posts_replied.txt", "r") as f:
       posts_replied = f.read()
       posts_replied = posts_replied.split("\n")
       posts_replied = list(filter(None, posts_replied))

rule_1 = "\r\r>**All posts must be assigned a flair**. If you don't flair your post, it will be removed. You can flair on mobile by posting it in your title, such as [Theory] Toffee is Star's brother. [Here is a list of flair options](https://www.reddit.com/r/StarVStheForcesofEvil/wiki/flairs). If your post is removed by the flair bot, **do NOT repost it**: [message the mods](https://www.reddit.com/message/compose?to=%2Fr%2FStarVStheForcesofEvil&subject=&message=) and we'll approve it. Unflaired posts are subject to removal without warning at any time."
def reply_bot():
    subreddit = reddit.subreddit(SUBREDDIT)
    new_posts = subreddit.new(limit=LIMIT)
    for submission in new_posts:
        if (submission.link_flair_text is None) and (datetime.utcnow() - datetime.fromtimestamp(submission.created_utc) >= timedelta(minutes=15)) and submission.id not in posts_replied:
            submission.reply("Hey there u/" + submission.author.name + "! Your post has been removed in accordance with rule #1 of this subreddit." + rule_1 + bot_message)
            submission.mod.remove()
            logging.info('Submission removed:' + str(submission.id))
            posts_replied.append(submission.id)
            update_files(posts_replied)


def update_files(posts_replied):
    with open("posts_replied.txt", "w") as f:
        for x in posts_replied:
            f.write(x + "\n")
    logging.info("Progress File Successfully Updated!")

if __name__ == "__main__":
    try:
        logging.info("------Starting: Flair Your Post Bot------")
        while True:
            reply_bot()
    except KeyboardInterrupt:
        update_files(posts_replied)
        logging.warning('Script interrupted')
    except (AttributeError, praw.exceptions.PRAWException) as e:
        logging.warning("PRAW encountered an error, waiting 30s before trying again. %s" % e)
        time.sleep(30)
        pass
    except praw.exceptions.APIException as e:
        logging.warning("Reddit API encountered an error. %s" % e)
        time.sleep(30)
        pass
    finally:
        push = pb.push_note("SCRIPT Down", "J_C___ Hiatus Script is Down!")
        update_files(posts_replied)
