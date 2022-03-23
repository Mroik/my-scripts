#!/bin/python

import requests
import json

endpoint = "https://it.global.nba.com/stats2/season/conferencestanding.json?locale=it"

data = requests.get(endpoint).json()["payload"]["standingGroups"]
east = data[0]["teams"]
west = data[1]["teams"]

east_standings = []
west_standings = []

for team in east:
    east_standings.append({
        "rank": team["standings"]["confRank"],
        "team": team["profile"]["name"]
    })

for team in west:
    west_standings.append({
        "rank": team["standings"]["confRank"],
        "team": team["profile"]["name"]
    })

for x in range(len(east)-1):
    for y in range(x+1,len(east)):
        if east_standings[x]["rank"] > east_standings[y]["rank"]:
            z = east_standings[x]
            east_standings[x] = east_standings[y]
            east_standings[y] = z

for x in range(len(west)-1):
    for y in range(x+1,len(west)):
        if west_standings[x]["rank"] > west_standings[y]["rank"]:
            z = west_standings[x]
            west_standings[x] = west_standings[y]
            west_standings[y] = z

print("EAST")
for x in east_standings:
    print("{} {}".format(x["rank"], x["team"]))

print("\nWEST")
for x in west_standings:
    print("{} {}".format(x["rank"], x["team"]))
