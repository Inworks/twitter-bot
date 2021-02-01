import tweepy
import os
import requests
import json

#from functions import *

url = "https://data.makeros.com/api/v1/projects"

allProj = {}
print("Loading projects")
#projectImport(allProj)

#Retrieve provider_id and key from computer to access MakerOS API
provider_id = os.getenv("PROVIDER_ID")
key = os.getenv("KEY")
print(provider_id)
print(key)

#Request access to MakerOS API using the provider_id and key acquired
r = requests.get(url,params={"key":key,"provider_id":provider_id})

# We print the status for testing purposes
# print("Status code: {}".format(r.status_code))

if r.status_code == 200:

    # Here we load the json string into a python list

    data = json.loads(r.text)
    count = 1
    ## This the nitty gritty that makes this dictionary usable
    for i in data['data']:
        d2 = {}
        d2.update(i)
        allProj[count] = d2
        count+=1

# Call in project breakdown to get specific project info
#projBreakdown(dictionary=dictionary)

# This controls which projects specific information will get brought in
# remove the 3 up to the # to get all projects
for number in range(1, 3):#len(dictionary) +1):
    print(number)
    projURL = url + "/"
    projURL = projURL + allProj[number]['id']
    #print(projURL)

    # Below part is how you get information on individual projects
    pRequest = requests.get(projURL,params={"key":key,"provider_id":provider_id})
    if pRequest.status_code ==200:
        print("Access good")
        data = json.loads(pRequest.text)

        #This was used to make sure data came in right
        #print(type(data))

        ## This the nitty gritty that makes this dictionary usable
        d2={}
        d2.update(data['data'])

        allProj[number] = d2

print("Project Load Successful\n")
