
# coding: utf-8



#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from urlparse import parse_qs
import shlex
import argparse


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyCNvlc8dQVAEoKzINru5YkCYL_0NHgDmOo"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def lambda_handler(event, context):
    req_body = event['body']
    params = parse_qs(req_body)
    finding = params['text'][0]
    argString = '--q --max-results 5'
    index = argString.find('--max')
    final_arg = argString[:index] + finding + ' ' + argString[index:]

    argparser = argparse.ArgumentParser( conflict_handler='resolve')
    argparser.add_argument("--q", help="Search term", default="Google")
    argparser.add_argument("--max-results", help="Max results", default=25)
    options = argparser.parse_args(shlex.split(final_arg))
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
      developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
      q=options.q,
      part="id,snippet",
      maxResults=options.max_results
    ).execute()

    videos = []
    tokens = []
    names = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s VIDID:(%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["videoId"]))
    print "Videos:\n", "\n".join(videos)
    for i in range(0,len(videos)):
        token = videos[i].find('VIDID:(')
        names.append(videos[i][0:token])
        tokens.append("https://youtube.com/watch?v="+ videos[i][token+7:-1])

    return {
        "response_type": "in_channel",
        "attachments": [
            {
                "text": "videos are here : \n" + "\n".join(tokens),
                "color": "#7CD197"
            }
        ]
    }
