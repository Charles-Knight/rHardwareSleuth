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

import praw, configparser, argparse, sys, os

def config_sub(config, sub = "", interactive = False):
    if interactive:
        sub = input("What sub would you like to monitor? (Do not include 'r/'): ")
        config.set('query', 'sub', str(sub))
    else:
        config.set('query', 'sub', str(sub))

def config_query(config, keywords = [], interactive = False):
    if interactive:
        keywords = input("What words would you like to watch for (space separated): ")
        keywords = keywords.split(' ')
        config.set('query', 'keywords', ','.join(keywords))
    else:
        config.set('query', 'keywords', ','.join(keywords))

def config_notif(config, sys = False, email = False, interactive = False):
    affirmatives = ['true'.casefold(), 'yes'.casefold(), 't'.casefold(), 'y'.casefold(), '1'.casefold()]
    
    if interactive:
        response = input("Do you want to display system notifications? ")
        config.set('notifications', 'sys_notif', str(response.casefold() in affirmatives))

        response = input("Do you want email notifications? ")
        config.set('notifications', 'email_notif', str(response.casefold() in affirmatives))
        
    else:
        config.set('notifications', 'sys_notif', str(sys))
        config.set('notifications', 'email_notif', str(email))


def create_empty_config():
    config =  configparser.RawConfigParser()
    config.add_section('email')
    config.add_section('notifications')
    config.add_section('query')
    return config

def write_config(config, file):
    with open(file, 'w') as configfile:
       config.write(configfile)

'''
configure - Allows user to interactively configure query. User will be prompted
to choose a sub, a set of keywords, if they want to use system notifications
and if they want to receive email notifications. Configuration is then saved to
rHWS.cfg
'''
def configure():
    config = create_empty_config()
    config_sub(config, interactive=True)
    config_query(config, interactive=True)
    config_notif(config, interactive=True)
    return config

'''
load_config - Reads configuration from config file. If no config file is given
or if the given file does not exist we call configure so that the user can
interactively configure the program.
'''
def load_config(file):

    if not os.path.exists(file):
        config = configure()
        write_config(config, file)
    else:
        config =  configparser.RawConfigParser()
        config.read(file)
    return config

'''
find_keywords - Checks is the submitted text contains any of the keywords and
returns a list of any keywords found in the text.

Notes: This function is currently just used to search submission titles for
keywords but is written so that it simply takes in a string of text. Thus it
could also be used to searck for keywords in the text bodies of submissions or
probably even comments if the program were extended to include searching such
things.
'''
def find_keywords(text, keywords):
    matches = []
    for word in keywords:
        if text.casefold().count(word.casefold()):
            matches.append(word)
    return matches

'''
match_posts - Given a list of posts, find posts that match search criteria
and return as list of tuples containing matched posts and the keywords on which
they match.

Notes: Not used in current implementation of program. This function doesn't make
sense with the current implementation of my search because the stream object
being used in main returns a single submission at a time. Thus it is easier to
work directly with find_keywords(). I'm keeping this here incase I ever finde a
reason to use it, but it's on the short list of functions to be removed.
'''
def match_posts(posts, keywords):

    matches = []
    for submission in posts:
        found_words = find_keywords(submission.title, keywords)
        if len(found_words) > 0:
            matches.append((submission,found_words))

    return matches

'''
Notify user - Simple function to create system notificatoins. Currently just
creates a notifcation via applescript and isn't super useful.

TO DO:
* Would be cool if I could interact with them. Click them to open the url of
  the post being presented.
* Implement notification for other systems? Windows, Gnome, etc...

Notes: This function is slow. When not using system notifications submissions
are processed and printed to terminal extremely quickly. With this function they
come in slow enough to watch.

It may be worth looking in to some way to interact more directly with the
notification center API. Or perhaps I could start this in a separate thread?
'''
def sys_notification(post, words):
    if sys.platform.startswith('darwin'):
        os.system("""
                  osascript -e 'display notification "{}" with title "New post matching {}"'
                  """.format(post.title, ", ".join(words)))

'''
email_notification - Send email to user for new posts.
TO DO: Implement this
Notes: Need to research how to automate email with python and figure out how I
can securely enter and store email credentials. Should also consider how to
implement this in a way that is safe for publicly publishing my code on github.
'''
def email_notification():
    pass

'''
print_matches - Just prints new posts to the terminal.
'''
def print_matches(post, words):
    print(post.title + " was posted by " + post.author.name)
    print("Matches: ",end="")
    print(', '.join(words))
    print("Link: ", post.url)

def main(args):
    # If there is a file, we want to either load config from file or save the
    # Saved the passed in query to the file (overwriting it if it exists)
    if args.file:
        config = load_config(args.file)

        if args.sub:
            sub = args.sub
        else:
            sub = config.get('query','sub')

        if args.query:
            keywords = args.query
        else:
            keywords = config.get('query','keywords').split(',')

        sys_notif = config.getboolean('notifications','sys_notif')


    # Otherwise we just want to run the query given in the arguments. If none
    # are given then we will want use the interactive configuration
    else:
        sub = args.sub
        keywords = args.query
        sys_notif = True

    # Open subreddit
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit(sub)

    # Create stream and view each new post
    for submission in subreddit.stream.submissions():
        # Check for keywords and if found save details somewhere and notify
        matched_words = find_keywords(submission.title, keywords)
        if len(matched_words) > 0:
            print_matches(submission, matched_words)
            if sys_notif:
                sys_notification(submission, matched_words)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A program to monitor your favorite subreddits")
    parser.add_argument('-r', '--sub', help="The subreddit you want to monitor")
    parser.add_argument('-q', '--query', nargs='*', help="List of keywords you want to search for")
    parser.add_argument('-f', '--file', help="Config file to load, if file does not exist then it will be created")
    args = parser.parse_args()

    main(args)
