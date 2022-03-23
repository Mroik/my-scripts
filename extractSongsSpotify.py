#!/bin/python

import requests
import sys

endpoint = "https://api.spotify.com/v1/playlists/"
endpoint += sys.argv[1]
endpoint += "?fields=tracks.items"

token = "Bearer <REPLACE ME>"

req = requests.get(endpoint, headers={
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": token
})
resp = req.json()

for tracks in resp["tracks"]["items"]:
    print(tracks["track"]["external_urls"]["spotify"])
