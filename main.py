#===========================================================================================
# Author: Benjamin Reelick
# Email: Benjamin.Reelick@gmail.com
# Last updated: 25/01/2022
# File description: Main file for CUTEANIMALPICTURES process.
#===========================================================================================
# Setup:
from RedditScrapper import catImageS
import praw
from UrlToJpg import urlToImage

#===========================================================================================
# Main:

def main():
    filename='PicURLs.csv'
    catsInstance = redditIn()
    catImageS(catsInstance, 5, filename)
    #deleteFile(filename)
    urlToImage(filename)

#===========================================================================================
# Reddit class:

class redditIn:
    '''Class for a reddit user instance.'''
    def __init__(self, client_id='kyuTgV9ra6nCzDUnp3Dg9A', 
            client_secret='ht0lNwisfQVN7CgZ6npe3i0Sy1hY5A', 
            user_agent='my user agent'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.reddit = praw.Reddit(
            client_id = self.client_id,
            client_secret = self.client_secret,
            user_agent = self.user_agent,
            ratelimit_seconds = 200
            )

#===========================================================================================
# Main function call:
main()