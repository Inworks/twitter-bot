#!/usr/bin/env python

from functions import *
import tweepy
import logging
from config import create_api #this takes the credentials exported to the venv
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

int statcounter=0

def main():
    
    testdict = {}
    tags = []
    statusString = "filler text"
    tempString = "temp"
    projectImport(testdict)
    statusString = titleTags(testdict,tags)
    
    api = create_api()
    api.update_status(statusString)
    while True:
        logger.info("Waiting...")
        time.sleep(60)
        tempString = titleTags(testdict,tags)
        if(tempString!=statusString):
            logger.info("Status change incoming...\n")
            api.update_status(tempString)
            statusString = tempString
            tempString = "temp"

if __name__ == "__main__":
    main()
