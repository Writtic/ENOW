#!/usr/bin/python
#-​*- encoding: utf-8 -*​-

import json
import requests

def lambda_handler(event, context):
    # TODO implement

    for element in event:

        dictionary = {"username" : "",\
        "text" : ""}

        dictionary["username"] = element["id"]
        dictionary["text"] = element["selftext"]

        request.post('',\
        data = json.dumps(dictionary))


    return event
