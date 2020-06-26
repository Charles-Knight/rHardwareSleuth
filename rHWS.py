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
Pull out posts that match search criteria
'''
def match_posts(posts, keywords):

    '''
    checks if submission contains any one of the keywords
    '''
    def matches_keyword(text, keywords):
        for word in keywords:
            if text.count(word):
                return True
        return False

    matches = []
    for submission in posts:
        if matches_keyword(submission.title, keywords):
            matches.append(submission)

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
'''
def notify():
    pass

if __name__ == "__main__":
    sub = "hardwareswap"
    keywords = ["RTX","DDR4"]

    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit(sub)

    # Create stream and view each new post
    # Check for keywords and if found save details somewhere ad notify
    # want to note: post title, time, author, and link
    # Also TODO: put matches_keyword outside of match_posts

    # OLD MAIN #
    #new = subreddit.new(limit=100)
    #matching = match_posts(new, keywords)

    #print_posts(matching)
