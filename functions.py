import requests
import json
import os

provider_id = os.getenv("PROVIDER_ID")
key = os.getenv("KEY")

url = "https://data.makeros.com/api/v1/projects"
#provider_id = "Kx0npmsi8l8jUf7rl7dNlLLJthNS7PNbKSh5M0coSmPZKNiDxIFpPLswVSZVhQJZ"
#key = "aGTpc6ExIlXU7lib91Wq9KaZlu4JHlr3DEVdq82NMML78Bpw7xVHaLzzvVXwu9GW"

#NOTE These functions all take in a dictionary, make sure in your api calls
# file you have a dictionary that is used to hold all project information

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
    for number in range(1, 3):#len(dictionary) +1):
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

#NOTE These functions use a list that holds tags, if you plan on using them you need a list to store tags

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
    projectImport(dictionary)
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
            print(tweetString)

            #Saw Danny added return so assumed that's what standard should be for functions that retrieve info from projects for tweets
            return tweetString

    #Will only execute if no match is found
    print("No featured project found. Please assign the \"featured\" tag to a project and run the program again")

# Returns an integer of the featured project current progress 0-100
def projectProg(dictionary):
    # added project import to populate the dict properly
    projectImport(dictionary)
    for project in dictionary:
        title = dictionary[project]['title']
        match = title.find('[featured]')
        prog = dictionary[project]['progress']

        # Match found
        if match != -1:
            print("Featured project exists")
            title = title[0:-10]
            description = dictionary[project]['description']


            # returns the progress percentage as an integer
            return prog

# This function returns the 'Title' of the matching project
def projectTitle(dictionary):
    # added project import to populate the dict properly
    projectImport(dictionary)
    for project in dictionary:
        title = dictionary[project]['title']
        match = title.find('[featured]')

        # Match found
        if match != -1:
            print("Featured project exists")
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
