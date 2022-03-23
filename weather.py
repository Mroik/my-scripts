#!/bin/python
import requests

key = "<REPLACE ME>"
lat = "45.462889"
lon = "9.0376503"

req = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&appid={}".format(lat, lon, key))
data = req.json()

print("Weather: ", end="")
for x in data["current"]["weather"]:
    print(x["main"], end=" ")
print()
print("Temperature: {} ˚C".format(data["current"]["temp"]))
