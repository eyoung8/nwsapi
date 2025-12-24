# nwsapi

Python script that calls the national weather service API

# Running

`python3 nwsapi.py`

# IP location lookup

The script looks up location info using an IP lookup of your public IP from ipinfo.io

# National Weather Service API

The script then looks up the location grid ID from the national weather service. This request returns a response that includes a URL to call to get forecast data for that grid ID. The script then calls this and prints part of that response:

````
You are in Atlanta, Georgia
Latitude: 33.749, Longitude: -84.388
Mostly sunny, with a high near 73. Northwest wind 5 to 10 mph.
````
