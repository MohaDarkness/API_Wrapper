import requests
import json
from SQLiteHandler import insertEventWeather

API_KEY = "f22892654725839a44ff6db985f0b151"

def sendToDatabase(eventId, weather):
    insertEventWeather(eventId, weather)

def getWeather(lat, lon, eventId):
    response = requests.get(
        url=f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&exclude=hourly,daily&appid={API_KEY}"
    )

    sendToDatabase(eventId, response)
    return response.json()


def getWeatherByEventData(jsonData):
    print(type(jsonData))
    dataDict = json.loads(jsonData)
    eventId = dataDict["id"]
    geo = dataDict['geo']
    lat = geo['coordinates'][0]
    lon = geo['coordinates'][1]
    return getWeather(lat, lon, eventId)