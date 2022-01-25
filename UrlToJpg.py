#===========================================================================================
# Author: Benjamin Reelick
# Email: Benjamin.Reelick@gmail.com
# Last updated: 25/01/2022
# File description: Converts Urls to images.
#===========================================================================================
# Setup:
import requests
import os

#===========================================================================================
# Main Url to Image process:

def urlToImage(dataFilename):
    newDirectory = "Pics"
    newDirectoryPath = os.path.join(os.getcwd(), newDirectory)
    if not os.path.isdir(newDirectoryPath):
        os.mkdir(newDirectoryPath)
        print(f"New Directory {newDirectoryPath} created")

    imageData = grabUrls(dataFilename)

    os.chdir(newDirectoryPath)

    for image in imageData:
        print(image)
        f = open(str(f'{image[0]}.jpg'),'wb')
        f.write(requests.get(image[1]).content)
        f.close()

#===========================================================================================
# Grabbing urls from our data file:
def grabUrls(filename):
    if fileExistenceCheck(filename):
        with open(filename, "r") as f:
            fileData = f.readlines()[1:]
        f.close()
        redditIdUrl = []
        for i in range(len(fileData)):
            fileData[i] = fileData[i].strip("\n").split(",")
            fileData[i][1] = float(fileData[i][1])
            redditIdUrl.append([fileData[i][1], fileData[i][2]])
        return redditIdUrl

def fileExistenceCheck(filename):
    '''Checks if the given file exists.'''
    return os.path.isfile(filename)

#===========================================================================================
