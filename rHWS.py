'''
Author: Charles Knight

rHWS.py - A script to monitor subreddits for given keywords and then notify the
user of the given threads. This was specifically created to monitor
r/HardwareSwap for computer compents that I want to purchase but always seem to
be to late to find. This is also meant to be a learning project aimed at
teaching myself how to interact with resources on the internet using third party
API's. It will initially use praw but may later transition to manually using the
reddit API, not because its a better way to do this, but because it will provide
me with a greater learning experience.
'''

import praw

'''
Get new posts from targeted subreddit
'''
def get_recent_posts():
    pass

'''
checks if submission contains any one of the keywords and then returns list of
all matching keywords.
'''
def find_keywords(text, keywords):
    matches = []
    for word in keywords:
        if text.count(word):
            matches.append(word)
    return matches

'''
Given a list of posts, find posts that match search criteria and return as list
of tuples containing matched posts and the keywords on which they match
'''
def match_posts(posts, keywords):

    matches = []
    for submission in posts:
        found_words = find_keywords(submission.title, keywords)
            if len(found_words) > 0:
                matches.append((submission,found_words))

    return matches


'''
Display posts
'''
def print_posts(posts):
    for submission in posts:
        print(submission.title)
        print("Score: " + str(submission.score))
        print()

'''
Notify user
Simple notification method. Currently just creates an apple script notifcation
to notify on macOS.
TODO: extend with other functionality - email? system notifications? sms?
'''
def notify(title, message):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

if __name__ == "__main__":
    sub = "hardwareswap"
    keywords = ["RTX","DDR4"]

    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit(sub)

    # Create stream and view each new post
    # Check for keywords and if found save details somewhere ad notify
    # want to note: post title, time, author, and link
    # Also TODO: put find_keywords outside of match_posts

    # OLD MAIN #
    #new = subreddit.new(limit=100)
    #matching = match_posts(new, keywords)

    #print_posts(matching)
