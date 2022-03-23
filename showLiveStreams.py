#!/bin/python

#Visit https://id.twitch.tv/oauth2/authorize?client_id=REPLACE_ME&redirect_uri=http://localhost&response_type=token&scope=user:edit

import requests
import sys

clientID = "REPLACE ME"
oauth = "Bearer <REPLACE ME>"

header = {
        "Client-Id":        clientID,
        "Authorization":    oauth
}

#Get user ID
endpoint = "https://api.twitch.tv/helix/users?login="
endpoint += sys.argv[1]

req = requests.get(endpoint, headers = header)
userID = req.json()["data"][0]["id"]

#Get following
endpoint = "https://api.twitch.tv/helix/users/follows?from_id="
endpoint += userID
endpoint += "&first=100"

req = requests.get(endpoint, headers = header)
following = req.json()["data"]

#Prepare streams request
endpoint = "https://api.twitch.tv/helix/streams?first=100&"
for users in following:
    endpoint += "user_id=" + users["to_id"] + "&"

#Request streams (Works only if prepared up to 100 users)
req = requests.get(endpoint, headers = header)
for x in req.json()["data"]:
    print(x["user_name"])
