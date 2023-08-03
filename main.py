from flask import *
import json
import APIs.PredictHqHandler as PredictHq
import APIs.OpenWeatherMapHandler as OpenWeatherMap
import APIs.AirLabsHandler as AirLabs
import database.SQLiteHandler as SQLiteHandler
import ErrorHandling.Exceptions as Exceptions

app = Flask(__name__)



@app.route('/', methods=["Get"])
def home():
    data_set = {"Description": "Wrapping 'PredictHq/events' & 'OpenWeatherMap' & 'AirLabs' into this one API you're using.",
                 "Creator":"https://github.com/MohaDarkness/API_Wrapper",
                 "Documentation":"https://github.com/MohaDarkness/API_Wrapper#readme"}

    return jsonify(data_set)

@app.route('/list/', methods=["Get"])
def listEvents():
    setOfArgs = {"countryCode"}
    if(setOfArgs.issubset(set(request.args))):
        countryCode = str(request.args.get('countryCode'))

        if not PredictHq.isIsoCountryCode(countryCode):
            return Exceptions.getError('CountryIsoCodeNotCorrect')
        
        databaseResults = SQLiteHandler.findEventsByCountryCode(countryCode)
        if databaseResults != None:
          return jsonify(databaseResults), 200

        return jsonify(PredictHq.getFullList(countryCode)), 200
    
    return Exceptions.getError('RequiredParametersNotProvided')

@app.route('/weather/', methods=["Get"])
def weatherOfEventLocation():
    setOfArgs = {"eventId"}
    if(setOfArgs.issubset(set(request.args))):
        eventId = str(request.args.get('eventId'))

        databaseResult = SQLiteHandler.findWeatherByEvent(eventId)
        if databaseResult != None:
          return jsonify(databaseResult), 200
        
        event = SQLiteHandler.findEventByEventId(eventId)
        if event != None:
            return OpenWeatherMap.getWeatherByEventData(event), 200
        
        PredictHq.getEventById(eventId)
        event = SQLiteHandler.findEventByEventId(eventId)
        if event != None:
            return OpenWeatherMap.getWeatherByEventData(event), 200
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
        if databaseResult != None:
            return jsonify(databaseResult), 200
        
        databaseResult = SQLiteHandler.findEventByEventId(eventId)
        if databaseResult != None:
            return AirLabs.getFLightByEventData(databaseResult, airportCode)
                    
        PredictHq.getEventById(eventId)
        databaseResult = SQLiteHandler.findEventByEventId(eventId)
        if databaseResult != None:
            return AirLabs.getFLightByEventData(databaseResult, airportCode)
           
        else:
            return Exceptions.getError('InvalidEventId')
        

    return Exceptions.getError('RequiredParametersNotProvided')


if __name__ == "__main__":
    SQLiteHandler.initialDbStructure()
    app.run(port=7777)
    
