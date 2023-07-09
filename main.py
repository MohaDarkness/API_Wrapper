def main():
    while(1):
        # We must take arguments somehow since this is an API, for now manually
        endPoint = input("Enter the endpoint: ")
        
        if(endPoint == "list"):
            countryCode = 0
            list(countryCode)
            continue

        if(endPoint == "weather"):
            eventId = 0
            weather(eventId)
            continue

        if(endPoint == "flights"):
            eventId = 0
            airportCode = 0
            flights(eventId, airportCode)
            continue
        
        if(endPoint == "refresh"):
            refreshDb()

        wrongEndPoint()


def list(countryCode):
    # Some logic
    pass

def weather(evenCode):
    # Some logic
    pass

def flights(eventId, airportCode):
    # Some logic
    pass

def wrongEndPoint():
    # Tell the user that end point does not exists
    pass

def refreshDb():
    # Logic to refresh the content of DB by fetching the APIs again
    assert isinstance()
    pass

if __name__ == "__main__":
    main()