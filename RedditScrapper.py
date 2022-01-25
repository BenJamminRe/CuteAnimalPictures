#===========================================================================================
# Author: Benjamin Reelick
# Email: Benjamin.Reelick@gmail.com
# Last updated: 25/01/2022
# File description: Reddit image scrapper process with basic file storage.
#
# What it can do: Uses reddit praw package to scrape subreddits for image urls.
# - you can specify what subreddit through .subreddit(' ') method in a redditIn function call.
# - you can specify the MAX amount of images you want to scrape through the nImages variable in the catImageS function. 
#   Note: if there are not enough posts on the subreddit with images in them you may not complete the quota or even get near it.
# - you can specify what trending page you want to scrape through the .top(' ') method in a redditIn function call.
#===========================================================================================
# Setup 

import praw
import os

#===========================================================================================
# Main image scrapper function # 

def catImageS(redditIn, nImages, filename='CatPicURLs.csv'):
    '''Adds a specified amount of cat picture URLs from Reddit
    to a named file; which would be created if it does not already exist.'''
    
    # Initial variables
    oldSubmissions = []
    checkData = []
    fileExistence = fileExistenceCheck(filename)

    # If our animal pictiure url file already exists; add the reddit post id's to checkData
    # so that we can make sure there are no duplicates.
    if fileExistence:
        with open(filename, "r") as f:
            oldSubmissions = f.readlines()[1:]
        f.close()
        checkData = []
        for i in range(len(oldSubmissions)):
            oldSubmissions[i] = oldSubmissions[i].strip("\n").split(",")
            oldSubmissions[i][1] = float(oldSubmissions[i][1])
            checkData.append([oldSubmissions[i][0], float(oldSubmissions[i][1])])

    # Grabbing reddit post picture urls (if they have them and if they are not already in our file).
    submissionData = getSubmissions(redditIn, nImages, checkData)

    # If our file exists already, add on the old files to the new.
    if fileExistence:
        submissionData.extend(oldSubmissions)

    # Sort the joined data.
    submissionSortedData = sorted(submissionData, key = lambda x: x[1])

    # Write all the new urls to our file (automatically making one if it doesn't yet exist).
    with open(filename, "w") as f:
        f.write("submissionID,timeCreatedUnix,url")
        for submission in submissionSortedData:
            f.write("\n{},{},{}".format(submission[0], submission[1], submission[2]))
        f.close()

#===========================================================================================
# File functions #

def checkKey(filename):
    '''Finds the last used key value plus 1 in the cat picture url file'''
    with open(filename, 'rb') as f:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        last_line = f.readline().decode()
    f.close()
    key = last_line.split(",")[0]
    return int(key) + 1

def deleteFile(filename):
    '''Deletes specified file'''
    os.remove(filename)
    print("File Removed!")

def fileExistenceCheck(filename):
    '''Checks if the given file exists.'''
    return os.path.isfile(filename)
    
def checkInFile(id, timeCreated, checkData):
    '''Checks if the url is already in our file'''
    for submission in checkData:
        if id == submission[0] and timeCreated == checkData[1]:
            return True
    return False

#===========================================================================================

def getSubmissions(redditIn, nImages, checkData):
    '''Gets reddit submission instances from the cats subreddit top week page.'''
    submissionData = []
    count = 0
    for submission in redditIn.reddit.subreddit('cats').top("week", limit=None):
        url = submission.url
        id = submission.id
        timeCreated = submission.created
        if count >= nImages:
            break
        elif url.endswith(('.jpg', '.png', '.gif', '.jpeg')) and not checkInFile(id, timeCreated, checkData):
            submissionData.append([id, timeCreated, url])
            count += 1
    return submissionData

#===========================================================================================
