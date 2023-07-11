from flask import *
import json
import PredictHqHandler
import OpenWeatherMapHandler
import AirLabsHandler
import SQLiteHandler
import Exceptions

app = Flask(__name__)



@app.route('/', methods=["Get"])
def home():
    print(set(request.args))
    # return a small documentation of how to use the API
    data_set = {"Page": "Home", "Message":"Mohannad Atmeh's API Wrapping assesment"}
    json_dump = json.dumps(data_set)
    SQLiteHandler.insertData()
    SQLiteHandler.fetchAllData()

    return json_dump

@app.route('/list/', methods=["Get"])
def listEvents():
    setOfArgs = {"countryCode"}
    if(setOfArgs.issubset(set(request.args))):
        countryCode = str(request.args.get('countryCode'))

        if not PredictHqHandler.isIsoCountryCode(countryCode):
            return Exceptions.getError('CountryIsoCodeNotCorrect')
        
        databaseResults = SQLiteHandler.findEventsByCountryCode(countryCode)
        if len(databaseResults) > 0:
          return jsonify(databaseResults), 200

        return jsonify(PredictHqHandler.getFullList(countryCode)), 200
    
    return Exceptions.getError('RequiredParametersNotProvided')

@app.route('/weather/', methods=["Get"])
def weatherOfEventLocation():
    setOfArgs = {"eventId"}
    if(setOfArgs.issubset(set(request.args))):
        eventId = str(request.args.get('eventId'))

        databaseResult = SQLiteHandler.findWeatherByEvent(eventId)
        if len(databaseResult) > 0:
          return jsonify(databaseResult), 200
        
        databaseResult = SQLiteHandler.findEventByEventId(eventId)
        if len(databaseResult) > 0:
            return OpenWeatherMapHandler.getWeatherByEventData(databaseResult[0]), 200
        
        PredictHqHandler.getEventById(eventId)
        databaseResult = SQLiteHandler.findEventByEventId(eventId)
        if len(databaseResult) > 0:
            return OpenWeatherMapHandler.getWeatherByEventData(databaseResult[0]), 200
        else:
            return Exceptions.getError('InvalidEventId')

    return Exceptions.getError('RequiredParametersNotProvided')

@app.route('/flights/', methods=["Get"])
def flightsToEventLocation():
    setOfArgs = {"airportCode", "eventId"}
    if(setOfArgs.issubset(set(request.args))):
        eventId = str(request.args.get('eventId'))
        airportCode = str(request.args.get('airportCode'))

        databaseResult = SQLiteHandler.findFlight(eventId, airportCode)
        if len(databaseResult) > 0:
            return jsonify(databaseResult), 200
        
        databaseResult = SQLiteHandler.findEventByEventId(eventId)
        if len(databaseResult) > 0:
            goFlight, backFlight = AirLabsHandler.getFLightByEventData(databaseResult[0], airportCode)
            return goFlight #the back flight is not returned!!!
                
        PredictHqHandler.getEventById(eventId)
        databaseResult = SQLiteHandler.findEventByEventId(eventId)
        if len(databaseResult) > 0:
            goFlight, backFlight = AirLabsHandler.getFLightByEventData(databaseResult[0], airportCode)
            return goFlight #the back flight is not returned!!!
        else:
            return Exceptions.getError('InvalidEventId')
        

    return Exceptions.getError('RequiredParametersNotProvided')


if __name__ == "__main__":
    SQLiteHandler.initialDbStructure()
    app.run(port=7777)
    
