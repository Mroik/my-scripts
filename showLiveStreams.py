#!/bin/python

#Visit https://id.twitch.tv/oauth2/authorize?client_id=REPLACE_ME&redirect_uri=http://localhost&response_type=token&scope=user:read:follows

import requests
import sys

clientID = "REPLACE_ME"
oauth = "Bearer REPLACE_ME"

header = {
        "Client-Id":        clientID,
        "Authorization":    oauth
}

# Get user ID
endpoint = "https://api.twitch.tv/helix/users?login="
endpoint += sys.argv[1]

req = requests.get(endpoint, headers=header)
userID = req.json()["data"][0]["id"]

# Get currently streaming
endpoint = "https://api.twitch.tv/helix/streams/followed?user_id={}".format(userID)
endpoint += "&first=100"
req = requests.get(endpoint, headers=header)
for x in req.json()["data"]:
    print(x["user_name"])
