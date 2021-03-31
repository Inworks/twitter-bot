import requests
import json
import os
from datetime import datetime, timedelta
import numpy as np

provider_id = os.getenv("PROVIDER_ID")
key = os.getenv("KEY")

url = "https://data.makeros.com/api/v1/projects"

# NOTE: These functions all take in a dictionary, make sure in your api calls
# file you have a dictionary that is used to hold all project information
#
#Downloads general and uses projBreakdown to get specific info
def projectImport(dictionary):
    #createmakerAPI()
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
            dictionary[count] = d2
            count+=1

    # Call in project breakdown to get specific project info
    projBreakdown(dictionary=dictionary)
    print("Project Load Successful\n")

#This function goes into project import to get more specific project info
def projBreakdown(dictionary):

    # This controls which projects specific information will get brought in
    # remove the 3 up to the # to get all projects
    for number in range(1, len(dictionary)+1):#len(dictionary) +1):
        print(number)
        projURL = url + "/"
        projURL = projURL + dictionary[number]['id']
        #print(projURL)

        # Below part is how you get information on individual projects
        pRequest = requests.get(projURL,params={"key":key,"provider_id":provider_id})
        if pRequest.status_code ==200:
            data = json.loads(pRequest.text)

            #This was used to make sure data came in right
            #print(type(data))

            ## This the nitty gritty that makes this dictionary usable
            d2={}
            d2.update(data['data'])

            dictionary[number] = d2

# NOTE: These functions use a list that holds tags, if you plan on using them you need a list to store tags
#
# This reads the titles and checks for tags and adds them to the list if they are not already in there
def titleTags(dictionary, tags):
    for project in dictionary:
        title = dictionary[project]['title']
        match = title.find('[')

        # If match is found
        if match != -1:
            print("Found")
            fullTag = title[match: len(title)]
            isIn = 0
            #added this to test - Danny
            sendString = "Project: "+dictionary[project]['title']+" Description: "+dictionary[project]['description']
            #print(sendString)
            #Now we return the string so we can use in our bot
            return sendString

            # Checks if tag exists and adds if it doesn't
            for i in tags:
                print(i)
                print(print(fullTag))
                if i == fullTag:
                    isIn = 1
            if isIn == 0:
                tags.append(fullTag)
        else:
            print("Not found")

    # Prints all tags in the end
    print(tags)

# This function relies on the function before it having been used. It uses the list of tags to print the descriptions of titles
# that have a tag listed.
def tagDescription(dictionary, tags):

    # Check tag presence in titles of all projects
    for i in tags:
        for project in dictionary:
            match = dictionary[project]['title'].find(i)
            print(match)

            # if there is a match print project information
            if match != -1:
                print(project)
                print(dictionary[project]['title'])
                print(dictionary[project]['description'])
            else:
                # This can be ommited later, just make sure to remove entire else statement for no errors
                print("No tag found.")

#titleTags(data,staff);

# Returns a string of the featured project in the same format as the tag tweets
def featuredProject(dictionary):
    # added project import to populate the dict properly
    #projectImport(dictionary)
    for project in dictionary:
        title = dictionary[project]['title']
        match = title.find('[featured]')

        # Match found
        if match != -1:
            print("Featured project exists")
            title = title[0:-10]
            description = dictionary[project]['description']

            # Formatted a tweet
            tweetString = "Featured Project-" + (title)+ ": " + description


            # Checks length of tweet and shortens it if necessary, can add this to other statements
            if (len(tweetString)) > 250:
                tweetString = tweetString[0:230] + "..."

            #for testing
            #print(len(tweetString))
            #print(tweetString)

            #Saw Danny added return so assumed that's what standard should be for functions that retrieve info from projects for tweets
            return tweetString

    #Will only execute if no match is found
    print("No featured project found. Please assign the \"featured\" tag to a project and run the program again")


# This function returns the 'Title' of the matching project as a string
def projectTitle(dictionary):
    # added project import to populate the dict properly
    #projectImport(dictionary)
    for project in dictionary:
        title = dictionary[project]['title']
        match = title.find('[featured]')

        # Match found
        if match != -1:
            #print("Featured project exists")
            title = title[0:-10]
            description = dictionary[project]['description']


            # returns the title as an string
            return title

#Assumes you have loaded dictionary
def downloadFile(dictionary):
    #if there's no dictionary here's where youd put request for project

    #Goes through every file in project 1, here's where you would replace 1
    # with the project you want the files for
    for thing in dictionary[1]['files']:
        print(thing)
        #print(os.getcwd())
        fileName = thing['name']
        ourCwd = "{}/{}".format(os.getcwd(), "Files")

        #Searches for folder called Files, makes if doesn't exist
        if not os.path.exists(ourCwd):
            os.mkdir(ourCwd)
        url = thing['download_url']

        #Creates file
        file_write = os.path.join(ourCwd,fileName)

        #Writes to file
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(file_write, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

#Returns string of duration of project in number of business days (from create date to update date) or hours if less than 24 hours
def projectDuration(project):
    durationString = ""
    #Converts the created_at and updated_at date strings into datetime objects we can manipulate
    date1 = datetime.strptime(project["created_at"], '%Y-%m-%d %H:%M:%S')
    date2 = datetime.strptime(project["updated_at"], '%Y-%m-%d %H:%M:%S')

    #We only need the date and not the time to calculate business days
    date1Test = date1.date()
    date2Test = date2.date()

    busDays = np.busday_count(date1Test, date2Test)

    #If there are updates within the same day, number of business days would be 0 since it took place in less than 24 hours
    #We would then want to find the number of hours
    if(busDays == 0):
        totalTime = date2 - date1
        #totalTime is a timedelta object that outputs number of days and then remaining number of hours, minutes and seconds in HH:MM:SS Format
        #Number of days is accessed through timedeltaobject.days
        #The remaining total of the  hours, minutes and seconds is accessed through timedeltaobject.seconds, all converted into seconds
        #timedeltaobject.seconds DOES NOT INCLUDE THE NUMBER OF DAYS
        #We want the total time to be outputted in number of days and hours
        #The following will make the output look better for the user

        #60 seconds in a minute, 60 minutes in an hour, rounding down to the nearest hour
        numberOfHours = int(totalTime.seconds / (60 * 60))
        #print(totalTime.days, " days and ", numberOfHours, " hours")

        #A tad more work just to avoid doing "hour(s)"
        if numberOfHours == 0:
            durationString = "less than an hour!"

        elif numberOfHours == 1:
            durationString = str(numberOfHours) + " hour"

        else:
            durationString = str(numberOfHours) + " hours"
    else:
        if busDays == 1:
            durationString = str(busDays) + " day"
        else:
            durationString = str(busDays) + " days"

    #Return durationString string object
    return durationString

#Return a list of all projects with the featured tag
def featuredProjectList(dictionary):
    # added project import to populate the dict properly
    #projectImport(dictionary)
    featuredList = []
    for project in dictionary:
        title = dictionary[project]['title']
        match = title.find('[featured]')

        # Match found
        if match != -1:
            print("Featured project exists")
            featuredList.append(dictionary[project])


    #Checks if list is empty. If it is empty, that means that no featured projects were found
    if not featuredList:
        print("No featured project found. Please assign the [featured] tag to a project and run the program again")

    return featuredList

#Checks if there is a new project with the featured tag and if so, adds it to the featured list and to do list
def checkNewFeaturedProject(dictionary, featuredList, toDoList):
    # added project import to populate the dict properly
    #projectImport(dictionary)
    for project in dictionary:
        title = dictionary[project]['title']
        match = title.find('[featured]')

        # Project with featured tag found
        if match != -1:
            #Check if project exists. If no match, that means there is a new featured project to be added
            newProj = True
            for featuredProj in featuredList:
                if featuredList[featuredProj]['title'] == dictionary[project]['title']:
                    newProj = False

            if newProj:
                print("New featured project exists")
                #Add to list of featured projects
                featuredList.append(dictionary[project])
                #Add to to-do list of featured projects
                projectToDoList = []
                for y in range(len(dictionary[project]['statuses'])):
                    if dictionary[project]['statuses'][y]['completed_at'] == None:
                        projectToDoList.append(dictionary[project]['statuses'][y])
                toDoList.append(projectToDoList)

#Return list containing list of statuses for each featured projects that are not yet completed
def getFeaturedProjectToDoList(featuredList):
    featuredProjectsToDoList = []
    #Traverse list of featured projects
    for x in range(len(featuredList)):
        specificFeaturedProjectToDoList = []
        #Traverse each project's list of statuses and checks which ones are not done
        for y in range(len(featuredList[x]['statuses'])):
            if featuredList[x]['statuses'][y]['completed_at'] == None:
                specificFeaturedProjectToDoList.append(featuredList[x]['statuses'][y])
        featuredProjectsToDoList.append(specificFeaturedProjectToDoList)
    return featuredProjectsToDoList

#Searches for new files with the [laser] tag and tweets it
def tweetLaser(testdict, api):
    for project in testdict:
        # print(testdict[project]['title'])
        # print(project)
        # print(testdict[project]['files'])
        for thing in testdict[project]['files']:
            #print(thing)
            #print(os.getcwd())
            fileName = thing['name']
            findLaser = fileName.find('[laser]')
            if findLaser != -1:
                ourCwd = "{}/{}".format(os.getcwd(), "Laser")

                #Searches for folder called Laser, makes if doesn't exist
                if not os.path.exists(ourCwd):
                    os.mkdir(ourCwd)

                laserPath = ourCwd + "/" + fileName
                #checks if file already exists
                #if file doesn't exist, then add it and tweet it
                if not os.path.exists(laserPath):
                    url = thing['download_url']

                    #Creates file
                    file_write = os.path.join(ourCwd,fileName)

                    #Writes to file
                    with requests.get(url, stream=True) as r:
                        r.raise_for_status()
                        with open(file_write, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)
                    # Upload image
                    media = api.media_upload("./Laser/" + fileName) #Add image path here

                    # Post tweet with image, duration, title and progress
                    tweetTitle = testdict[project]['title'].replace('[laser]','')
                    tweet = ("Look what we've laser cut for " + tweetTitle)
                    prompt = input("The following will be tweeted: " + tweet + " Would you like to proceed? (y/n)")
                    if prompt == 'y':
                        post_result = api.update_status(status=tweet, media_ids=[media.media_id])
                    elif prompt == 'n':
                        print("User declined")
                    else:
                        print("Invalid response. Will not proceed to tweet")

#Searches for new files with the [3d] tag and tweets it
def tweet3d(testdict, api):
    for project in testdict:
        # print(testdict[project]['title'])
        # print(project)
        # print(testdict[project]['files'])
        for thing in testdict[project]['files']:
            #print(thing)
            #print(os.getcwd())
            fileName = thing['name']
            find3d = fileName.find('[3d]')
            if find3d != -1:
                ourCwd = "{}/{}".format(os.getcwd(), "3D")

                #Searches for folder called Laser, makes if doesn't exist
                if not os.path.exists(ourCwd):
                    os.mkdir(ourCwd)

                path3d = ourCwd + "/" + fileName
                #checks if file already exists
                #if file doesn't exist, then add it and tweet it
                if not os.path.exists(path3d):
                    url = thing['download_url']

                    #Creates file
                    file_write = os.path.join(ourCwd,fileName)

                    #Writes to file
                    with requests.get(url, stream=True) as r:
                        r.raise_for_status()
                        with open(file_write, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)
                    # Upload image
                    media = api.media_upload("./3D/" + fileName) #Add image path here

                    # Post tweet with image, duration, title and progress
                    tweetTitle = testdict[project]['title'].replace('[3d]','')
                    tweet = ("Look what we've 3D printed for " + tweetTitle)
                    prompt = input("The following will be tweeted: " + tweet + " Would you like to proceed? (y/n)")
                    if prompt == 'y':
                        post_result = api.update_status(status=tweet, media_ids=[media.media_id])
                    elif prompt == 'n':
                        print("User declined")
                    else:
                        print("Invalid response. Will not proceed to tweet")
