from makeros_functions import *
import tweepy
import logging
from twitter_config import create_api #this takes the credentials exported to the venv
import time
 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def main():

    api = create_api()    

    # Upload image
    media = api.media_upload("./LaptopStand.jpg") #Add image path here

    # Post tweet with image
    # will add Asia's function here and place resulting string in tweet.
    tweet = "It took us <Asia's func> to get our first prototype!  #inworks" #Add image description here
    post_result = api.update_status(status=tweet, media_ids=[media.media_id])

if __name__ == "__main__":

    main()
