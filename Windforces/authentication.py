#!/usr/bin/python
#-​*- encoding: utf-8 -*​-

# praw(reddit api in python)
import praw
import re
import getpass
import json
import time

from pprint import pprint

# boto3(aws sdk library in python)
import boto3

def main():

    array=[]
    # identification credentials for reddit
    identification = input("Enter an id")
    # password for the account
    password = getpass.getpass("Enter the password")
    # requesting authentication for AWS lambda function(AWS_IAM)
    client = boto3.client('lambda',\
    aws_access_key_id = '',\
    aws_secret_access_key = '')

    # initializing reddit class object
    resource = praw.Reddit("For checking new stuffs on PCMasterRace")
    # provide login credentials
    resource.login(username=identification, password=password)

    while True:
        # retrieving subreddit information
        subreddit = resource.get_subreddit('pcmasterrace')
        # getting top 10 submission for the subreddit
        for submission in subreddit.get_hot(limit=10):
            # setting up dictionary per submission
            dictionary = {\
            'id':'',\
            'selftext':''\
            }
            msg = '[PRAW related thread](%s)' % submission.short_link
            dictionary['id'] = msg
            dictionary['selftext']=submission.selftext
            # concatenating all the dictionary
            array.append(dictionary)

        # invoking remote lambda function
        response = client.invoke(\
        FunctionName = '',\
        Payload = json.dumps(array))
        del array[:]
        pprint(response)
        # repeating iteration every 5 seconds
        time.sleep(5)

if __name__ == '__main__':
    main()
