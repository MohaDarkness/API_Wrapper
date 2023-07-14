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

    except:
        cursor.execute("CREATE TABLE Events (eventId TEXT, country TEXT, eventData JSON, time INTEGER)")
        
    
    closeConnection(connection)

def initialEventsWeatherTableStructure():
    connection = makeConnection()
    cursor = connection.cursor()

    try:
        fetchedData = cursor.execute("SELECT * FROM Events_Weather")

    except:
        cursor.execute("CREATE TABLE Events_Weather (eventId TEXT, weather JSON, time INTEGER)")
        
    
    closeConnection(connection)


def initialEventFlightTableStructure():
    connection = makeConnection()
    cursor = connection.cursor()

    try:
        fetchedData = cursor.execute("SELECT * FROM Event_Flight")
        

    except:
        cursor.execute("CREATE TABLE Event_Flight (eventId TEXT, depIATA TEXT, goFligh JSON, backFligh JSON, time INTEGER)")
    
    closeConnection(connection)



def initialDbStructure():
    initialEventsTableStructure()
    initialEventsWeatherTableStructure()
    initialEventFlightTableStructure()


def insertEvent(id, country, data):
    dataToInsert = (id, country, data, time.time())
    connection = makeConnection()
    cursor = connection.cursor()
    cursor.execute("insert into Events values (?,?,?,?)", dataToInsert)
    closeConnection(connection)


def insertEventFlight(id, userIATA, goFlight, backFlight):
    dataToInsert = (id, userIATA, goFlight, backFlight, time.time())
    connection = makeConnection()
    cursor = connection.cursor()
    cursor.execute("insert into Event_Flight values (?,?,?,?,?)", dataToInsert)
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
    cursor.execute(f"SELECT eventData FROM Events WHERE country = \"{countryCode.upper()}\" AND time>{time.time() - 21600}")
    result_list = [list(row) for row in cursor.fetchall()]
    closeConnection(connection)
    return result_list


def findEventByEventId(eventId):
    connection = makeConnection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT eventData FROM Events WHERE eventId = \"{eventId}\" AND time>{time.time() - 21600}")
    result_list = [list(row) for row in cursor.fetchall()]
    closeConnection(connection)
    return result_list


def findWeatherByEvent(eventId):
    connection = makeConnection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT weather FROM Events_Weather WHERE eventId = \"{eventId}\" AND time>{time.time() - 21600}")
    result_list = [list(row) for row in cursor.fetchall()]
    closeConnection(connection)
    return result_list

def findFlight(eventId, IATA):
    connection = makeConnection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT goFlight, backFlight FROM Event_FLight WHERE eventId = \"{eventId}\" AND depIATA =\"{IATA}\" AND time>{time.time() - 21600}")
    result_list = [list(row) for row in cursor.fetchall()]
    closeConnection(connection)
    return result_list


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