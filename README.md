# API_Wrapper
Educational project, that aims to create an API Wrapper using python programming language, that this wrapper is going to communicate with other 3 3rd party APIs about weather, flights, and events.

# Tools used
- Flask framework : flask
- SQLite : sqlit3

# How to execute?
After downloading the project and open it by any IDE, and by making sure that Python3 is installed already on the device.
use `pip install flask` to install flask framework which is the main drive in my project.
Now you can just simple run the `main.py` script, and you can interact with my API by the browser on `localhost:7777`.

# Endpoints of the API
- `localhost:7777/list/?countryCode=<string>`
- `localhost:7777/weather/?eventId=<string id>`
- `localhost:7777/flight/?eventId=<string id>&airportCode=<IATA code>`

test


