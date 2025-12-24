import requests
# import json
from requests.exceptions import HTTPError, Timeout, RequestException

def make_nws_request(endpoint, user_agent):
    headers = {
        "User-Agent": user_agent,
    }

    try:
        response = requests.get(
                       endpoint, 
                       headers=headers
                   )
        # Raise HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()
        return response.json()

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status code: {response.status_code}")
    except Timeout as timeout_err:
        print(f"Request timed out: {timeout_err}")
    except RequestException as req_err:
        print(f"Request error: {req_err}")

    return None  # Return None if an error occurred

def get_location_from_ip(ip_address=''):
    """
    Fetches the location (latitude, longitude, city, state) for a given IP address.
    If no IP address is provided, it uses the public IP of the machine running the script.
    """
    try:
        # ipinfo.io provides a clean API for geolocation
        if ip_address:
            # Use the specified IP address
            url = f"https://ipinfo.io/{ip_address}/json"
        else:
            # Use 'me' to automatically use your public IP
            url = "https://ipinfo.io"

        response = requests.get(url)
        data = response.json()

        if 'loc' in data:
            # 'loc' field is a string in "latitude,longitude" format
            loc = data['loc'].split(',')
            latitude = float(loc[0])
            longitude = float(loc[1])
            city = data.get('city', 'Unknown')
            state = data.get('region', 'Unknown')

            return latitude, longitude, city, state
        else:
            print("Could not find location details for the provided IP.")
            return None, None, None, None

    except requests.exceptions.RequestException as e:
        print(f"Internet or API request error: {e}")
        return None, None, None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None, None, None


if __name__ == "__main__":
    # Sample user agent
    user_agent = "YourName/1.0"


    # Get latitude and longitude from the location of your network's IP
    lat, lon, city, state = get_location_from_ip()
    if lat == None:
        print("failed to retrieve location data from ip")
        exit(1)

    # Request the national weather service to give the grid location based on latitude and longitude
    # The national weather service groups multiple latitude and longitude to a grid ID to look up
    WEATHER_API_URL = "https://api.weather.gov"
    grid_url = f"{WEATHER_API_URL}/points/{lat},{lon}"
    grid_data = make_nws_request(grid_url, user_agent)
    if grid_data == None:
        print("Failed to retrieve grid location from national weather service")
        exit(1)

    # Get the forecast URL to call from the response of the grid location lookup request
    forecast_url = grid_data['properties']['forecast']
    # Request the forecast using the grid url
    forecast_data = make_nws_request(forecast_url, user_agent)
    if forecast_data == None:
        print("failed to retrieve forecast data from national weather service")
        exit(1)

    # Get the forecast text from the forecast_data dictionary
    # there is a lot more info that can be grabbed from forecast_data
    # try looking at nwsForecastDataExample.json to find other information to work with,
    # like chance of rain and forecast for the next couple days
    # You can print more information or use that information to make new logic
    detailed_forecast = forecast_data['properties']['periods'][0]['detailedForecast']

    print(f"You are in {city}, {state}")
    print(f"Latitude: {lat}, Longitude: {lon}")
    print(detailed_forecast)

# The below commented out code prints the full forecast_data request
# To print it uncomment out the json library import and the below lines
#    json_data = json.dumps(forecast_data, indent=4)
#    print(json_data)
