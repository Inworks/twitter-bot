#!/usr/bin/env python

from makeros_functions import *
import tweepy
import logging
from twitter_config import create_api #this takes the credentials exported to the venv
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

#Test commit - danny
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
                status="Please reach us via DM or visit us at https://linktr.ee/inworks/",
                in_reply_to_status_id=tweet.id,
            )
# This is supposed to reply to a tweet as a comment when someone @ the bot
# at the moment this only works if someone Tweets, if someone comments on our tweets the bot tweets out the response, working on a fix
    return new_since_id

# Here is an attempt at making the status change a function
#def statusChange(string):

def main():
    # Here are the variables needed for functions.py
    # We can condense this into its own function later
    #statusString = titleTags(testdict,tags)

    testdict = {}
    projectImport(testdict)

    #This is how we will check for changes
    #We store an instance when the bot starts and continually compare it to an updated and current one
    initialFeaturedProjects = []
    initialFeaturedProjects = featuredProjectList(testdict)
    #print(initialFeaturedProjects)
    featuredProjectsToDoList = []
    featuredProjectsToDoList = getFeaturedProjectToList(initialFeaturedProjects)
    #print(featuredProjectsToDoList)


    api = create_api()
    #api.update_status("superBot Test is up and running :D")
    since_id = 1
    while True:
        #since_id = check_mentions(api, ["what","up","joe","hello","hey","hi","yo","help", "support"], since_id) #disabled for now
        logger.info("Waiting...")
        time.sleep(20) #This is our delay in seconds
        logger.info("running functions.py\n")
        # We can condense this into its own function later

        #This is the updated and current list. We will need to constantly update the list in order to find changes
        projectImport(testdict)
        updatedFeaturedProjects = []
        updatedFeaturedProjects = featuredProjectList(testdict)

        #print(featuredProjectsToDoList)
        #Iterate through the to-do list to see if any have been updated
        #First loop will iterate through list of featured projects
        for x in range(len(featuredProjectsToDoList)):
            #print("first loop")
            #Second loop will iterate through specific project's statuses that have not been completed
            for y in range(len(featuredProjectsToDoList[x])):
                #print("second loop")
                #Find index of to-do status so we can reference it in the updated list
                testIndex = 0
                for a in range(len(updatedFeaturedProjects[x]['statuses'])):
                    if(updatedFeaturedProjects[x]['statuses'][a]['status'] == featuredProjectsToDoList[x][y]['status']):
                        testIndex = a
                        #print(testIndex)
                #print(testIndex)
                #print(updatedFeaturedProjects[x]['statuses'][testIndex]['completed_at'])
                #Check if item is complete
                if updatedFeaturedProjects[x]['statuses'][testIndex]['completed_at'] != None:
                    logger.info("Change in progress!!!\n")
                    #Tweet
                    #The .replace removes the [featured] tag from the tweet
                    tweetTitle = updatedFeaturedProjects[x]['title'].replace('[featured]','')
                    tweetStatus = updatedFeaturedProjects[x]['statuses'][testIndex]['status']
                    tweetProgress = str(updatedFeaturedProjects[x]['progress'])
                    tweetDuration = str(projectDuration(updatedFeaturedProjects[x]))
                    tweet = ("Update on " + tweetTitle + ": The team just completed \"" + tweetStatus +
                                "\" and is " + tweetProgress + "% complete! \U0001F389 So far this project has taken "
                                 + tweetDuration + " days.")
                    #print(tweet)

                    prompt = input("The following will be tweeted: " + tweet + " Would you like to proceed? (y/n)")
                    if prompt == 'y':
                        post_result = api.update_status(status=tweet)
                        print("Status has been tweeted!")
                    elif prompt == 'n':
                        print("User declined")
                    else:
                        print("Invalid response. Will not proceed to tweet")
                    #api.update_status(tweet)
                    #Remove item from to-do list
                    del featuredProjectsToDoList[x][y]
                    #print(featuredProjectsToDoList)
                    break #To prevent an out of bounds error since list will be smaller after removal

if __name__ == "__main__":
    main()
