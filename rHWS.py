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

import praw, configparser, sys, os

def configure():
    pass

'''
load_config pulls in configuration from config file. If no config file is
present we should call function to configure program and then save configuration
to a file.
'''
def load_config(file = ""):
    config =  configparser.RawConfigParser()
    if file == "":
        config = configure()
    else:

        config.read(file)
    return config

'''
Checks if submission contains any one of the keywords and then returns list of
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
Not used in current implementation of program
'''
def match_posts(posts, keywords):

    matches = []
    for submission in posts:
        found_words = find_keywords(submission.title, keywords)
        if len(found_words) > 0:
            matches.append((submission,found_words))

    return matches

'''
Notify user
Simple function to create system notificatoins. Currently just creates an apple
script notifcation that isn't super useful.

TODO:
* would be cool if I could interact with them. Click them to open the url of
  the post being presented.
* Implement notification for other systems? Windows, Gnome, etc...
'''
def sys_notification(post, words):
    if sys.platform.startswith('darwin'):
        os.system("""
                  osascript -e 'display notification "{}" with title "New post matching {}"'
                  """.format(post.title, ", ".join(words)))

'''
Send email to user for new posts.
TODO: Implement this
'''
def email_notification():
    pass
    # Send an email to user

'''
Just prints new posts to the terminal
'''
def print_matches(post, words):
    # Print to terminal
    print(post.title + " was posted by " + post.author.name)
    print("Matches: ",end="")
    print(', '.join(words))
    print("Link: ", post.url)

def main():
    config = load_config('rHWS.cfg')
    sub = config.get('query','sub')
    keywords = config.get('query','keywords').split(',')
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit(sub)

    # Create stream and view each new post
    for submission in subreddit.stream.submissions():

        # Check for keywords and if found save details somewhere and notify
        # want to note: post title, time, author, and link
        matched_words = find_keywords(submission.title, keywords)
        if len(matched_words) > 0:
            print_matches(submission, matched_words)
            sys_notification(submission, matched_words)

if __name__ == "__main__":
    main()
