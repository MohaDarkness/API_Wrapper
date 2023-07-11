from flask import jsonify
errors = {
    'RequiredParametersNotProvided': {
        'message' : "RequiredParametersNotProvided:: Some of the required parameters wasn't provided through the request!",
        'status'  : 400
    },
    'CountryIsoCodeNotCorrect' : {
        'message' : "CountryIsoCodeNotCorrect:: The iso_3166_1 country code provided does not exist!",
        'status'  : 400
    },
    'InvalidEventId' : {
        'message' : "InvalidEventId:: The event ID entered is not in any database!",
        'status'  : 400
    }
}

def getError(errorTitle):
    body = errors[errorTitle]
    status = body['status']
    return jsonify(body),status