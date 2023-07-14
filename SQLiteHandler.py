import sqlite3
import json
import time


def makeConnection():
    connection = sqlite3.connect("events.db")
    return connection
    
    
def closeConnection(connection):
    connection.commit()
    connection.close()

def initialEventsTableStructure():
    connection = makeConnection()
    cursor = connection.cursor()
    try:
        fetchedData = cursor.execute("SELECT * FROM Events")
        print("@@@SQLite: Table 'Events' already exists..")

    except:
        cursor.execute("CREATE TABLE Events (eventId TEXT, country TEXT, eventData JSON, time INTEGER)")
        print("@@@SQLite: Table 'Events' had been created..")
        
    
    closeConnection(connection)

def initialEventsWeatherTableStructure():
    connection = makeConnection()
    cursor = connection.cursor()

    try:
        fetchedData = cursor.execute("SELECT * FROM Events_Weather")
        print("@@@SQLite: Table 'Events_Weather' already exists..")

    except:
        cursor.execute("CREATE TABLE Events_Weather (eventId TEXT, weather JSON, time INTEGER)")
        print("@@@SQLite: Table 'Events_Weather' had been created..")
        
    
    closeConnection(connection)


def initialEventFlightTableStructure():
    connection = makeConnection()
    cursor = connection.cursor()

    try:
        fetchedData = cursor.execute("SELECT * FROM Event_Flight")
        print("@@@SQLite: Table 'Event_Flight' already exists..")
        

    except:
        cursor.execute("CREATE TABLE Event_Flight (eventId TEXT, depIATA TEXT, flightsSchedule JSON, time INTEGER)")
        print("@@@SQLite: Table 'Event_Flight' had been created..")
    
    closeConnection(connection)



def initialDbStructure():
    initialEventsTableStructure()
    initialEventsWeatherTableStructure()
    initialEventFlightTableStructure()


def insertEvent(id, country, data):
    dataToInsert = (id, country, json.dumps(data), time.time())
    connection = makeConnection()
    cursor = connection.cursor()
    cursor.execute("insert into Events values (?,?,?,?)", dataToInsert)
    closeConnection(connection)


def insertEventFlight(id, userIATA, flightsSchedule):
    dataToInsert = (id, userIATA, json.dumps(flightsSchedule), time.time())
    connection = makeConnection()
    cursor = connection.cursor()
    cursor.execute("insert into Event_Flight values (?,?,?,?)", dataToInsert)
    closeConnection(connection)


def insertEventWeather(eventId, weather):
    dataToInsert = (eventId, json.dumps(weather), time.time())
    connection = makeConnection()
    cursor = connection.cursor()
    cursor.execute("insert into Events_Weather values (?,?,?)", dataToInsert)
    closeConnection(connection)


def findEventsByCountryCode(countryCode):
    connection = makeConnection()
    cursor = connection.cursor()
    result_list = cursor.execute(f"SELECT eventData FROM Events WHERE country = \"{countryCode.upper()}\" AND time>{time.time() - 21600}")
    result_list = [json.loads(row[0]) for row in cursor.fetchall()]
    result_list = None if len(result_list) == 0 else result_list
    closeConnection(connection)
    return result_list

def findAnElement(query):
    connection = makeConnection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query)
    result = [json.loads(row[0]) for row in cursor.fetchall()]
    result = None if result == [] else result[0]
    closeConnection(connection)
    return result

def findEventByEventId(eventId):
    return findAnElement(f"SELECT eventData FROM Events WHERE eventId = \"{eventId}\" AND time>{time.time() - 21600}")


def findWeatherByEvent(eventId):
    return findAnElement(f"SELECT weather FROM Events_Weather WHERE eventId = \"{eventId}\" AND time>{time.time() - 21600}")

def findFlight(eventId, IATA):
    return findAnElement(f"SELECT flightsSchedule FROM Event_Flight WHERE eventId = \"{eventId}\" AND depIATA =\"{IATA}\" AND time>{time.time() - 21600}")


# test wise #########
def fetchAllData():
    connection = makeConnection()
    cursor = connection.cursor()
    fetchedData = cursor.execute("SELECT * FROM Events")
    for row in fetchedData:
        print(row)
    print("Here is the inserted data!")
    closeConnection(connection)
######################