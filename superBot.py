#!/usr/bin/env python

from functions import *
import tweepy
import logging
from config import create_api #this takes the credentials exported to the venv
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

statcounter=0


# This is the mentions bot from tweepy ment to work with our status change
def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")

            #This just follows whoever mentioned us if we aren't already
            #if not tweet.user.following:
            #    tweet.user.follow()
            #This is how we reply to the mention
            api.update_status(
                status="Please reach us via DM or visit us at https://linktr.ee/inworks/",in_reply_to_status_id=tweet.id)
# This is supposed to reply to a tweet as a comment when someone @ the bot
# at the moment this only works if someone Tweets, if someone comments on our tweets the bot tweets out the response, working on a fix
    return new_since_id

def main():
    
    # Here are the variables needed for functions.py
    # We can condense this into its own function later
    statusString = "filler text"
    tempString = "temp"
    #statusString = titleTags(testdict,tags)
   
    #testing the strings
    print(statusString)
    print(tempString)
     
    api = create_api()
    api.update_status("superBot Test is up and running :D")
    since_id = 1
    while True:
        since_id = check_mentions(api, ["help", "support"], since_id)
        logger.info("Waiting...")
        time.sleep(10)
        logger.info("running functions.py\n")
        # Here are the variables needed for functions.py
        # We can condense this into its own function later
        testdict = {}
        tags = []
        projectImport(testdict)
        statusString = titleTags(testdict,tags)
       
        #test
        print(tempString)  
        
        # This can also be condensed into a function above
        if(tempString!=statusString): # Checks for change in makeros
            logger.info("Status change incoming...\n")
            api.update_status(statusString)
            tempString = statusString
        else:
            logger.info("No Changes...\n")

if __name__ == "__main__":
    main()
