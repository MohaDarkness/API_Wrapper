from flask import *
import json
from PredictHqHandler import predictHqTest
from OpenWeatherMapHandler import openWeatherMapTest
from AirLabsHandler import airLabsTest

app = Flask(__name__)

@app.route('/', methods=["Get"])
def home():
    # return a small documentation of how to use the API
    data_set = {"Page": "Home", "Message":"Mohannad Atmeh's API Wrapping assesment"}
    json_dump = json.dumps(data_set)

    return json_dump

@app.route('/list/', methods=["Get"])
def listEvents():
    countryCode = str(request.args.get('countryCode'))

    data_set = {"Page": "Request", "Message":'List of events must be visible in this route'}
    json_dump = json.dumps(data_set)

    print(predictHqTest())

    return json_dump

@app.route('/weather/', methods=["Get"])
def weatherOfEventLocation():
    eventId = str(request.args.get('eventId'))

    data_set = {"Page": "Request", "Message":'This route tell you the weather of the location of a speccifec event'}
    json_dump = json.dumps(data_set)

    print(openWeatherMapTest())

    return json_dump

@app.route('/flights/', methods=["Get"])
def flightsToEventLocation():
    eventId = str(request.args.get('eventId'))
    airportCode = str(request.args.get('airportCode'))

    data_set = {"Page": "Request", "Message":'This rout lists flights from the users airport to the event destination'}
    json_dump = json.dumps(data_set)

    print(airLabsTest())

    return json_dump



if __name__ == "__main__":
    app.run(port=7777)