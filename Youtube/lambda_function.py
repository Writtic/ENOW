import json
import boto3
import urllib2
from pytube import YouTube


def lambda_handler(event, context):
    youtube_url = event.get('url', None)
    if youtube_url is None:
        return
    yt = YouTube(youtube_url)
    video = yt.filter('mp4')[-1]
    if not video:
        # TODO: Raise exception
        return
    return {
        "text": "video is " + video
    }
