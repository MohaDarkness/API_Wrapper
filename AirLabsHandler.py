import requests
import json
from SQLiteHandler import insertEventFlight

API_KEY = "98edecdb-9074-4b95-83b6-c003feb19e58"

def sendDatatoDatabase(eventId, userIATA, goFlight, backFlight):
    insertEventFlight(eventId, userIATA, goFlight, backFlight)



def getFlightByIATAs(eventId, usersIATA, destIATA):
    params = {
        'api_key': API_KEY,
        'dep_iata': usersIATA,
        'arr_iata': destIATA,
    }
    method = 'ping'
    api_base = 'http://airlabs.co/api/v9/schedules'
    api_result = requests.get(api_base+method, params)
    goFlight = api_result.json()
    
    params = {
        'api_key': API_KEY,
        'dep_iata': destIATA,
        'arr_iata': usersIATA,
    }
    method = 'ping'
    api_base = 'http://airlabs.co/api/v9/schedules'
    api_result = requests.get(api_base+method, params)
    backFlight = api_result.json()

    sendDatatoDatabase(eventId, usersIATA, goFlight, backFlight)

    return (goFlight, backFlight)


def getFLightByEventData(event, usersIATA):
    print(event)
    # event = json.loads(event)
    print("this is 'event' data type:", type(event))
    eventId = event['id']
    geo = event['geo']
    lat = geo['coordinates'][0]
    lng = geo['coordinates'][1]

    params = {
        'api_key': API_KEY,
        'lat': lat,
        'lng': lng,
        'distance':200
    }
    method = 'ping'
    api_base = 'http://airlabs.co/api/v9/nearby'
    api_result = requests.get(api_base+method, params)

    api_response = api_result.json()
    destinationIATA = api_response["airports"][0]['iata_code']
    return getFlightByIATAs(eventId, usersIATA, destinationIATA)

