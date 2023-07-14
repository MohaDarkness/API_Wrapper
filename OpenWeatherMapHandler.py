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

    sendToDatabase(eventId, response.json())
    return response.json()


def getWeatherByEventData(jsonData):
    eventId = jsonData["id"]
    location = jsonData['location']
    lat = location[1]
    lon = location[0]
    return getWeather(lat, lon, eventId)