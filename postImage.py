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

    # Post tweet with image and duration
    durationString = projectDuration(dict)
    tweet = "It took us " + durationString + " to get our first prototype!  #inworks" #Add image description here
    post_result = api.update_status(status=tweet, media_ids=[media.media_id])

if __name__ == "__main__":

    main()
