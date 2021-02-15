from makeros_functions import *
import tweepy
import logging
from twitter_config import create_api #this takes the credentials exported to the venv
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def main():

    api = create_api()

    #Empty dictionary for use as a parameter for makeros_functions
    dict ={}

    # Upload image
    media = api.media_upload("./LaptopStand.jpg") #Add image path here

    # Post tweet with image, duration, title and progress
    featuredDuration = projectDuration(dict)
    featuredTitle = projectTitle(dict)
    featuredProgress = projectProg(dict)
    tweet = featuredDuration + " until we got the first prototype made for the " + featuredTitle + " project. We're currently " + str(featuredProgress) + "% completed! \U0001F389  #inworks" #Add image description here
    prompt = input("The following will be tweeted: " + tweet + " Would you like to proceed? (y/n)")
    if prompt == 'y':
        post_result = api.update_status(status=tweet, media_ids=[media.media_id])
    elif prompt == 'n':
        print("User declined")
    else:
        print("Invalid response. Will no proceed to tweet")

if __name__ == "__main__":

    main()
