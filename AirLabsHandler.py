import requests
import json
from SQLiteHandler import insertEventFlight

API_KEY = "98edecdb-9074-4b95-83b6-c003feb19e58"

def sendDatatoDatabase(eventId, userIATA, flightsSchedule):
    insertEventFlight(eventId, userIATA, flightsSchedule)



def getFlightByICAOs(usersICAO, destICAOs, dep = True):
    d = "dep" if dep else "arr"
    params = {
        'api_key': API_KEY,
        f'{d}_icao': usersICAO,
    }
    
    method = 'schedules.json'
    api_base = 'http://airlabs.co/api/v9/'
    api_result = requests.get(api_base+method, params).json()
    # return api_result
    flights = api_result["response"]
    flightSchedule = {"flight_found":False, "data":None}
    for flight in flights:
        try:
            if flight["arr_icao"] in destICAOs:
                flightSchedule["flight_found"] = True
                flightSchedule["data"] = flight
                break
        except:
            continue

    return flightSchedule

def findGoAndBackFlights(eventId, usersICAO, destICAOS):
    flightsSchedule = {"goFlight":None, "backFlight":None}
    flightsSchedule["goFlight"] = getFlightByICAOs(usersICAO, destICAOS, True)
    flightsSchedule["backFlight"] = getFlightByICAOs(usersICAO, destICAOS, False)
    sendDatatoDatabase(eventId, usersICAO, flightsSchedule)

    return flightsSchedule


def getFLightByEventData(event, usersICAO):
    eventId = event['id']
    location = event["location"]
    lng = location[0]
    lat = location[1]

    params = {
        'api_key': API_KEY,
        'lat': lat,
        'lng': lng,
        'distance':200
    }
    method = 'nearby.json'
    api_base = 'http://airlabs.co/api/v9/'
    api_result = requests.get(api_base+method, params)

    api_response = api_result.json()
    jsonAirports = api_response["response"]["airports"]
    destAirports = []
    for airport in jsonAirports:
        try:
            destAirports.append(airport["icao_code"])
        except:
            continue
    return findGoAndBackFlights(eventId, usersICAO, destAirports)

