# rHardwareSleuth
rHWS.py - A script to monitor subreddits for given keywords and then notify the
user of new threads wich match any of the keywords. This was specifically created to monitor r/HardwareSwap for computer compents that I want to find but always seem to be to late to purchase. This is also meant to be a learning project aimed at teaching myself how to interact with resources on the internet using third party API's. It will initially use praw but *may* later transition to manually using the reddit API, not because its a better way to do this, but because it will provide me with a greater learning experience.

## Requirements:

1. A reddit account configured for API access.
2. You must have praw installed: Simply run `pip install praw`
3. You need to create a praw.ini file this is detailed in the praw [documentation](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html). The script currently uses a site named 'bot1'

## Usage

Run the program from the terminal using `python3 rHWS.py`

The program will attempt to load it's parameters from rHWS.cfg and if the file is not found you will be prompted to interactively create it. Simply enter the subreddit you wish to monitor (without the 'r/'), then enter the keywords you want the script to watch for. You must also decide if you want system notifications (only implemented on macOS), and if you would like email notifications (not yet implemented). Afterwords your configuration will be saved to rHWS.cfg, in your current working directory.

The program will then open a stream and monitor incoming submissions to the given subreddit. If a new submission is found matching your keywords, it will be printed to the terminal and you will be notified via any of the notifications methods you selected. (Assuming they have been implemented.)

You can also manually edit rHWS.cfg if you so desire. The file is currently extremely simple and it should be evident what everything does. Simply run the program once to create an intial file and then open it in any text editor.